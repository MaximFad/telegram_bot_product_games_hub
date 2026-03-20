from telegram import Update
from telegram.ext import ContextTypes
from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2
from sheets import count_referrals
from referrals import get_ref_link, share_keyboard

async def my_refs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    count = count_referrals(user_id)
    ref_link = await get_ref_link(context, user_id)

    if count >= REFERRALS_FOR_BONUS_2:
        text = (
            f"🏆 Ты получил все секретные материалы!\n\n"
            f"👥 Всего приглашено друзей: {count}\n\n"
            f"Хочешь помочь каналу расти? Продолжай делиться ссылкой 💪\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )
    elif count >= REFERRALS_FOR_BONUS_1:
        remaining = REFERRALS_FOR_BONUS_2 - count
        text = (
            f"✅ Первый секретный подарок получен — поздравляем!\n\n"
            f"🔥 Хочешь ещё один супер-секретный бонус?\n"
            f"Пригласи ещё 3 друзей — и он твой!\n\n"
            f"👥 Осталось пригласить: {remaining} из 3\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )
    else:
        text = (
            f"🎁 Хочешь получить закрытый материал бесплатно?\n\n"
            f"Просто пригласи 2 друзей по своей реферальной ссылке.\n"
            f"Друг должен подписаться на канал и запустить бота — тогда засчитается.\n\n"
            f"👥 Приглашено друзей: {count} из {REFERRALS_FOR_BONUS_1}\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    await query.message.reply_text(text, reply_markup=share_keyboard(ref_link))