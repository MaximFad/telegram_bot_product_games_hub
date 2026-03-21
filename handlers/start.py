from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from sheets import count_referrals
from referrals import get_ref_link
from handlers.menu import get_level_name


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    count = count_referrals(user_id)
    level_name = get_level_name(count)
    ref_link = await get_ref_link(context, user_id)

    text = (
        "Привет! Это Product Games Hub.\n\n"
        f"🏅 Твой уровень: «{level_name}»\n"
        "🎯 Миссия: дойти до «Амбассадора канала» и открыть все секретные материалы\n\n"
        "Выбери, с чего начать:"
    )

    keyboard = [
        [InlineKeyboardButton("📂 Таблицы и документы", callback_data="materials_menu")],
        [InlineKeyboardButton("📌 Мои реферальные ссылки", callback_data="my_refs")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=reply_markup)
