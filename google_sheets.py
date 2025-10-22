import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Чтение JSON из переменной окружения Render
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS_FILE")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")  # ID таблицы

def get_sheet(sheet_name):
    if not GOOGLE_CREDENTIALS or not GOOGLE_SHEET_ID:
        raise ValueError("GOOGLE_CREDENTIALS_FILE или GOOGLE_SHEET_ID не установлены в переменных окружения")

    creds_dict = json.loads(GOOGLE_CREDENTIALS)  # JSON в одну строку
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    return sheet

def append_row(sheet_name, row_values):
    sheet = get_sheet(sheet_name)
    sheet.append_row(row_values)
