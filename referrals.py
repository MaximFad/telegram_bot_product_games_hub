from urllib.parse import quote
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import REFERRALS_FOR_BONUS_1, REFERRALS_FOR_BONUS_2, BONUS_LINKS
from handlers.content_texts import BotTexts


async def get_ref_link(context, user_id: int) -> str:
    bot_username = (await context.bot.get_me()).username
    return f"https://t.me/{bot_username}?start=ref_{user_id}"


def share_keyboard(ref_link: str) -> InlineKeyboardMarkup:
    share_text = quote(
        "Привет! Нашёл крутой телеграм канал по геймдеву.\n\n"
        "Есть интересные темы, думаю тебе понравится, у бота можно получить все доки сразу, вот:"
    )

    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                BotTexts.BTN_SHARE_WITH_FRIEND,
                url=(
                    "https://t.me/share/url"
                    f"?url={ref_link}"
                    f"&text={share_text}"
                ),
            )
        ]]
    )

async def notify_inviter(context, inviter_id: int, refs_count: int):
    ref_link = await get_ref_link(context, inviter_id)

    if refs_count == 1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=BotTexts.invite_progress_first(ref_link, refs_count),
            reply_markup=share_keyboard(ref_link),
        )
        return

    if refs_count == REFERRALS_FOR_BONUS_1:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=BotTexts.invite_progress_bonus_1_unlocked(
                ref_link=ref_link,
                bonus_link=BONUS_LINKS[1],
            ),
            reply_markup=share_keyboard(ref_link),
        )
        return

    if REFERRALS_FOR_BONUS_1 < refs_count < REFERRALS_FOR_BONUS_2:
        done_on_level2 = refs_count - REFERRALS_FOR_BONUS_1
        total_on_level2 = REFERRALS_FOR_BONUS_2 - REFERRALS_FOR_BONUS_1
        remaining = REFERRALS_FOR_BONUS_2 - refs_count

        await context.bot.send_message(
            chat_id=inviter_id,
            text=BotTexts.invite_progress_middle(
                ref_link=ref_link,
                progress_now=done_on_level2,
                progress_total=total_on_level2,
                refs_left=remaining,
            ),
            reply_markup=share_keyboard(ref_link),
        )
        return

    if refs_count == REFERRALS_FOR_BONUS_2:
        await context.bot.send_message(
            chat_id=inviter_id,
            text=BotTexts.invite_progress_final(BONUS_LINKS[2]),
        )
