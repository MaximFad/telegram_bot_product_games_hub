import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
ADMIN_ID = int(os.environ["ADMIN_ID"])
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]

creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_json, scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
])
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).worksheet("users")

WAITING_BROADCAST = 1

LINKS = {
    "link_1": (os.environ["LINK_1"], "📊 Инструменты для анализа игр"),
    "link_2": (os.environ["LINK_2"], "Пример карточки проекта"),
    "link_3": (os.environ["LINK_3"], "Пример отличного туториала"),
    "link_4": (os.environ["LINK_4"], "Статьи на Teletype"),
}

def load_users():
    records = sheet.col_values(1)[1:]
    return set(int(uid) for uid in records if uid.strip().lstrip('-').isdigit())

def save_user(user):
    users = load_users()
    if user.id not in users:
        sheet.append_row([
            user.id,
            user.username or "",
            user.first_name or "",
            user.last_name or "",
            user.language_code or "",
            "✅" if user.is_premium else ""
        ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user)
    keyboard = [[InlineKeyboardButton(name, callback_data=key)] for key, (_, name) in LINKS.items()]
    if update.effective_user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("🔧 Админ панель", callback_data="admin_panel")])
    await update.effective_message.reply_text(
        "👋 Выбери материал который хочешь получить:",
        reply_markup=InlineKeyboardMarkup(keyboard)
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
            await query.message.reply_text(f"✅ Вот твой материал — {name}:\n{link}")
        else:
            keyboard = [[InlineKeyboardButton("✅ Я подписался", callback_data=key)]]
            await query.message.reply_text(
                "❌ Сначала подпишись на канал @product_games_hub и нажми кнопку снова.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except Exception:
        await query.message.reply_text("Ошибка проверки. Попробуй снова.")

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
    await query.message.reply_text(f"📊 Всего пользователей: {len(users)}")

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
    await update.message.reply_text(f"✅ Отправлено {success} из {len(users)} пользователей")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

broadcast_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(ask_broadcast_text, pattern="^do_broadcast$")],
    states={WAITING_BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_broadcast)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(broadcast_conv)
app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
app.add_handler(CallbackQueryHandler(stats, pattern="^stats$"))
app.add_handler(CallbackQueryHandler(check_and_send))
app.add_handler(MessageHandler(filters.ALL, start))
app.run_polling()
