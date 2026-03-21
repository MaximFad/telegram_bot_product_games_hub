from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from config import SHEET_ID, GOOGLE_CREDENTIALS


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

creds = Credentials.from_service_account_info(
    GOOGLE_CREDENTIALS,
    scopes=SCOPES,
)
gc = gspread.authorize(creds)

spreadsheet = gc.open_by_key(SHEET_ID)
sheet_users = spreadsheet.worksheet("users")
sheet_refs = spreadsheet.worksheet("referrals")


def load_users() -> set[int]:
    records = sheet_users.col_values(1)[1:]
    result = set()

    for uid in records:
        uid = uid.strip()
        if uid.lstrip("-").isdigit():
            result.add(int(uid))

    return result


def save_user(user) -> bool:
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
    existing = sheet_refs.col_values(1)[1:]
    return str(referred_id) in existing


def save_referral(referred_id: int, invited_by: int) -> bool:
    if has_referral(referred_id):
        return False

    sheet_refs.append_row([
        referred_id,
        invited_by,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ])
    return True


def count_referrals(user_id: int) -> int:
    invited_by_col = sheet_refs.col_values(2)[1:]
    return invited_by_col.count(str(user_id))


def get_all_refs() -> list[str]:
    return sheet_refs.col_values(1)[1:]
