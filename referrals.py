from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2, BONUS_LINKS


async def get_ref_link(context, user_id: int) -> str:
    bot_username = (await context.bot.get_me()).username
    return f"https://t.me/{bot_username}?start=ref_{user_id}"


def share_keyboard(ref_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "📤 Поделиться с другом",
                url=(
                    "https://t.me/share/url"
                    f"?url={ref_link}"
                    "&text=Забери%20бесплатные%20материалы%20по%20gamedev%20👇"
                ),
            )
        ]]
    )


async def notify_inviter(context, inviter_id: int, refs_count: int):
    ref_link = await get_ref_link(context, inviter_id)

    if refs_count == 1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                "🙌 Один друг уже с нами!\n\n"
                "Текущий уровень: «Новичок»\n"
                f"👥 Приглашено друзей: 1 из {REFERRALS_FOR_BONUS_1}\n\n"
                "Ещё 1 друг — и ты получишь первый секретный материал.\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link),
        )

    elif refs_count == REFERRALS_FOR_BONUS_1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                "🎉 Уровень «Новичок» завершён!\n\n"
                "Вот твой первый секретный материал:\n"
                f"🔗 {BONUS_LINKS[1]}\n\n"
                "🎯 Новый квест: уровень «Инсайдер»\n"
                "Пригласи ещё 3 друзей и получи супер-секретный бонус.\n\n"
                "Текущий прогресс уровня «Инсайдер»: 0 из 3\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link),
        )

    elif REFERRALS_FOR_BONUS_1 < refs_count < REFERRALS_FOR_BONUS_2:
        done_on_level2 = refs_count - REFERRALS_FOR_BONUS_1
        total_on_level2 = REFERRALS_FOR_BONUS_2 - REFERRALS_FOR_BONUS_1
        remaining = REFERRALS_FOR_BONUS_2 - refs_count

        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                "🙌 Ещё один друг присоединился!\n\n"
                "Текущий уровень: «Инсайдер»\n"
                f"👥 Прогресс: {done_on_level2} из {total_on_level2}\n"
                f"Осталось пригласить: {remaining}\n\n"
                f"🔗 Твоя ссылка:\n{ref_link}"
            ),
            reply_markup=share_keyboard(ref_link),
        )

    elif refs_count == REFERRALS_FOR_BONUS_2:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=(
                "🏆 Уровень «Инсайдер» завершён!\n\n"
                f"Ты пригласил {REFERRALS_FOR_BONUS_2} друзей и открыл все секретные материалы.\n\n"
                "Вот твой супер-секретный бонус:\n"
                f"🔗 {BONUS_LINKS[2]}\n\n"
                "Спасибо, что помогаешь развивать канал."
            ),
        )
