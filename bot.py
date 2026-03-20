import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

LINKS = {
    "link_1": (os.environ["LINK_1"], "📊 Инструменты для анализа игр"),
    "link_2": (os.environ["LINK_2"], "Пример карточки проекта"),
    "link_3": (os.environ["LINK_3"], "Пример отличного туториала"),
    "link_4": (os.environ["LINK_3"], "Статьи на Teletype"),
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=key)] for key, (_, name) in LINKS.items()]
    await update.message.reply_text(
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

from telegram.ext import MessageHandler, filters

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_and_send))
app.add_handler(MessageHandler(filters.ALL, start))
app.run_polling()
