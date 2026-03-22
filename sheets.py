from datetime import datetime
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from config import SHEET_ID, GOOGLE_CREDENTIALS


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_client():
    creds = Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=SCOPES,
    )
    return gspread.authorize(creds)


def get_spreadsheet():
    return get_client().open_by_key(SHEET_ID)


def get_users_sheet():
    return get_spreadsheet().worksheet("users")


def get_refs_sheet():
    return get_spreadsheet().worksheet("referrals")


def get_game_reviews_sheet():
    return get_spreadsheet().worksheet("game_reviews")


def get_leaderboard_sheet():
    return get_spreadsheet().worksheet("leaderboard_points")


def load_users() -> set[int]:
    sheet_users = get_users_sheet()
    records = sheet_users.col_values(1)[1:]
    return set(int(uid) for uid in records if uid.strip().lstrip("-").isdigit())


def _find_user_row(user_id: int) -> Optional[int]:
    sheet_users = get_users_sheet()
    user_ids = sheet_users.col_values(1)

    for index, value in enumerate(user_ids[1:], start=2):
        if value.strip() == str(user_id):
            return index

    return None


def _find_leaderboard_row(user_id: int) -> Optional[int]:
    sheet = get_leaderboard_sheet()
    user_ids = sheet.col_values(1)

    for index, value in enumerate(user_ids[1:], start=2):
        if value.strip() == str(user_id):
            return index

    return None


def save_user(user, pending_inviter_id: Optional[int] = None) -> bool:
    """
    Колонки users:
    A: user_id
    B: username
    C: first_name
    D: last_name
    E: language_code
    F: premium
    G: created_at
    H: pending_inviter_id
    I: referral_confirmed_at
    """
    sheet_users = get_users_sheet()
    users = load_users()

    if user.id in users:
        return False

    safe_pending_inviter = ""
    if (
        pending_inviter_id
        and pending_inviter_id != user.id
        and not getattr(user, "is_bot", False)
    ):
        safe_pending_inviter = str(pending_inviter_id)

    sheet_users.append_row([
        user.id,
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        user.language_code or "",
        "✅" if getattr(user, "is_premium", False) else "",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        safe_pending_inviter,
        "",
    ])
    return True


def has_referral(referred_id: int) -> bool:
    sheet_refs = get_refs_sheet()
    existing = sheet_refs.col_values(1)[1:]
    return str(referred_id) in existing


def save_referral(referred_id: int, invited_by: int) -> bool:
    if referred_id == invited_by:
        return False

    sheet_refs = get_refs_sheet()

    if has_referral(referred_id):
        return False

    sheet_refs.append_row([
        referred_id,
        invited_by,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ])
    return True


def get_pending_inviter(user_id: int) -> Optional[int]:
    row = _find_user_row(user_id)
    if not row:
        return None

    sheet_users = get_users_sheet()
    value = sheet_users.cell(row, 8).value  # H = pending_inviter_id

    if value and value.strip().isdigit():
        return int(value.strip())

    return None


def clear_pending_inviter(user_id: int):
    row = _find_user_row(user_id)
    if not row:
        return

    sheet_users = get_users_sheet()
    sheet_users.update_cell(row, 8, "")


def mark_referral_confirmed(user_id: int):
    row = _find_user_row(user_id)
    if not row:
        return

    sheet_users = get_users_sheet()
    sheet_users.update_cell(row, 9, datetime.now().strftime("%Y-%m-%d %H:%M"))


def confirm_pending_referral(user_id: int) -> Optional[int]:
    """
    Подтверждает реферала только после проверки подписки.
    Возвращает inviter_id, если реферал реально был засчитан.
    """
    if has_referral(user_id):
        clear_pending_inviter(user_id)
        return None

    inviter_id = get_pending_inviter(user_id)
    if not inviter_id:
        return None

    if inviter_id == user_id:
        clear_pending_inviter(user_id)
        return None

    was_saved = save_referral(user_id, inviter_id)
    clear_pending_inviter(user_id)

    if not was_saved:
        return None

    mark_referral_confirmed(user_id)
    return inviter_id


def count_referrals(user_id: int) -> int:
    sheet_refs = get_refs_sheet()
    invited_by_col = sheet_refs.col_values(2)[1:]
    return invited_by_col.count(str(user_id))


def get_all_refs() -> list[str]:
    sheet_refs = get_refs_sheet()
    return sheet_refs.col_values(1)[1:]


def save_game_review(user, message_text: str):
    sheet = get_game_reviews_sheet()

    username = user.username or ""
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    contact = f"@{user.username}" if user.username else f"tg://user?id={user.id}"

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user.id,
        username,
        first_name,
        last_name,
        contact,
        message_text or "",
    ])


def ensure_leaderboard_user(user):
    row = _find_leaderboard_row(user.id)
    sheet = get_leaderboard_sheet()

    if row:
        sheet.update(f"B{row}:F{row}", [[
            user.username or "",
            user.first_name or "",
            user.last_name or "",
            sheet.cell(row, 5).value or "0",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ]])
        return

    sheet.append_row([
        user.id,
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ])


def increment_comment_count(user) -> int:
    ensure_leaderboard_user(user)

    row = _find_leaderboard_row(user.id)
    sheet = get_leaderboard_sheet()

    current_value = sheet.cell(row, 5).value or "0"
    current_count = int(current_value) if str(current_value).isdigit() else 0
    new_count = current_count + 1

    sheet.update(f"B{row}:F{row}", [[
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        str(new_count),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]])

    return new_count


def _load_users_map() -> dict[int, dict]:
    sheet_users = get_users_sheet()
    rows = sheet_users.get_all_values()

    result = {}
    for row in rows[1:]:
        if not row or not row[0].strip().isdigit():
            continue

        user_id = int(row[0].strip())
        result[user_id] = {
            "username": row[1] if len(row) > 1 else "",
            "first_name": row[2] if len(row) > 2 else "",
            "last_name": row[3] if len(row) > 3 else "",
        }

    return result


def get_leaderboard_data() -> list[dict]:
    users_map = _load_users_map()

    refs_sheet = get_refs_sheet()
    refs_rows = refs_sheet.get_all_values()[1:]

    referrals_map: dict[int, int] = {}
    for row in refs_rows:
        if len(row) < 2:
            continue
        inviter_raw = row[1].strip()
        if inviter_raw.isdigit():
            inviter_id = int(inviter_raw)
            referrals_map[inviter_id] = referrals_map.get(inviter_id, 0) + 1

    leaderboard_sheet = get_leaderboard_sheet()
    leaderboard_rows = leaderboard_sheet.get_all_values()[1:]

    activity_map: dict[int, dict] = {}
    for row in leaderboard_rows:
        if not row or not row[0].strip().isdigit():
            continue

        user_id = int(row[0].strip())
        activity_map[user_id] = {
            "comments_count": int(row[4]) if len(row) > 4 and str(row[4]).isdigit() else 0,
            "username": row[1] if len(row) > 1 else "",
            "first_name": row[2] if len(row) > 2 else "",
            "last_name": row[3] if len(row) > 3 else "",
        }

    all_user_ids = set(users_map.keys()) | set(activity_map.keys()) | set(referrals_map.keys())

    result = []
    for user_id in all_user_ids:
        user_info = users_map.get(user_id, {})
        activity_info = activity_map.get(user_id, {})

        username = activity_info.get("username") or user_info.get("username") or ""
        first_name = activity_info.get("first_name") or user_info.get("first_name") or ""
        last_name = activity_info.get("last_name") or user_info.get("last_name") or ""

        comments_count = activity_info.get("comments_count", 0)
        referrals_count = referrals_map.get(user_id, 0)

        points = comments_count * 20 + referrals_count * 40

        result.append({
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "comments_count": comments_count,
            "referrals_count": referrals_count,
            "points": points,
        })

    result.sort(key=lambda item: (-item["points"], -item["referrals_count"], item["user_id"]))
    return result
