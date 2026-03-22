from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from sheets import get_leaderboard_data
from handlers.content_texts import BotTexts
from handlers.menu import is_user_subscribed, send_subscription_required


def _display_name(item: dict) -> str:
    full_name = " ".join(
        part for part in [item.get("first_name", ""), item.get("last_name", "")] if part
    ).strip()

    if full_name:
        return full_name

    username = item.get("username", "")
    if username:
        return f"@{username}"

    return str(item["user_id"])


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if not await is_user_subscribed(context, user_id):
        await send_subscription_required(update, context)
        return

    leaders = get_leaderboard_data()

    if not leaders:
        await query.message.reply_text(
            BotTexts.leaderboard_empty(),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(BotTexts.BTN_BACK, callback_data="back_to_menu")]
            ]),
        )
        return

    lines = [BotTexts.leaderboard_intro(), ""]

    top3 = leaders[:3]
    medals = ["🥇", "🥈", "🥉"]

    for index, item in enumerate(top3):
        lines.append(
            f"{medals[index]} {_display_name(item)} — {item['points']} очков"
        )

    if len(leaders) > 3:
        lines.append("")
        for index, item in enumerate(leaders[3:10], start=4):
            lines.append(f"{index}. {_display_name(item)} — {item['points']} очков")

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(BotTexts.BTN_BACK, callback_data="back_to_menu")]
        ]),
    )
