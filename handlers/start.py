from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID, CHANNEL_ID, get_env
from sheets import save_user, count_referrals, confirm_pending_referral
from referrals import get_ref_link, notify_inviter
from handlers.content_texts import BotTexts, BotLogic


CHANNEL_USERNAME = get_env("CHANNEL_USERNAME", "product_games_hub", required=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user.is_bot:
        if update.message:
            await update.message.reply_text("❌ Боты не участвуют в реферальной программе.")
        else:
            query = update.callback_query
            await query.answer()
            await query.message.reply_text("❌ Боты не участвуют в реферальной программе.")
        return

    pending_inviter_id = None

    if context.args:
        arg = context.args[0]
        if arg.startswith("ref_"):
            inviter_raw = arg.replace("ref_", "").strip()
            if inviter_raw.isdigit():
                inviter_id = int(inviter_raw)
                if inviter_id != user_id:
                    pending_inviter_id = inviter_id

    save_user(user, pending_inviter_id=pending_inviter_id)

    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        is_subscribed = member.status in ("member", "administrator", "creator")
    except Exception:
        is_subscribed = False

    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton(BotTexts.BTN_SUBSCRIBE, url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton(BotTexts.BTN_CHECK_SUBSCRIBE, callback_data="link_1")],
        ]
        text = BotTexts.not_subscribed(CHANNEL_USERNAME)

        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            await update.message.reply_text(text, reply_markup=reply_markup)
        else:
            query = update.callback_query
            await query.answer()
            await query.message.reply_text(text, reply_markup=reply_markup)
        return

    inviter_id = confirm_pending_referral(user_id)
    if inviter_id:
        refs_count = count_referrals(inviter_id)
        await notify_inviter(context, inviter_id, refs_count)

    count = count_referrals(user_id)
    level_name = BotLogic.get_level_name(count)
    ref_link = await get_ref_link(context, user_id)

    text = BotTexts.main_menu(level_name, ref_link)

    keyboard = [
        [InlineKeyboardButton(BotTexts.BTN_MATERIALS, callback_data="materials_menu")],
        [InlineKeyboardButton(BotTexts.BTN_MY_REFS, callback_data="my_refs")],
    ]

    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton(BotTexts.BTN_ADMIN, callback_data="admin_panel")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=reply_markup)
