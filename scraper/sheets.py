import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

COMPETITOR_SHEET = "competitor-slots"
COMPARISON_SHEET = "comparison"
SPREADSHEET_ID = "1SYmQBiCaz_hxguFdOMVpE7DpLHK3xi1w2mYSeicGkjw"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_service():
    creds_json = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        creds_json,
        scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)

def clear_sheet(service, sheet_name):
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=sheet_name
    ).execute()

def write_competitor_matrices(data):
    service = get_service()

    clear_sheet(service, COMPETITOR_SHEET)

    rows = []

    for course in data.values():
        rows.append([course["name"]])
        rows.append(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

        day_map = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": []
        }

        for day, start, end in course["slots"]:
            day_map[day].append(f"{start}-{end}")

        max_rows = max(len(v) for v in day_map.values())

        for i in range(max_rows):
            rows.append([
                day_map["Monday"][i] if i < len(day_map["Monday"]) else "",
                day_map["Tuesday"][i] if i < len(day_map["Tuesday"]) else "",
                day_map["Wednesday"][i] if i < len(day_map["Wednesday"]) else "",
                day_map["Thursday"][i] if i < len(day_map["Thursday"]) else "",
                day_map["Friday"][i] if i < len(day_map["Friday"]) else "",
                day_map["Saturday"][i] if i < len(day_map["Saturday"]) else "",
                day_map["Sunday"][i] if i < len(day_map["Sunday"]) else "",
            ])

        rows.append([])
        rows.append([])
