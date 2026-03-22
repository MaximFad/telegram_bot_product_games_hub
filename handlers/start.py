from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID
from sheets import save_user, save_referral, count_referrals
from referrals import get_ref_link, notify_inviter
from content_texts import BotTexts, BotLogic


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # ---------------------------------------------------------
    # ЗАЩИТА ОТ БОТОВ
    # Если в бота зашёл telegram-бот, не засчитываем его как реферала
    # и вообще не даём ему участвовать в реферальной механике.
    # ---------------------------------------------------------
    if user.is_bot:
        if update.message:
            await update.message.reply_text("❌ Боты не участвуют в реферальной программе.")
        else:
            query = update.callback_query
            await query.answer()
            await query.message.reply_text("❌ Боты не участвуют в реферальной программе.")
        return

    is_new_user = save_user(user)

    # ---------------------------------------------------------
    # ОБРАБОТКА РЕФЕРАЛКИ
    # Засчитываем только:
    # - нового пользователя
    # - не бота
    # - если есть ref_...
    # - если не сам себя пригласил
    # ---------------------------------------------------------
    if context.args and is_new_user:
        arg = context.args[0]

        if arg.startswith("ref_"):
            inviter_raw = arg.replace("ref_", "").strip()

            if inviter_raw.isdigit():
                inviter_id = int(inviter_raw)

                if inviter_id != user_id:
                    was_saved = save_referral(user_id, inviter_id)

                    if was_saved:
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
