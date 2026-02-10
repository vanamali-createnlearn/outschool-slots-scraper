import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

COMPETITOR_SHEET = "competitor-slots"
COMPARISON_SHEET = "comparison"
SPREADSHEET_NAME = "roblox-slot-analyses"

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
        spreadsheetId=SPREADSHEET_NAME,
        range=sheet_name
    ).execute()

def write_competitor_matrices(data):
    service = get_service()

    clear_sheet(service, COMPETITOR_SHEET)

    rows = []

    for course in data.values():
        rows.append([course["name"]])
        rows.append(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

        day_map = {d: [] for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]}

        for day, start, end in course["slots"]:
            day_map[day].append(f"{start}-{end}")

        max_rows = max(len(v) for v in day_map.values())

        for i in range(max_rows):
            row = []
            for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
                row.append(day_map[d][i] if i < len(day_map[d]) else "")
            rows.append(row)

        rows.append([])
        rows.append([])

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_NAME,
        range=COMPETITOR_SHEET,
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()

def write_comparisons(course_name, comparison):
    service = get_service()

    existing = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_NAME,
        range=COMPARISON_SHEET
    ).execute().get("values", [])

    rows = existing

    rows.append([f"Comparison for {course_name}"])
    rows.append(["Missing slots (competitors have)"])

    for d,s,e in sorted(comparison["missing"]):
        rows.append([d, f"{s}-{e}"])

    rows.append([])
    rows.append(["Extra slots (we have)"])

    for d,s,e in sorted(comparison["extra"]):
        rows.append([d, f"{s}-{e}"])

    rows.append([])
    rows.append([])

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_NAME,
        range=COMPARISON_SHEET,
        valueInputOption="RAW",
        body={"values": rows}
    ).execute()
