"""
Automation Script 2: File Validation Automation

Purpose:
- Automatically generate GOOD and BAD CSV samples for repeatable testing
- Run the real validator.py logic against those samples
"""

from __future__ import annotations

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import csv
from datetime import datetime, timedelta
from typing import List, Tuple

from validator import validate_csv_file, EXPECTED_COLUMNS


def _timestamp_name(dt: datetime) -> str:
    # STRICTLY follows: CLINICALDATA_YYYYMMDDHHMMSS.csv
    ts = dt.strftime("%Y%m%d%H%M%S")
    return f"CLINICALDATA_{ts}.csv"


def _write_csv(path: str, header: List[str], rows: List[List[str]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def generate_good_file(out_dir: str) -> Tuple[str, str]:
    filename = _timestamp_name(datetime.now())
    path = os.path.join(out_dir, filename)

    today = datetime.now().date()
    start = today.isoformat()
    end = (today + timedelta(days=7)).isoformat()

    rows = [
        ["P001", "T100", "D200", "50", start, end, "Improved", "None", "AnalystA"],
        ["P002", "T100", "D200", "25", start, end, "No Change", "Nausea", "AnalystB"],
        ["P003", "T101", "D201", "10", start, end, "Worsened", "Headache", "AnalystC"],
    ]

    _write_csv(path, EXPECTED_COLUMNS, rows)
    return filename, path


def generate_bad_file(out_dir: str) -> Tuple[str, str]:
    # Offset by 1 second to avoid filename collision
    filename = _timestamp_name(datetime.now() + timedelta(seconds=1))
    path = os.path.join(out_dir, filename)

    today = datetime.now().date()
    start = today.isoformat()
    end_before = (today - timedelta(days=2)).isoformat()

    rows = [
        ["", "T100", "D200", "-10", start, end_before, "Improved", "None", "AnalystA"],
        ["P010", "T100", "D200", "20", "2025/01/01", start, "No Change", "None", "AnalystB"],
        ["P011", "T100", "D200", "10", start, start, "Better", "None", "AnalystC"],
        ["P011", "T100", "D200", "10", start, start, "Better", "None", "AnalystC"],
    ]

    _write_csv(path, EXPECTED_COLUMNS, rows)
    return filename, path


def run_validation(label: str, filename: str, path: str) -> None:
    is_valid, errors = validate_csv_file(filename, path)
    print(f"\n--- Validation Result ({label}) ---")
    print(f"Filename: {filename}")
    print(f"Path: {path}")
    print(f"Valid: {is_valid}")
    if not is_valid:
        print(f"Errors ({len(errors)}):")
        for msg in errors[:12]:
            print(f" - {msg}")
        if len(errors) > 12:
            print(f" ... ({len(errors) - 12} more)")


def main() -> None:
    out_dir = os.path.join(os.getcwd(), "generated_test_data")
    print("=== Validation Automation ===")
    print(f"Output folder: {out_dir}")

    good_name, good_path = generate_good_file(out_dir)
    bad_name, bad_path = generate_bad_file(out_dir)

    print(f"\nGenerated GOOD file: {good_name}")
    print(f"Generated BAD file : {bad_name}")

    run_validation("GOOD", good_name, good_path)
    run_validation("BAD", bad_name, bad_path)

    print("\nDone. You can upload these files to your FTP server if needed.")


if __name__ == "__main__":
    main()
