from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import (
    LINKS,
    BONUS_LINKS,
    CHANNEL_ID,
    REFERRALS_FOR_BONUS_1,
    REFERRALS_FOR_BONUS_2,
    ADMIN_ID,
    get_env,
)
from sheets import count_referrals, confirm_pending_referral
from referrals import get_ref_link, share_keyboard, notify_inviter
from handlers.content_texts import BotTexts, BotLogic


CHANNEL_USERNAME = get_env("CHANNEL_USERNAME", "product_games_hub", required=False)


async def is_user_subscribed(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False


async def send_subscription_required(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(BotTexts.BTN_SUBSCRIBE, url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton(BotTexts.BTN_CHECK_SUBSCRIBE, callback_data="check_subscription")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = BotTexts.not_subscribed(CHANNEL_USERNAME)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=reply_markup)
        return

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if not await is_user_subscribed(context, user_id):
        await send_subscription_required(update, context)
        return False

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

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=reply_markup)
        return True

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
        return True

    return True


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)


async def materials_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if not await is_user_subscribed(context, user_id):
        await send_subscription_required(update, context)
        return

    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)]
        for key, (_, name) in LINKS.items()
    ]

    count = count_referrals(user_id)

    if count >= REFERRALS_FOR_BONUS_1:
        keyboard.append([
            InlineKeyboardButton(BotTexts.BONUS_1_MENU_TITLE, callback_data="secret_1")
        ])

    if count >= REFERRALS_FOR_BONUS_2:
        keyboard.append([
            InlineKeyboardButton(BotTexts.BONUS_2_MENU_TITLE, callback_data="secret_2")
        ])

    await query.message.reply_text(
        BotTexts.materials_menu(),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def check_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    key = query.data

    try:
        if not await is_user_subscribed(context, user_id):
            await send_subscription_required(update, context)
            return

        inviter_id = confirm_pending_referral(user_id)
        if inviter_id:
            refs_count = count_referrals(inviter_id)
            await notify_inviter(context, inviter_id, refs_count)

        ref_link = await get_ref_link(context, user_id)
        count = count_referrals(user_id)
        level_name = BotLogic.get_level_name(count)

        if key.startswith("link_"):
            if key not in LINKS:
                await query.message.reply_text(BotTexts.TEXT_MATERIAL_NOT_FOUND)
                return

            link, name = LINKS[key]

            await query.message.reply_text(
                BotTexts.material_opened(
                    material_name=name,
                    material_link=link,
                    current_level=level_name,
                    current_refs=count,
                    ref_link=ref_link,
                ),
                reply_markup=share_keyboard(ref_link),
            )
            return

        if key == "secret_1":
            if count < REFERRALS_FOR_BONUS_1:
                await query.message.reply_text(
                    BotTexts.bonus_locked(REFERRALS_FOR_BONUS_1, count)
                )
                return

            await query.message.reply_text(
                BotTexts.bonus_1_opened(BONUS_LINKS[1]),
                reply_markup=share_keyboard(ref_link),
            )
            return

        if key == "secret_2":
            if count < REFERRALS_FOR_BONUS_2:
                await query.message.reply_text(
                    BotTexts.bonus_locked(REFERRALS_FOR_BONUS_2, count)
                )
                return

            await query.message.reply_text(
                BotTexts.bonus_2_opened(BONUS_LINKS[2]),
                reply_markup=share_keyboard(ref_link),
            )
            return

        await query.message.reply_text(BotTexts.TEXT_UNKNOWN_ACTION)

    except Exception:
        await query.message.reply_text(BotTexts.TEXT_CHECK_ERROR)
