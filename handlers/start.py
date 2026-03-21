from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID
from sheets import save_user, save_referral, count_referrals
from referrals import get_ref_link, notify_inviter
from handlers.menu import get_level_name


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    is_new_user = save_user(user)

    if context.args and is_new_user:
        arg = context.args[0]

        if arg.startswith("ref_"):
            inviter_raw = arg.replace("ref_", "").strip()

            if inviter_raw.isdigit():
                inviter_id = int(inviter_raw)

                if inviter_id != user_id:
                    was_saved = save_referral(user_id, inviter_id)

                    if was_saved:
                        refs_count = count_referrals(inviter_id)
                        await notify_inviter(context, inviter_id, refs_count)

    count = count_referrals(user_id)
    level_name = get_level_name(count)
    ref_link = await get_ref_link(context, user_id)

    text = (
        "Привет! Это Product Games Hub.\n\n"
        f"🏅 Твой уровень: «{level_name}»\n"
        "🎯 Миссия: дойти до «Амбассадора канала» и открыть все секретные материалы\n\n"
        f"🔗 Твоя ссылка:\n{ref_link}\n\n"
        "Выбери, с чего начать:"
    )

    keyboard = [
        [InlineKeyboardButton("📂 Таблицы и документы", callback_data="materials_menu")],
        [InlineKeyboardButton("📌 Мои реферальные ссылки", callback_data="my_refs")],
    ]

    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=reply_markup)
