# tdd_versions/validator_refactor.py
# REFACTOR: same behaviour as GREEN, but cleaner + more maintainable.

from __future__ import annotations

from dataclasses import dataclass
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
_DATE_FMT = "%Y-%m-%d"
_TS_FMT = "%Y%m%d%H%M%S"


def validate_filename_pattern(filename: str) -> Tuple[bool, Optional[str]]:
    match = _FILENAME_RE.match(filename)
    if not match:
        return False, "Invalid filename format. Expected CLINICALDATA_YYYYMMDDHHMMSS(.csv)"

    ts = match.group(1)
    try:
        datetime.strptime(ts, _TS_FMT)
    except ValueError:
        return False, "Invalid timestamp in filename."

    return True, None


def validate_header(header_row: List[str]) -> List[str]:
    if header_row == EXPECTED_HEADER:
        return []
    return [f"Header mismatch. Expected: {EXPECTED_HEADER}"]


def validate_record(row: List[str], line_number: int, seen_records: Set[tuple]) -> List[str]:
    errors: List[str] = []

    if len(row) != len(EXPECTED_HEADER):
        return [f"Line {line_number}: Expected {len(EXPECTED_HEADER)} columns, got {len(row)}."]

    rec = _Record.from_row(row, line_number, errors)

    # Only do duplicate/date ordering checks if the core fields parsed OK
    if rec is not None:
        rec.check_date_order(errors)
        rec.check_duplicate(seen_records, errors)

    return errors


def _is_blank(s: str) -> bool:
    return s is None or str(s).strip() == ""


def _require(value: str, field: str, line: int, errors: List[str]) -> str:
    if _is_blank(value):
        errors.append(f"Line {line}: {field} is mandatory.")
    return str(value).strip()


def _parse_positive_int(value: str, field: str, line: int, errors: List[str]) -> Optional[int]:
    try:
        x = int(str(value).strip())
        if x <= 0:
            raise ValueError
        return x
    except Exception:
        errors.append(f"Line {line}: {field} must be a positive integer.")
        return None


def _parse_date(value: str, field: str, line: int, errors: List[str]) -> Optional[datetime]:
    try:
        return datetime.strptime(str(value).strip(), _DATE_FMT)
    except Exception:
        errors.append(f"Line {line}: {field} must be in YYYY-MM-DD format.")
        return None


@dataclass(frozen=True)
class _Record:
    patient_id: str
    trial_code: str
    drug_code: str
    dosage_mg: Optional[int]
    start_raw: str
    end_raw: str
    start_dt: Optional[datetime]
    end_dt: Optional[datetime]
    outcome: str
    side_effects: str
    analyst: str
    line_number: int

    @staticmethod
    def from_row(row: List[str], line: int, errors: List[str]) -> Optional["_Record"]:
        patient_id = _require(row[0], "PatientID", line, errors)
        trial_code = _require(row[1], "TrialCode", line, errors)
        drug_code = _require(row[2], "DrugCode", line, errors)

        dosage_mg = _parse_positive_int(row[3], "Dosage_mg", line, errors)

        start_raw = str(row[4]).strip()
        end_raw = str(row[5]).strip()
        start_dt = _parse_date(start_raw, "StartDate", line, errors)
        end_dt = _parse_date(end_raw, "EndDate", line, errors)

        outcome = _require(row[6], "Outcome", line, errors)
        side_effects = _require(row[7], "SideEffects", line, errors)
        analyst = _require(row[8], "Analyst", line, errors)

        # Even if errors exist, we still return a record so later checks can run
        return _Record(
            patient_id=patient_id,
            trial_code=trial_code,
            drug_code=drug_code,
            dosage_mg=dosage_mg,
            start_raw=start_raw,
            end_raw=end_raw,
            start_dt=start_dt,
            end_dt=end_dt,
            outcome=outcome,
            side_effects=side_effects,
            analyst=analyst,
            line_number=line,
        )

    def check_date_order(self, errors: List[str]) -> None:
        if self.start_dt and self.end_dt and self.end_dt < self.start_dt:
            errors.append(f"Line {self.line_number}: EndDate cannot be before StartDate.")

    def check_duplicate(self, seen_records: Set[tuple], errors: List[str]) -> None:
        key = (self.patient_id, self.trial_code, self.drug_code, self.start_raw, self.end_raw)
        if key in seen_records:
            errors.append(f"Line {self.line_number}: Duplicate record detected.")
        else:
            seen_records.add(key)
