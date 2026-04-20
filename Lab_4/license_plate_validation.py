import re
import sys

RTO_DATA = {
    "AN": {str(i).zfill(2) for i in range(1, 3)},
    "AP": {str(i).zfill(2) for i in range(1, 40)},
    "AR": {str(i).zfill(2) for i in range(1, 20)},
    "AS": {str(i).zfill(2) for i in range(1, 35)},
    "BR": {str(i).zfill(2) for i in range(1, 60)},
    "CG": {str(i).zfill(2) for i in range(1, 30)},
    "CH": {"01"},
    "DD": {"01", "02"},
    "DL": {str(i).zfill(2) for i in range(1, 15)},
    "DN": {"01"},
    "GA": {str(i).zfill(2) for i in range(1, 15)},
    "GJ": {str(i).zfill(2) for i in range(1, 40)},
    "HR": {str(i).zfill(2) for i in range(1, 100)},
    "HP": {str(i).zfill(2) for i in range(1, 100)},
    "JH": {str(i).zfill(2) for i in range(1, 30)},
    "JK": {str(i).zfill(2) for i in range(1, 25)},
    "KA": {str(i).zfill(2) for i in range(1, 70)},
    "KL": {str(i).zfill(2) for i in range(1, 90)},
    "LA": {"01"},
    "LD": {"01"},
    "MH": {str(i).zfill(2) for i in range(1, 100)},
    "ML": {str(i).zfill(2) for i in range(1, 15)},
    "MN": {str(i).zfill(2) for i in range(1, 10)},
    "MP": {str(i).zfill(2) for i in range(1, 80)},
    "MZ": {str(i).zfill(2) for i in range(1, 10)},
    "NL": {str(i).zfill(2) for i in range(1, 10)},
    "OD": {str(i).zfill(2) for i in range(1, 40)},
    "PB": {str(i).zfill(2) for i in range(1, 100)},
    "PY": {str(i).zfill(2) for i in range(1, 4)},
    "RJ": {str(i).zfill(2) for i in range(1, 100)},
    "SK": {str(i).zfill(2) for i in range(1, 10)},
    "TN": {str(i).zfill(2) for i in range(1, 100)},
    "TS": {str(i).zfill(2) for i in range(1, 40)},
    "TR": {str(i).zfill(2) for i in range(1, 10)},
    "UK": {str(i).zfill(2) for i in range(1, 30)},
    "UP": {str(i).zfill(2) for i in range(1, 100)},
    "WB": {str(i).zfill(2) for i in range(1, 100)},
}

def is_valid_indian_plate(plate: str) -> bool:
    plate = plate.replace(" ", "").upper()

    pattern = r'^([A-Z]{2})([0-9]{2})([A-Z]{1,3})([0-9]{1,4})$'
    match = re.fullmatch(pattern, plate)

    if not match:
        return False

    state, district, series, number = match.groups()

    if state not in RTO_DATA:
        return False

    if district not in RTO_DATA[state]:
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: license_plate_validator.py <numbers.txt>")
        sys.exit()

    numbers : set[str] = set()
    with open(sys.argv[1], "r") as test_file:
        test = test_file.readlines()
        for i in test:
            numbers.add(i.strip())

    for i in numbers:
        print(i, " --> ", "Valid" if is_valid_indian_plate(i) else "Invalid")