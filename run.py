import gspread
from google.oauth2.service_account import Credentials
from dataclasses import dataclass


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('rain_data')

WORKSHEET_NAME = "sheet1"

# The header row in the worksheet file.
HEADERS = ["year", "month", "rain_volume(mm/h)",
           "area_m2", "density", "save_at"]


@dataclass
class RainEntry:
    year: int
    month: int
    rain_volume: float
    area_m2: float
    density: float    
    save_at: str         


def open_worksheet():
    """Open (and if needed, create) the target worksheet."""""
    try:
        ws = SHEET.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = SHEET.add_worksheet(title=WORKSHEET_NAME,
                                 rows=1000, cols=len(HEADERS))

    existing = ws.row_values(1)
    if existing != HEADERS:
        ws.clear()
        ws.append_row(HEADERS)
    return ws


def append_entry(ws, entry):
    """
    Append a single entry to the worksheet.
    """
    ws.append_row([entry.year,
                   entry.month, 
                   entry.rain_volume,
                   entry.area_m2,
                   entry.density,
                   entry.save_at
                   ])


""" Test append_entry function.
if __name__ == "__main__":
    ws = open_worksheet()
    test_entry = RainEntry(
        year=2024,
        month=1,
        rain_volume=42.5,
        area_m2=25,
        density=42.5 / 25,  # should be 1.7
        save_at="TEST_ENTRY"
    )
    append_entry(ws, test_entry)
    print("Test entry added to Google Sheet")"""


def get_entries(ws):
    """
    Read all entries from the sheet (skrips header)
    """
    records = ws.get_all_values()[1:]  # To skip the header
    entries = []

    for row in records:
        try:
            year = int(row[0])
            month = int(row[1])
            rain_volume = float(row[2])
            area = float(row[3])
            density = float(row[4])
            if len(row) > 5 and row[5].strip():
                save_at = row[5].strip()
            else:
                save_at = "N/A"
            entries.append(RainEntry(year, month, rain_volume,
                                     area, density, save_at))
        except (IndexError, ValueError):
            continue

    return entries

# Test the get_entries() function


if __name__ == "__main__":
    ws = open_worksheet()
    entries = get_entries(ws)

    print("Entiers feched from google sheet")
    if entries != []:
        for e in entries:
            print(e)

