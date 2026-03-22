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


def save_user(user, pending_inviter_id: Optional[int] = None) -> bool:
    """
    users sheet:
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
    value = sheet_users.cell(row, 8).value  # H

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
