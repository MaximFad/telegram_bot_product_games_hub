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
            "🏆 Все миссии пройдены.\n\n"
            "Текущий статус: «Амбассадор канала»\n"
            f"👥 Всего приглашено друзей: {count}\n\n"
            "Хочешь помочь каналу расти ещё сильнее? Продолжай делиться ссылкой:\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    elif count >= REFERRALS_FOR_BONUS_1:
        done_on_level2 = count - REFERRALS_FOR_BONUS_1
        remaining = REFERRALS_FOR_BONUS_2 - count
        text = (
            "🎯 Миссия: уровень «Инсайдер»\n\n"
            "✅ Первый секретный подарок уже твой.\n"
            "Задача: пригласи ещё 3 друзей и открой супер-секретный бонус.\n\n"
            f"👥 Прогресс: {done_on_level2} из 3\n"
            f"Осталось пригласить: {remaining} друга(ов)\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    else:
        remaining = REFERRALS_FOR_BONUS_1 - count
        text = (
            "🎯 Миссия: уровень «Новичок»\n\n"
            "Хочешь получить закрытый материал бесплатно?\n"
            "Пригласи 2 друзей по своей реферальной ссылке.\n"
            "Друг должен подписаться на канал и запустить бота — тогда засчитается.\n\n"
            f"👥 Приглашено друзей: {count} из {REFERRALS_FOR_BONUS_1}\n"
            f"Осталось пригласить: {remaining} друга(ов)\n\n"
            f"🔗 Твоя ссылка:\n{ref_link}"
        )

    await query.message.reply_text(text, reply_markup=share_keyboard(ref_link))
