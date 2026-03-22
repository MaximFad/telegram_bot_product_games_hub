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
            "🏆 Лидерборд\n\n"
            "Очки начисляются так:\n"
            "💬 Комментарий — 20 очков\n"
            "👥 Приглашённый друг — 40 очков\n\n"
            "Твои очки: 0\n"
            "Твоё место: —\n\n"
            "Пока лидеров нет.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(BotTexts.BTN_BACK, callback_data="back_to_menu")]
            ]),
        )
        return

    my_points = 0
    my_rank = "—"

    for index, item in enumerate(leaders):
        if item["user_id"] == user_id:
            my_points = item["points"]
            my_rank = index + 1
            break

    lines = [
        "🏆 Лидерборд",
        "",
        "Очки начисляются так:",
        "💬 Комментарий — 20 очков",
        "👥 Приглашённый друг — 40 очков",
        "",
        f"Твои очки: {my_points}",
        f"Твоё место: {my_rank}",
        "",
    ]

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
