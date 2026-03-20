from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from sheets import load_users, get_all_refs

WAITING_BROADCAST = 1

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("📢 Сделать рассылку", callback_data="do_broadcast")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
    ]
    await query.message.reply_text("🔧 Админ панель:", reply_markup=InlineKeyboardMarkup(keyboard))

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = load_users()
    refs = get_all_refs()
    await query.message.reply_text(
        f"📊 Всего пользователей: {len(users)}\n"
        f"🔗 Всего рефералов: {len(refs)}"
    )

async def ask_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✏️ Напиши текст рассылки:")
    return WAITING_BROADCAST

async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
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