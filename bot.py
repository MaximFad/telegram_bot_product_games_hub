import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
ADMIN_ID = int(os.environ["ADMIN_ID"])
SHEET_ID = os.environ["GOOGLE_SHEET_ID"]

# Подключение к Google Sheets
creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_json, scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
])
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_ID).worksheet("users")

def load_users():
    records = sheet.col_values(1)[1:]  # пропускаем заголовок
    return set(int(uid) for uid in records if uid)

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        sheet.append_row([user_id])

LINKS = {
    "link_1": (os.environ["LINK_1"], "📊 Инструменты для анализа игр"),
    "link_2": (os.environ["LINK_2"], "Пример карточки проекта"),
    "link_3": (os.environ["LINK_3"], "Пример отличного туториала"),
    "link_4": (os.environ["LINK_4"], "Статьи на Teletype"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    keyboard = [[InlineKeyboardButton(name, callback_data=key)] for key, (_, name) in LINKS.items()]
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

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Напиши текст: /broadcast Привет!")
        return
    text = " ".join(context.args)
    users = load_users()
    success = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"🔔 {text}")
            success += 1
        except Exception:
            pass
    await update.message.reply_text(f"✅ Отправлено {success} из {len(users)} пользователей")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(check_and_send))
app.add_handler(MessageHandler(filters.ALL, start))
app.run_polling()
