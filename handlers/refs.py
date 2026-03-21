from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sheets import count_referrals
from referrals import get_ref_link, share_keyboard
from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2
from handlers.menu import get_level_name, get_next_level_target


async def my_refs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    count = count_referrals(user_id)
    ref_link = await get_ref_link(context, user_id)

    level_name = get_level_name(count)
    next_level_name, next_threshold = get_next_level_target(count)

    base_text = (
        "👋 Это твоя реферальная панель.\n\n"
        f"🏅 Текущий уровень: «{level_name}»\n"
        f"👥 Твои приглашённые: {count}\n\n"
        f"🔗 Твоя ссылка:\n{ref_link}\n\n"
    )

    if next_level_name and next_threshold:
        base_text += (
            f"🎯 Цель: дойти до уровня «{next_level_name}» и набрать {next_threshold} приглашённых.\n"
            "За уровни открываются секретные бонусы и материалы."
        )
    else:
        base_text += (
            "🎯 Ты на максимальном уровне «Амбассадор канала».\n"
            "Дальше будут временные челленджи и сезонные бонусы для амбассадоров."
        )

    keyboard = [
        [InlineKeyboardButton("📤 Поделиться ссылкой", switch_inline_query=ref_link)],
        [InlineKeyboardButton("⬅️ Вернуться в меню", callback_data="back_to_menu")],
    ]

    await query.message.reply_text(
        base_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
