from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import LINKS, ADMIN_ID, REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2
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

    refs_count = count_referrals(user.id)
    if refs_count >= REFERRALS_FOR_BONUS_2:
        player_level = "Амбассадор канала"
    elif refs_count >= REFERRALS_FOR_BONUS_1:
        player_level = "Инсайдер"
    else:
        player_level = "Новичок"

    keyboard = []
    keyboard.append([InlineKeyboardButton("📂 Таблицы и документы", callback_data="materials_menu")])
    keyboard.append([InlineKeyboardButton("🎯 Миссии и награды", callback_data="my_refs")])

    if user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel")])

    await update.effective_message.reply_text(
        "👋 Привет! Это Product Games Hub.\n\n"
        f"🏅 Твой уровень: «{player_level}»\n"
        "🎯 Миссия: дойти до «Амбассадора канала» и открыть все секретные материалы\n\n"
        "Выбери материал который хочешь получить:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
