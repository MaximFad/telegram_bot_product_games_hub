from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import LINKS, CHANNEL_ID, REFERRALS_FOR_BONUS_1
from sheets import count_referrals
from referrals import get_ref_link, share_keyboard

async def check_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    key = query.data
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            link, name = LINKS[key]
            ref_link = await get_ref_link(context, user_id)
            count = count_referrals(user_id)
            await query.message.reply_text(
                f"✅ Вот твой материал — {name}:\n{link}\n\n"
                f"🎁 Пригласи 2 друзей — получи секретный материал!\n"
                f"👥 Приглашено: {count}/{REFERRALS_FOR_BONUS_1}",
                reply_markup=share_keyboard(ref_link)
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Подписаться на канал", url="https://t.me/product_games_hub")],
                [InlineKeyboardButton("✅ Я подписался", callback_data=key)]
            ]
            await query.message.reply_text(
                "❌ Сначала подпишись на канал и нажми кнопку снова.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except Exception:
        await query.message.reply_text("Ошибка проверки. Попробуй снова.")