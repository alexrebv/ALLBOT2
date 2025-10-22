import os
import json
import gspread
from google.oauth2.service_account import Credentials

GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS_FILE")
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")

def get_sheet(sheet_name):
    creds_dict = json.loads(GOOGLE_CREDENTIALS)  # JSON из строки
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
