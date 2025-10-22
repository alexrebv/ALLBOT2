import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
gc = gspread.authorize(creds)

# Основные листы
users_ws = gc.open_by_key(SHEET_ID).worksheet("Users")
roles_ws = None
try:
    roles_ws = gc.open_by_key(SHEET_ID).worksheet("Roles")
except Exception:
    pass

def get_all_users():
    return users_ws.get_all_records()

def find_user_by_login(login):
    users = get_all_users()
    for u in users:
        if str(u.get("Логин", "")).strip().lower() == login.lower():
            return u
    return None

def find_user_by_tg_id(tg_id):
    users = get_all_users()
    for u in users:
        if str(u.get("Telegram ID", "")).strip() == str(tg_id):
            return u
    return None

def update_telegram_id(login, tg_id):
    cell = users_ws.find(login)
    if cell:
        users_ws.update_cell(cell.row, 3, tg_id)  # 3-й столбец = Telegram ID
        return True
    return False

def get_user_role(tg_id):
    user = find_user_by_tg_id(tg_id)
    if not user:
        return None
    return user.get("Роль", "")
