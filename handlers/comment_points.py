from telegram import Update
from telegram.ext import ContextTypes

from config import DISCUSSION_GROUP_ID
from sheets import increment_comment_count


async def handle_comment_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    if not message or not user or not chat:
        return

    if not DISCUSSION_GROUP_ID or chat.id != DISCUSSION_GROUP_ID:
        return

    if user.is_bot:
        return

    if getattr(message, "is_automatic_forward", False):
        return

    if not (message.text or message.caption):
        return

    has_thread_context = bool(message.reply_to_message) or bool(getattr(message, "message_thread_id", None))
    if not has_thread_context:
        return

    try:
        increment_comment_count(user)
    except Exception:
        pass
