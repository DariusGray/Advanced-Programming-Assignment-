from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple


EXPECTED_COLUMNS = [
    "PatientID",
    "TrialCode",
    "DrugCode",
    "Dosage_mg",
    "StartDate",
    "EndDate",
    "Outcome",
    "SideEffects",
    "Analyst",
]

ALLOWED_OUTCOMES = {"Improved", "No Change", "Worsened"}

_DATE_FMT = "%Y-%m-%d"
_TS_FMT = "%Y%m%d%H%M%S"


def validate_filename_pattern(filename: str) -> Tuple[bool, str | None]:
    """
    Validate filename: CLINICALDATA_YYYYMMDDHHMMSS.csv
    """
    base = filename
    if base.lower().endswith(".csv"):
        base = base[:-4]  # strip .csv

    if not base.startswith("CLINICALDATA_"):
        return False, "Filename does not start with 'CLINICALDATA_'"

    timestamp_part = base[len("CLINICALDATA_") :]

    if len(timestamp_part) != 14 or not timestamp_part.isdigit():
        return False, "Filename timestamp must be 14 digits (YYYYMMDDHHMMSS)"

    try:
        datetime.strptime(timestamp_part, _TS_FMT)
    except ValueError:
        return False, "Filename timestamp is not a valid date/time"

    return True, None


def validate_header(header: List[str]) -> List[str]:
    errors: List[str] = []

    if len(header) != len(EXPECTED_COLUMNS):
        errors.append(
            f"Header has {len(header)} fields; expected {len(EXPECTED_COLUMNS)}"
        )
        return errors

    # Normalize whitespace
    normalized = [h.strip() for h in header]

    if normalized != EXPECTED_COLUMNS:
        errors.append(f"Header mismatch. Expected: {EXPECTED_COLUMNS}, got: {normalized}")

    return errors


def _parse_positive_int(value: str) -> int | None:
    try:
        num = int(value)
        if num <= 0:
            return None
        return num
    except Exception:
        return None


def _parse_date(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, _DATE_FMT)
    except Exception:
        return None


def _is_empty(value: str) -> bool:
    return value.strip() == ""


@dataclass(frozen=True)
class _ParsedRow:
    row: List[str]
    line_number: int

    patient_id: str
    trial_code: str
    drug_code: str
    dosage_str: str
    start_str: str
    end_str: str
    outcome: str
    side_effects: str
    analyst: str

    @staticmethod
    def from_row(row: List[str], line_number: int) -> "_ParsedRow":
        # Strip whitespace exactly like your original implementation
        stripped = [cell.strip() for cell in row]
        return _ParsedRow(
            row=stripped,
            line_number=line_number,
            patient_id=stripped[0],
            trial_code=stripped[1],
            drug_code=stripped[2],
            dosage_str=stripped[3],
            start_str=stripped[4],
            end_str=stripped[5],
            outcome=stripped[6],
            side_effects=stripped[7],
            analyst=stripped[8],
        )


def validate_record(
    row: List[str],
    line_number: int,
    seen_records: set[tuple],
) -> List[str]:
    """
    Validate a single CSV row according to the rules.
    Returns a list of error messages for that row (may be empty).
    """
    errors: List[str] = []

    if len(row) != len(EXPECTED_COLUMNS):
        errors.append(
            f"Line {line_number}: Expected {len(EXPECTED_COLUMNS)} fields, got {len(row)}"
        )
        return errors  # other checks depend on correct length

    parsed = _ParsedRow.from_row(row, line_number)

    # Mandatory fields (keep your exact messages)
    if _is_empty(parsed.patient_id):
        errors.append(f"Line {line_number}: PatientID is mandatory and cannot be empty")
    if _is_empty(parsed.trial_code):
        errors.append(f"Line {line_number}: TrialCode is mandatory and cannot be empty")
    if _is_empty(parsed.drug_code):
        errors.append(f"Line {line_number}: DrugCode is mandatory and cannot be empty")
    if _is_empty(parsed.outcome):
        errors.append(f"Line {line_number}: Outcome is mandatory and cannot be empty")
    if _is_empty(parsed.side_effects):
        errors.append(f"Line {line_number}: SideEffects is mandatory and cannot be empty")
    if _is_empty(parsed.analyst):
        errors.append(f"Line {line_number}: Analyst is mandatory and cannot be empty")

    # Dosage positive integer (keep exact message + include value)
    if _parse_positive_int(parsed.dosage_str) is None:
        errors.append(
            f"Line {line_number}: Dosage_mg must be a positive integer, got '{parsed.dosage_str}'"
        )

    # Dates and chronological integrity (keep exact messages + values)
    start_date = _parse_date(parsed.start_str)
    end_date = _parse_date(parsed.end_str)

    if start_date is None:
        errors.append(
            f"Line {line_number}: StartDate '{parsed.start_str}' is not in YYYY-MM-DD format"
        )
    if end_date is None:
        errors.append(
            f"Line {line_number}: EndDate '{parsed.end_str}' is not in YYYY-MM-DD format"
        )
    if start_date is not None and end_date is not None and end_date < start_date:
        errors.append(
            f"Line {line_number}: EndDate '{parsed.end_str}' is before StartDate '{parsed.start_str}'"
        )

    # Outcome value check (keep exact message format)
    if parsed.outcome not in ALLOWED_OUTCOMES:
        errors.append(
            f"Line {line_number}: Outcome '{parsed.outcome}' is invalid. "
            f"Allowed values: {sorted(ALLOWED_OUTCOMES)}"
        )

    # Duplicate detection (keep: tuple(row) AFTER stripping)
    record_key = tuple(parsed.row)
    if record_key in seen_records:
        errors.append(f"Line {line_number}: Duplicate record found in file")
    else:
        seen_records.add(record_key)

    return errors


def validate_csv_file(filename: str, filepath: str) -> Tuple[bool, List[str]]:
    """
    Full validation of a CSV file.
    Returns (is_valid, errors_list).
    """
    all_errors: List[str] = []

    # Filename pattern
    ok, msg = validate_filename_pattern(filename)
    if not ok and msg:
        all_errors.append(f"Filename error: {msg}")

    # CSV content validation
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            try:
                reader = csv.reader(f)
                try:
                    header = next(reader)
                except StopIteration:
                    all_errors.append("File is empty (no header row found)")
                    return False, all_errors

                # Header validation
                header_errors = validate_header(header)
                all_errors.extend(header_errors)

                seen_records: set[tuple] = set()

                for line_number, row in enumerate(reader, start=2):
                    # Skip completely empty lines
                    if not row or all(cell.strip() == "" for cell in row):
                        all_errors.append(
                            f"Line {line_number}: Empty or malformed row encountered"
                        )
                        continue

                    row_errors = validate_record(row, line_number, seen_records)
                    all_errors.extend(row_errors)

            except csv.Error as e:
                all_errors.append(f"Malformed CSV syntax: {e}")

    except FileNotFoundError:
        all_errors.append("Local file not found for validation")
    except Exception as e:
        all_errors.append(f"Unexpected error while reading file: {e}")

    is_valid = len(all_errors) == 0
    return is_valid, all_errors