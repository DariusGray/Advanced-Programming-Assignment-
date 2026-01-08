# tdd_versions/validator_green.py
# GREEN: minimal implementation to satisfy the tests.

from __future__ import annotations

from datetime import datetime
import re
from typing import List, Optional, Set, Tuple


EXPECTED_HEADER = [
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


_FILENAME_RE = re.compile(r"^CLINICALDATA_(\d{14})(?:\.csv)?$")


def validate_filename_pattern(filename: str) -> Tuple[bool, Optional[str]]:
    m = _FILENAME_RE.match(filename)
    if not m:
        return False, "Invalid filename format. Expected CLINICALDATA_YYYYMMDDHHMMSS(.csv)"
    ts = m.group(1)
    try:
        datetime.strptime(ts, "%Y%m%d%H%M%S")
    except ValueError:
        return False, "Invalid timestamp in filename."
    return True, None


def validate_header(header_row: List[str]) -> List[str]:
    if header_row == EXPECTED_HEADER:
        return []
    return [f"Header mismatch. Expected: {EXPECTED_HEADER}"]


def _is_empty(value: str) -> bool:
    return value is None or str(value).strip() == ""


def _parse_date(date_str: str, field: str, errors: List[str], line_number: int) -> Optional[datetime]:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        errors.append(f"Line {line_number}: {field} must be in YYYY-MM-DD format.")
        return None


def validate_record(
    row: List[str],
    line_number: int,
    seen_records: Set[tuple],
) -> List[str]:
    errors: List[str] = []

    if len(row) != 9:
        return [f"Line {line_number}: Expected 9 columns, got {len(row)}."]

    patient_id, trial_code, drug_code, dosage, start_date, end_date, outcome, side_effects, analyst = row

    # Mandatory fields
    if _is_empty(patient_id):
        errors.append(f"Line {line_number}: PatientID is mandatory.")
    if _is_empty(trial_code):
        errors.append(f"Line {line_number}: TrialCode is mandatory.")
    if _is_empty(drug_code):
        errors.append(f"Line {line_number}: DrugCode is mandatory.")
    if _is_empty(outcome):
        errors.append(f"Line {line_number}: Outcome is mandatory.")
    if _is_empty(side_effects):
        errors.append(f"Line {line_number}: SideEffects is mandatory.")
    if _is_empty(analyst):
        errors.append(f"Line {line_number}: Analyst is mandatory.")

    # Dosage: positive integer
    try:
        d = int(str(dosage).strip())
        if d <= 0:
            raise ValueError
    except Exception:
        errors.append(f"Line {line_number}: Dosage_mg must be a positive integer.")

    # Dates
    start_dt = _parse_date(str(start_date).strip(), "StartDate", errors, line_number)
    end_dt = _parse_date(str(end_date).strip(), "EndDate", errors, line_number)

    if start_dt and end_dt and end_dt < start_dt:
        errors.append(f"Line {line_number}: EndDate cannot be before StartDate.")

    # Duplicate check
    key = (patient_id, trial_code, drug_code, start_date, end_date)
    if key in seen_records:
        errors.append(f"Line {line_number}: Duplicate record detected.")
    else:
        seen_records.add(key)

    return errors
