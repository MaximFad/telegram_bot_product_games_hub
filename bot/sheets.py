import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from config import SHEET_ID, GOOGLE_CREDENTIALS

creds = Credentials.from_service_account_info(GOOGLE_CREDENTIALS, scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
])
gc = gspread.authorize(creds)
sheet_users = gc.open_by_key(SHEET_ID).worksheet("users")
sheet_refs = gc.open_by_key(SHEET_ID).worksheet("referrals")

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
            "✅" if user.is_premium else "",
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

def count_referrals(user_id):
    invited_by_col = sheet_refs.col_values(2)[1:]
    return invited_by_col.count(str(user_id))

def get_all_refs():
    return sheet_refs.col_values(1)[1:]
