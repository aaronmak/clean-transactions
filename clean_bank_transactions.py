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


def clean_dirty_row(row: List[Optional[str]]) -> Optional[List[str]]:
    # Rows without 9 columns are not needed because they
    # contain redundant data, such as summaries
    return row[0:9] if len(row) >= 9 else None


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
        clean_rows = [clean_dirty_row(row) for row in csv_reader]
        return [row for row in clean_rows if row]


def write_csv(filepath: str, rows: List[List[str]]):
    with open(filepath, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for r in rows:
            writer.writerow(r)


def generate_output_fp(csv_fp: str, rows: List[List[str]]):
    directory = Path(csv_fp).parent
    dates = get_dates(rows)
    min_date_str = date_to_str(min_date(dates))
    max_date_str = date_to_str(max_date(dates))
    output_file = f"{min_date_str}__{max_date_str}__bank-transactions.csv"

    return directory / output_file


cleaned_rows = clean_rows(filepath=csv_fp)
output_fp = generate_output_fp(csv_fp=csv_fp, rows=cleaned_rows)
print(f"Writing to {output_fp}...")
write_csv(filepath=output_fp, rows=cleaned_rows)
