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

    keyboard = [[InlineKeyboardButton(name, callback_data=key)] for key, (_, name) in LINKS.items()]
    keyboard.append([InlineKeyboardButton("🎁 Мой прогресс и бонусы", callback_data="my_refs")])
    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel")])

    await update.effective_message.reply_text(
        "👋 Привет! Добро пожаловать в Product Games Hub.\n\n"
        "🎯 У тебя есть 2 уровня наград:\n\n"
        "1) «Новичок» — пригласи 2 друзей и получи первый секретный материал\n"
        "2) «Инсайдер» — пригласи ещё 3 друзей и открой супер-секретный бонус\n\n"
        "Выбери, с чего начать:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
