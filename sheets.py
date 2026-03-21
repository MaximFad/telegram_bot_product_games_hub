from datetime import datetime

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


def save_user(user) -> bool:
    sheet_users = get_users_sheet()
    users = load_users()

    if user.id in users:
        return False

    sheet_users.append_row([
        user.id,
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        user.language_code or "",
        "✅" if getattr(user, "is_premium", False) else "",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ])
    return True


def has_referral(referred_id: int) -> bool:
    sheet_refs = get_refs_sheet()
    existing = sheet_refs.col_values(1)[1:]
    return str(referred_id) in existing


def save_referral(referred_id: int, invited_by: int) -> bool:
    sheet_refs = get_refs_sheet()

    if has_referral(referred_id):
        return False

    sheet_refs.append_row([
        referred_id,
        invited_by,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ])
    return True


def count_referrals(user_id: int) -> int:
    sheet_refs = get_refs_sheet()
    invited_by_col = sheet_refs.col_values(2)[1:]
    return invited_by_col.count(str(user_id))


def get_all_refs() -> list[str]:
    sheet_refs = get_refs_sheet()
    return sheet_refs.col_values(1)[1:]
