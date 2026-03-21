from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from config import ADMIN_ID
from sheets import load_users, get_all_refs


WAITING_BROADCAST = 1


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text("❌ У тебя нет доступа к админ-панели.")
        return

    keyboard = [
        [InlineKeyboardButton("📢 Сделать рассылку", callback_data="do_broadcast")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
    ]

    await query.message.reply_text(
        "🔧 Админ-панель:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text("❌ У тебя нет доступа к статистике.")
        return

    users = load_users()
    refs = get_all_refs()

    await query.message.reply_text(
        f"📊 Всего пользователей: {len(users)}\n"
        f"🔗 Всего рефералов: {len(refs)}"
    )


async def ask_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text("❌ У тебя нет доступа к рассылке.")
        return ConversationHandler.END

    await query.message.reply_text("✏️ Напиши текст рассылки:")
    return WAITING_BROADCAST


async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ У тебя нет доступа к рассылке.")
        return ConversationHandler.END

    text = update.message.text
    users = load_users()
    success = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"🔔 {text}")
            success += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ Отправлено {success}/{len(users)}")
    return ConversationHandler.END
