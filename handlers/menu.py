from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import (
    LINKS,
    CHANNEL_ID,
    REFERRALS_FOR_BONUS_1,
    REFERRALS_FOR_BONUS_2,
)
from sheets import count_referrals
from referrals import get_ref_link, share_keyboard


def get_level_name(count: int) -> str:
    if count < 2:
        return "Новичок"
    if 2 <= count < 5:
        return "Продвинутый"
    if 5 <= count < 10:
        return "Соратник"
    return "Амбассадор канала"


def get_next_level_target(count: int) -> tuple[str | None, int | None]:
    if count < 2:
        return "Продвинутый", 2
    if 2 <= count < 5:
        return "Соратник", 5
    if 5 <= count < 10:
        return "Амбассадор канала", 10
    return None, None


async def materials_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)]
        for key, (_, name) in LINKS.items()
    ]

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
        if member.status in ["member", "administrator", "creator"]:
            link, name = LINKS[key]
            ref_link = await get_ref_link(context, user_id)
            count = count_referrals(user_id)

            level_name = get_level_name(count)

            # Базовый кейс: обычный материал + реф-миссия
            if key.startswith("link_"):
                await query.message.reply_text(
                    f"✅ Достижение получено, разблокирован документ {name}:\n"
                    f"{link}\n\n"
                    "🎁 Миссия: поднять уровень персонажа\n"
                    "🎯 Цель: пригласить 2 друзей по своей ссылке и открыть первый секретный бонус.\n"
                    f"🏅 Текущий уровень: {level_name}\n"
                    f"👥 Прогресс: {count} из {REFERRALS_FOR_BONUS_1} приглашённых\n"
                    f"🔗 Твоя ссылка:\n{ref_link}",
                    reply_markup=share_keyboard(ref_link),
                )
                return

            # Если это первый секретный бонус (например, key == "secret_1")
            if key == "secret_1":
                await query.message.reply_text(
                    "✅ Достижение получено — ты выполнил реферальную миссию «Новичок»\n\n"
                    f"🎁 Разблокирован первый секретный бонус:\n"
                    f"🔒 {name}\n"
                    f"{link}\n\n"
                    "🏅 Новый уровень: «Продвинутый»\n"
                    f"👥 Твои приглашённые: {count}\n\n"
                    "Следующая цель: дойти до уровня «Амбассадор канала» и открыть второй секретный бонус.",
                    reply_markup=share_keyboard(ref_link),
                )
                return

            # Второй секретный бонус (например, key == "secret_2")
            if key == "secret_2":
                await query.message.reply_text(
                    "✅ Достижение получено — ты закрыл реферальную миссию «Продвинутый»\n\n"
                    f"🎁 Разблокирован второй секретный бонус:\n"
                    f"🔒 {name}\n"
                    f"{link}\n\n"
                    "🏅 Новый уровень: «Амбассадор канала»\n"
                    f"👥 Всего приглашённых: {count}\n\n"
                    "Ты открыл все текущие секретные материалы Product Games Hub.",
                    reply_markup=share_keyboard(ref_link),
                )
                return

            # Фолбек, если появятся другие ключи
            await query.message.reply_text(
                f"✅ Достижение получено, материал {name} разблокирован:\n{link}"
            )

        else:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 Подписаться на канал", url="https://t.me/product_games_hub"
                    )
                ],
                [InlineKeyboardButton("✅ Я подписался", callback_data=key)],
            ]
            await query.message.reply_text(
                "❌ Сначала подпишись на канал @product_games_hub, чтобы получить материалы.\n"
                "После подписки вернись в бота и нажми кнопку ещё раз.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
    except Exception:
        await query.message.reply_text("Ошибка проверки. Попробуй снова.")
