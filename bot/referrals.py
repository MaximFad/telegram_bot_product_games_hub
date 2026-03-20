from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2, BONUS_LINKS

async def get_ref_link(context, user_id):
    bot_username = (await context.bot.get_me()).username
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def share_keyboard(ref_link):
    return InlineKeyboardMarkup([[InlineKeyboardButton(
        "📤 Поделиться с другом",
        url=f"https://t.me/share/url?url={ref_link}&text=Забери%20бесплатные%20материалы%20по%20gamedev%20👇"
    )]])

async def notify_inviter(context, inviter_id, refs_count):
    ref_link = await get_ref_link(context, inviter_id)

    if refs_count == 1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                f"🙌 Один друг уже с нами!\n\n"
                f"👥 Приглашено друзей: 1 из {REFERRALS_FOR_BONUS_1}\n"
                f"🎁 Ещё 1 — и получишь секретный материал!\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link)
        )

    elif refs_count == REFERRALS_FOR_BONUS_1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                f"🎉 Поздравляем! Ты пригласил 2 друзей!\n\n"
                f"Вот твой первый секретный материал:\n"
                f"🔗 {BONUS_LINKS[1]}\n\n"
                f"———\n\n"
                f"🔥 Хочешь ещё один супер-секретный бонус?\n"
                f"Пригласи ещё 3 друзей — и он твой!\n\n"
                f"👥 Осталось пригласить: 3 из 3\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link)
        )

    elif REFERRALS_FOR_BONUS_1 < refs_count < REFERRALS_FOR_BONUS_2:
        remaining = REFERRALS_FOR_BONUS_2 - refs_count
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                f"🙌 Ещё один друг присоединился!\n\n"
                f"👥 Осталось пригласить: {remaining} из 3\n"
                f"🔥 Ты близко к супер-секретному бонусу!\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link)
        )

    elif refs_count == REFERRALS_FOR_BONUS_2:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                f"🏆 Невероятно! Ты пригласил 5 друзей!\n\n"
                f"Вот твой супер-секретный бонус:\n"
                f"🔗 {BONUS_LINKS[2]}\n\n"
                f"Спасибо, что помогаешь развивать канал — ты красавчик! 🔥"
            )
        )
