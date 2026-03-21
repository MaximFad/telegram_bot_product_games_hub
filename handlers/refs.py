from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sheets import count_referrals
from referrals import get_ref_link
from config import REFERRALS_FOR_BONUS_1
from handlers.menu import get_level_name


async def my_refs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    count = count_referrals(user_id)
    ref_link = await get_ref_link(context, user_id)
    level_name = get_level_name(count)

    text = (
        "👋 Это твоя реферальная панель.\n\n"
        f"🏅 Текущий уровень: «{level_name}»\n"
        f"👥 Твои приглашённые: {count}\n"
        f"🎯 Цель: пригласить 2 друзей и открыть первый секретный бонус.\n\n"
        f"🔗 Твоя ссылка:\n{ref_link}"
    )

    keyboard = [
        [InlineKeyboardButton("📤 Поделиться ссылкой", switch_inline_query=ref_link)],
    ]

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
