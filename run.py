import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('rain_data')

WORKSHEET_NAME = "rain_data"

# The header row in the worksheet file.
HEADERS = ["Year", "Month", "Rain_Volum(mm/h)",
          "Area_m2", "Density", "Save_At"]


class RainEntry:
    year: int
    month: int
    rain_volume: float
    area_m2: float
    save_at: str


def open_worksheet() -> gspread.Worksheet:
    """Open (and if needed, create) the target worksheet."""
    try:
        ws = SHEET.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = SHEET.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(HEADERS))

    existing = ws.row_values(1)
    if existing != HEADERS:
        ws.clear()
        ws.append_row(HEADERS)
    return ws


print(open_worksheet())


