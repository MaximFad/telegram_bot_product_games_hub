from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from sheets import count_referrals
from referrals import get_ref_link
from handlers.content_texts import BotTexts, BotLogic


async def my_refs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    count = count_referrals(user_id)
    ref_link = await get_ref_link(context, user_id)

    level_name = BotLogic.get_level_name(count)
    next_level_name, next_threshold = BotLogic.get_next_level_target(count)

    text = BotTexts.refs_panel(
        current_level=level_name,
        current_refs=count,
        ref_link=ref_link,
        next_level_name=next_level_name,
        next_level_target=next_threshold,
    )

    keyboard = [
        [InlineKeyboardButton(BotTexts.BTN_SHARE, switch_inline_query=ref_link)],
        [InlineKeyboardButton(BotTexts.BTN_BACK, callback_data="back_to_menu")],
    ]

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
