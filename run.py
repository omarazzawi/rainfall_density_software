import gspread
from google.oauth2.service_account import Credentials
from dataclasses import dataclass
from datetime import datetime


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
            year = int(row[0].strip())
            month = int(row[1].strip())
            rain_volume = float(row[2].strip().replace(",", "."))
            area = float(row[3].strip().replace(",", "."))
            density = float(row[4].strip().replace(",", "."))
            if len(row) > 5 and row[5].strip():
                save_at = row[5].strip()
            else:
                save_at = "N/A"
            entries.append(RainEntry(year, month, rain_volume,
                                     area, density, save_at))
        except (IndexError, ValueError):
            continue

    return entries


""" Test the get_entries() function
if __name__ == "__main__":
    ws = open_worksheet()
    entries = get_entries(ws)

    print("Entiers feched from google sheet")
    if entries != []:
        for e in entries:
            print(e)"""


def input_int(prompt):
    """
    Ask the user for an intger number,
    keep retrying until get a valid input
    """
    while True:
        try:
            number = int(input(prompt))
            return number
        except ValueError:
            print("Please enter a whole number ( like 2025)")
        except Exception as e:
            print(f"Unxpected error: {e}")


def input_float(prompt):
    """
    Ask the user for a float number,
    keep retrying until get a valid input
    """
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Please enter a decimal number ( like 15.005)")
        except Exception as e:
            print(f"Unxpected error: {e}")
            return None


def confirm(prompt):
    """
    Aska yes / no question
    """
    while True:
        answer = input(prompt + "y/n: ").lower().strip()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Please anwswer 'y' or 'n'")

    """
    Test code that only runs when this file is executed directly
    if __name__ == "__main__":
    print("=== Testing Input Functions ===")
    
    print("\n1. Testing input_int:")
    year = input_int("Enter what year this data collected : ")
    print(f"Success! You entered: {year} (type: {type(year)})")
    print("\n2. Testing input_float:")
    area = input_float("Enter e: ")
    print(f"Success! You entered: {area} (type: {type(area)})")
    print("\n3. Testing confirm:")
    save_file = confirm("Do you want to save 'y' or 'n'?")
    print(f"You answered: {save_file}")"""


def compute_density(rain_volume, area_m2):
    """
    Compute the rainfall density.
    Formula:
        density = rain_volume / area_m2
    Arguments:
        rain_volume (float): Rainfall in mm/h
        area_m2 (float): Surface area in square meters
    Returns:
        float: Rainfall density (mm/h per m²), rounded to 6 decimals.
    """
    return round(rain_volume / area_m2, 6)


# The main data entry
def add_rainfall_record(ws):
    """
    Collects input for a single rainfall record
    (year, month, volume, area).
    Computes density and saves the record
    to Google Sheets if confirmed.
    Arguments:
        ws (gspread.Worksheet): The Google Sheets worksheet to append to.
    """
    while True:
        year = input_int("Year (e.g 2020) 4-digit: ")
        if year is None:
            return
        if 1000 <= year <= 9999:   # must be exactly 4 digits
            break
        print("Year must be a 4-digit number (e.g. 2024)")
    
    # Month validation
    while True:
        month = input_int("Month (1 - 12): ")
        if month is None:
            return
        if 1 <= month <= 12:
            break
        print(" Month must be between (1 and 12)")

    rain_volume = input_float("Rain volume (mm/h): ")
    if rain_volume is None:
        return
    
    # Area Validation.
    while True:
        area = input_float("Area (m^2). ")
        if area is None:
            return
        if area > 0:
            break
        print("Area must be greater than 0")

    density = compute_density(rain_volume, area)
    print(f"\n density = {density} mm/h per m^2")

    # Confirmation before saving.
    if confirm("Save this entry?"):
        entry = RainEntry(
            year=year,
            month=month,
            rain_volume=rain_volume,
            area_m2=area,
            density=density,
            save_at=datetime.utcnow().isoformat()

        )
        append_entry(ws, entry)
        print("Entry saved.\n")
    else:
        print("Entry discarded.\n")


def calculator_only():
    """
    Simple rainfall density calculator.
    Does NOT save results to Google Sheets.
    Prompts for rain volume and area, then computes density.
    """
    rain_volume = input_float("Rain volume (mm/h): ")
    if rain_volume is None:
        return
    
    while True:
        area = input_float("Area (m^2): ")
        if area is None:
            return
        if area > 0:
            break
        print("Area must be greater than 0")
    
    density = compute_density(rain_volume, area)
    print(f"Density = {density} mm/h per m^2\n")


def show_entries(ws, limit=25):
    """
    Show rainfall records from the worksheet.
    limit (int): How many entries to show (default 25).
    """
    entries = get_entries(ws)
    if not entries:
        print("No entries found.\n")
        return

    print(f"\nShowing up to {limit} records:")
    count = 0
    for entry in entries:
        # Stop if we already showed 'limit' entries
        if count >= limit:
            break
        print(
            f"Year: {entry.year}, "
            f"Month: {entry.month}, "
            f"Rain Volume: {entry.rain_volume} mm/h, "
            f"Area: {entry.area_m2} m², "
            f"Density: {entry.density}, "
            f"Saved at: {entry.save_at}"
        )
        count += 1
    print("")


def average_last_12_months(ws):
    """
    Find the average rainfall density for the last 12 months.
    """
    # Get all entries from the sheet
    entries = get_entries(ws)
    if not entries:
        print("No entries found.\n")
        return

    # Sort all entries by year and month oldest to newset.
    entries.sort(key=lambda e: (e.year, e.month))

    # Go backwards and pick the last 12 different months
    last12_entries = []
    seen_months = set()

    for entry in reversed(entries):
        key = (entry.year, entry.month)
        if key not in seen_months:  # avoid duplicates
            seen_months.add(key)
            last12_entries.append(entry)

        if len(last12_entries) == 12:  # stop once we have 12 months
            break

    if len(last12_entries) < 12:
        print("Not enough data to calculate.\n")
        return

    # Calculate the average density
    total_density = sum(entry.density for entry in last12_entries)
    avg_density = total_density / len(last12_entries)

    print(
        f"Average density (last {len(last12_entries)} months): "
        f"{round(avg_density, 6)} mm/h per m^2\n"
    )


if __name__ == "__main__":
    ws = open_worksheet()

    print("=== Testing ====")
    average_last_12_months(ws)
