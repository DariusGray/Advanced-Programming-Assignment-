# validator.py
import re
from datetime import datetime


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


def validate_filename_pattern(filename):
    pattern = r"^CLINICALDATA_(\d{14})(\.csv)?$"
    m = re.match(pattern, filename)

    if not m:
        return False, "Invalid filename format."

    timestamp = m.group(1)
    try:
        datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    except ValueError:
        return False, "Invalid date in filename."

    return True, ""


def validate_header(header):
    errors = []
    if header != EXPECTED_HEADER:
        errors.append("Header mismatch.")
    return errors


def validate_record(row, row_num, seen):
    errors = []

    if len(row) != 9:
        errors.append(f"Row {row_num}: Expected 9 columns.")
        return errors

    (
        patient_id,
        trial_code,
        drug_code,
        dosage,
        start_date,
        end_date,
        outcome,
        side_effects,
        analyst,
    ) = row

    # Mandatory fields
    if not patient_id:
        errors.append("PatientID is mandatory.")
    if not trial_code:
        errors.append("TrialCode is mandatory.")
    if not drug_code:
        errors.append("DrugCode is mandatory.")
    if not outcome:
        errors.append("Outcome is mandatory.")
    if not side_effects:
        errors.append("SideEffects is mandatory.")
    if not analyst:
        errors.append("Analyst is mandatory.")

    # Dosage validation
    if not dosage.isdigit() or int(dosage) <= 0:
        errors.append("Dosage_mg must be a positive integer.")

    # Date validation
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    except:
        errors.append("StartDate is invalid.")
        start = None

    try:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        errors.append("EndDate is invalid.")
        end = None

    if start and end and end < start:
        errors.append("EndDate cannot be before StartDate.")

    # Duplicate check
    key = tuple(row)
    if key in seen:
        errors.append("Duplicate record detected.")
    else:
        seen.add(key)

    return errors
