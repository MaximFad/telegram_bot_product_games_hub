from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from config import ADMIN_ID
from handlers.content_texts import BotTexts
from handlers.menu import is_user_subscribed, send_subscription_required
from sheets import save_game_review


WAITING_GAME_REVIEW = 2


def _escape_html(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _get_user_name(user) -> str:
    full_name = " ".join(
        part for part in [user.first_name, user.last_name] if part
    ).strip()
    return full_name or user.username or str(user.id)


def _get_user_contact(user) -> str:
    if user.username:
        username = _escape_html(user.username)
        return f"@{username}"
    return f'<a href="tg://user?id={user.id}">tg://user?id={user.id}</a>'


def _extract_message_text(message) -> str:
    if message.text:
        return message.text
    if message.caption:
        return message.caption

    if message.photo:
        return "[Пользователь отправил фото без текста]"
    if message.video:
        return "[Пользователь отправил видео без текста]"
    if message.document:
        filename = message.document.file_name or "без названия"
        return f"[Пользователь отправил документ: {filename}]"

    return "Текст не добавлен."


def _build_admin_text(user, message) -> str:
    sent_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    user_name = _escape_html(_get_user_name(user))
    user_contact = _get_user_contact(user)
    user_text = _escape_html(_extract_message_text(message))

    media_info = []

    if message.photo:
        media_info.append("📎 Тип: фото")
    if message.video:
        media_info.append("📎 Тип: видео")
    if message.document:
        filename = _escape_html(message.document.file_name or "без названия")
        media_info.append(f"📎 Тип: документ ({filename})")

    media_block = ""
    if media_info:
        media_block = "\n" + "\n".join(media_info)

    return (
        "🎮 <b>Новая заявка на личный разбор игры</b>\n\n"
        f"👤 <b>Имя:</b> {user_name}\n"
        f"📩 <b>Контакт:</b> {user_contact}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"📅 <b>Дата отправки:</b> {sent_at}"
        f"{media_block}\n\n"
        f"💬 <b>Сообщение:</b>\n{user_text}"
    )


async def open_game_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if not await is_user_subscribed(context, user_id):
        await send_subscription_required(update, context)
        return ConversationHandler.END

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(BotTexts.BTN_BACK, callback_data="back_to_menu")]]
    )

    await query.message.reply_text(
        BotTexts.game_review_intro(),
        reply_markup=keyboard,
    )
    return WAITING_GAME_REVIEW


async def receive_game_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    if not message or not user:
        return ConversationHandler.END

    admin_text = _build_admin_text(user, message)
    plain_text_for_sheet = _extract_message_text(message)

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception as e:
        print(f"[GAME_REVIEW_ERROR] {e}")

        await message.reply_text(
            "❌ Не удалось отправить заявку. Попробуй позже."
        )
    return ConversationHandler.END

    try:
        if message.photo or message.video or message.document:
            await context.bot.copy_message(
                chat_id=ADMIN_ID,
                from_chat_id=message.chat_id,
                message_id=message.message_id,
            )
    except Exception:
        pass

    try:
        save_game_review(user, plain_text_for_sheet)
    except Exception:
        pass

    await message.reply_text(BotTexts.game_review_sent())
    return ConversationHandler.END
