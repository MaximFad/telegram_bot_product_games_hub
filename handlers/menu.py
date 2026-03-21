from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    LINKS,
    BONUS_LINKS,
    CHANNEL_ID,
    REFERRALS_FOR_BONUS_1,
    REFERRALS_FOR_BONUS_2,
)
from sheets import count_referrals
from referrals import get_ref_link, share_keyboard


def get_level_name(count: int) -> str:
    if count < REFERRALS_FOR_BONUS_1:
        return "Новичок"
    if count < REFERRALS_FOR_BONUS_2:
        return "Инсайдер"
    return "Амбассадор канала"


def get_next_level_target(count: int):
    if count < REFERRALS_FOR_BONUS_1:
        return "Инсайдер", REFERRALS_FOR_BONUS_1
    if count < REFERRALS_FOR_BONUS_2:
        return "Амбассадор канала", REFERRALS_FOR_BONUS_2
    return None, None


async def materials_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)]
        for key, (_, name) in LINKS.items()
    ]

    count = count_referrals(query.from_user.id)

    if count >= REFERRALS_FOR_BONUS_1:
        keyboard.append([InlineKeyboardButton("🔒 Секретный бонус 1", callback_data="secret_1")])

    if count >= REFERRALS_FOR_BONUS_2:
        keyboard.append([InlineKeyboardButton("🔒 Секретный бонус 2", callback_data="secret_2")])

    await query.message.reply_text(
        "📂 Таблицы и документы — выбери материал:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def check_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    key = query.data

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status not in ("member", "administrator", "creator"):
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/product_games_hub")],
                [InlineKeyboardButton("✅ Я подписался", callback_data=key)],
            ]
            await query.message.reply_text(
                "❌ Сначала подпишись на канал @product_games_hub, чтобы получить материалы.\n"
                "После подписки вернись в бота и нажми кнопку ещё раз.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
            return

        ref_link = await get_ref_link(context, user_id)
        count = count_referrals(user_id)
        level_name = get_level_name(count)

        if key.startswith("link_"):
            if key not in LINKS:
                await query.message.reply_text("❌ Материал не найден.")
                return

            link, name = LINKS[key]

            await query.message.reply_text(
                f"✅ Разблокирован документ {name}:\n"
                f"{link}\n\n"
                "🎁 Миссия: поднять уровень персонажа\n"
                f"🎯 Цель: пригласить {REFERRALS_FOR_BONUS_1} друзей по своей ссылке и открыть первый секретный бонус.\n"
                f"🏅 Текущий уровень: {level_name}\n"
                f"👥 Прогресс: {count} из {REFERRALS_FOR_BONUS_1}\n"
                f"🔗 Твоя ссылка:\n{ref_link}",
                reply_markup=share_keyboard(ref_link),
            )
            return

        if key == "secret_1":
            if count < REFERRALS_FOR_BONUS_1:
                await query.message.reply_text(
                    f"❌ Этот бонус откроется после {REFERRALS_FOR_BONUS_1} приглашённых.\n"
                    f"Сейчас у тебя: {count}."
                )
                return

            await query.message.reply_text(
                "✅ Разблокирован первый секретный бонус:\n"
                f"{BONUS_LINKS[1]}",
                reply_markup=share_keyboard(ref_link),
            )
            return

        if key == "secret_2":
            if count < REFERRALS_FOR_BONUS_2:
                await query.message.reply_text(
                    f"❌ Этот бонус откроется после {REFERRALS_FOR_BONUS_2} приглашённых.\n"
                    f"Сейчас у тебя: {count}."
                )
                return

            await query.message.reply_text(
                "✅ Разблокирован второй секретный бонус:\n"
                f"{BONUS_LINKS[2]}",
                reply_markup=share_keyboard(ref_link),
            )
            return

        await query.message.reply_text("❌ Неизвестное действие.")

    except Exception as e:
        await query.message.reply_text(f"Ошибка проверки: {e}")
