from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import LINKS, ADMIN_ID
from sheets import save_user, save_referral, count_referrals
from referrals import notify_inviter

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_new = save_user(user)

    if is_new and context.args and context.args[0].startswith("ref_"):
        inviter_id = int(context.args[0].split("_")[1])
        if inviter_id != user.id:
            save_referral(user.id, inviter_id)
            refs_count = count_referrals(inviter_id)
            await notify_inviter(context, inviter_id, refs_count)

    keyboard = []
    keyboard.append([InlineKeyboardButton("📂 Таблицы и документы", callback_data="materials_menu")])
    keyboard.append([InlineKeyboardButton("🎯 Миссии и награды", callback_data="my_refs")])

    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel")])

    await update.effective_message.reply_text(
        "👋 Привет! Это Product Games Hub.\n\n"
        "Выбери, что тебе сейчас важно:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
