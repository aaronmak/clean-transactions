
import csv
import argparse
from pathlib import Path
from typing import Optional, List
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("csv_filepath", help="filepath of CSV file to clean")
args = parser.parse_args()

csv_fp = args.csv_filepath
print(f"Reading {csv_fp}...")


def remove_dollar_sign(data: str):
    return data.replace("S$", "")


def add_sign(data: str):
    if data.endswith(" cr"):
        return data.replace(" cr", "")
    else:
        return f"-{data}"


def clean_amount_data(rows: List[List[str]]) -> List[List[str]]:
    for row in rows:
        row[2] = remove_dollar_sign(row[2])
        row[2] = add_sign(row[2])

    return rows


def remove_empty_row(row: List[Optional[str]]) -> Optional[List[str]]:
    # Remove all row items if there is one empty string because we expect
    # all columns to be filled
    for d in row:
        if d == "":
            row.clear()

    # Only include rows where all 3 columns have data
    return row if len(row) == 3 else None


def get_dates(rows: List[List[str]]) -> str:
    dates = []
    for row in rows:
        try:
            # Transaction Date is 1st column
            d = datetime.strptime(row[0], "%d %b %Y")
            dates.append(d)
        except ValueError:
            pass
    return dates


def max_date(dates: List[datetime]) -> datetime:
    return max(dates)


def min_date(dates: List[datetime]) -> datetime:
    return min(dates)


def date_to_str(d: datetime) -> str:
    return d.strftime('%Y-%m-%d')


def clean_rows(filepath: str):
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = [row for row in csv_reader if remove_empty_row(row)]

        header_row = rows[0]
        body_rows = clean_amount_data(rows[1:])
        return [header_row] + body_rows


def write_csv(filepath: str, rows: List[List[str]]):
    with open(filepath, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='unix')
        writer.writerows(rows)


def generate_output_fp(csv_fp: str, rows: List[List[str]]):
    directory = Path(csv_fp).parent
    dates = get_dates(rows)
    min_date_str = date_to_str(min_date(dates))
    max_date_str = date_to_str(max_date(dates))
    output_file = f"{min_date_str}__{max_date_str}__card-transactions.csv"

    return directory / output_file


cleaned_rows = clean_rows(filepath=csv_fp)
output_fp = generate_output_fp(csv_fp=csv_fp, rows=cleaned_rows)
output_fp.unlink(missing_ok=True)
print(f"Writing to {output_fp}...")
write_csv(filepath=output_fp, rows=cleaned_rows)


print()
print(f"{output_fp} created")
