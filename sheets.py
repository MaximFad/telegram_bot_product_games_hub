import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from config import SHEET_ID, GOOGLE_CREDENTIALS

try:
    creds = Credentials.from_service_account_info(
        GOOGLE_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    print("OK: credentials parsed")
except Exception as e:
    print(f"FAIL: credentials parse error -> {e}")
    raise

try:
    gc = gspread.authorize(creds)
    print("OK: gspread authorized")
except Exception as e:
    print(f"FAIL: gspread authorize error -> {e}")
    raise

try:
    spreadsheet = gc.open_by_key(SHEET_ID)
    print("OK: spreadsheet opened")
except Exception as e:
    print(f"FAIL: spreadsheet open error -> {e}")
    raise

try:
    sheet_users = spreadsheet.worksheet("users")
    print("OK: users worksheet opened")
except Exception as e:
    print(f"FAIL: users worksheet error -> {e}")
    raise

try:
    sheet_refs = spreadsheet.worksheet("referrals")
    print("OK: referrals worksheet opened")
except Exception as e:
    print(f"FAIL: referrals worksheet error -> {e}")
    raise


def load_users():
    records = sheet_users.col_values(1)[1:]
    return set(int(uid) for uid in records if uid.strip().lstrip('-').isdigit())


def save_user(user):
    users = load_users()
    if user.id not in users:
        sheet_users.append_row([
            user.id,
            user.username or "",
            user.first_name or "",
            user.last_name or "",
            user.language_code or "",
            "✅" if getattr(user, "is_premium", False) else "",
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
        return True
    return False


def save_referral(referred_id, invited_by):
    existing = sheet_refs.col_values(1)[1:]
    if str(referred_id) not in existing:
        sheet_refs.append_row([
            referred_id,
            invited_by,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ])
        return True
    return False


def count_referrals(user_id):
    invited_by_col = sheet_refs.col_values(2)[1:]
    return invited_by_col.count(str(user_id))


def get_all_refs():
    return sheet_refs.col_values(1)[1:]
