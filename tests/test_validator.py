# import csv
# from pathlib import Path

# import pytest

# from clinical_data_validator import validator



# def test_validate_filename_pattern_valid():
#     ok, msg = validator.validate_filename_pattern("CLINICALDATA_20251212120000.csv")
#     assert ok is True
#     assert msg is None


# def test_validate_filename_pattern_wrong_prefix():
#     ok, msg = validator.validate_filename_pattern("INVALID_20251212120000.csv")
#     assert ok is False
#     assert msg == "Filename does not start with 'CLINICALDATA_'"


# def test_validate_filename_pattern_bad_length():
#     ok, msg = validator.validate_filename_pattern("CLINICALDATA_20251212.csv")
#     assert ok is False
#     assert msg == "Filename timestamp must be 14 digits (YYYYMMDDHHMMSS)"


# def test_validate_filename_pattern_invalid_datetime():
#     # Month 13 is invalid
#     ok, msg = validator.validate_filename_pattern("CLINICALDATA_20251301120000.csv")
#     assert ok is False
#     assert msg == "Filename timestamp is not a valid date/time"


# def test_validate_header_exact_match():
#     errors = validator.validate_header(validator.EXPECTED_COLUMNS.copy())
#     assert errors == []


# def test_validate_header_strips_whitespace():
#     header = [h + "   " for h in validator.EXPECTED_COLUMNS]
#     errors = validator.validate_header(header)
#     assert errors == []


# def test_validate_header_wrong_count():
#     errors = validator.validate_header(["A", "B"])
#     assert errors == ["Header has 2 fields; expected 9"]


# def test_validate_header_mismatch_same_length():
#     bad = validator.EXPECTED_COLUMNS.copy()
#     bad[-1] = "AnalystName"
#     errors = validator.validate_header(bad)
#     assert len(errors) == 1
#     assert errors[0].startswith("Header mismatch. Expected:")


# def _good_row_list():
#     # Must be exactly 9 fields, in EXPECTED_COLUMNS order
#     return [
#         "P4001",
#         "TR2025-A",
#         "DRG-123",
#         "10",
#         "2025-07-01",
#         "2025-07-10",
#         "Improved",
#         "Fatigue",
#         "Dr. Tan",
#     ]


# def test_validate_record_valid_row_no_errors():
#     seen = set()
#     errors = validator.validate_record(_good_row_list(), line_number=2, seen_records=seen)
#     assert errors == []
#     # Should store record_key into seen
#     assert len(seen) == 1


# def test_validate_record_wrong_field_count():
#     seen = set()
#     row = ["A", "B"]
#     errors = validator.validate_record(row, line_number=2, seen_records=seen)
#     assert errors == ["Line 2: Expected 9 fields, got 2"]


# def test_validate_record_mandatory_fields_patient_trial_drug():
#     seen = set()
#     row = _good_row_list()
#     row[0] = ""  # PatientID
#     row[1] = ""  # TrialCode
#     row[2] = ""  # DrugCode
#     errors = validator.validate_record(row, line_number=5, seen_records=seen)

#     joined = "\n".join(errors)
#     assert "Line 5: PatientID is mandatory and cannot be empty" in joined
#     assert "Line 5: TrialCode is mandatory and cannot be empty" in joined
#     assert "Line 5: DrugCode is mandatory and cannot be empty" in joined


# def test_validate_record_mandatory_fields_outcome_sideeffects_analyst():
#     seen = set()
#     row = _good_row_list()
#     row[6] = ""  # Outcome
#     row[7] = ""  # SideEffects
#     row[8] = ""  # Analyst
#     errors = validator.validate_record(row, line_number=6, seen_records=seen)

#     joined = "\n".join(errors)
#     assert "Line 6: Outcome is mandatory and cannot be empty" in joined
#     assert "Line 6: SideEffects is mandatory and cannot be empty" in joined
#     assert "Line 6: Analyst is mandatory and cannot be empty" in joined


# def test_validate_record_dosage_must_be_positive_int():
#     seen = set()
#     row = _good_row_list()
#     row[3] = "twenty"
#     errors = validator.validate_record(row, line_number=3, seen_records=seen)
#     assert any("Dosage_mg must be a positive integer" in e for e in errors)


# def test_validate_record_start_date_format():
#     seen = set()
#     row = _good_row_list()
#     row[4] = "07/01/2025"
#     errors = validator.validate_record(row, line_number=3, seen_records=seen)
#     assert "Line 3: StartDate '07/01/2025' is not in YYYY-MM-DD format" in errors


# def test_validate_record_end_date_format():
#     seen = set()
#     row = _good_row_list()
#     row[5] = "2025/07/10"
#     errors = validator.validate_record(row, line_number=3, seen_records=seen)
#     assert "Line 3: EndDate '2025/07/10' is not in YYYY-MM-DD format" in errors


# def test_validate_record_end_before_start():
#     seen = set()
#     row = _good_row_list()
#     row[4] = "2025-07-20"
#     row[5] = "2025-07-05"
#     errors = validator.validate_record(row, line_number=4, seen_records=seen)
#     assert "Line 4: EndDate '2025-07-05' is before StartDate '2025-07-20'" in errors


# def test_validate_record_invalid_outcome_value():
#     seen = set()
#     row = _good_row_list()
#     row[6] = "Better"
#     errors = validator.validate_record(row, line_number=9, seen_records=seen)
#     # Exact string includes allowed values list
#     assert any("Outcome 'Better' is invalid." in e for e in errors)


# def test_validate_record_duplicate_detection():
#     seen = set()
#     row = _good_row_list()
#     e1 = validator.validate_record(row, line_number=2, seen_records=seen)
#     e2 = validator.validate_record(row, line_number=3, seen_records=seen)

#     assert e1 == []
#     assert "Line 3: Duplicate record found in file" in e2


# def test_validate_csv_file_valid(tmp_path: Path):
#     filename = "CLINICALDATA_20251212120000.csv"
#     fpath = tmp_path / filename

#     with fpath.open("w", newline="", encoding="utf-8") as f:
#         w = csv.writer(f)
#         w.writerow(validator.EXPECTED_COLUMNS)
#         w.writerow(_good_row_list())

#     is_valid, errors = validator.validate_csv_file(filename, str(fpath))
#     assert is_valid is True
#     assert errors == []


# def test_validate_csv_file_empty(tmp_path: Path):
#     filename = "CLINICALDATA_20251212120000.csv"
#     fpath = tmp_path / filename
#     fpath.write_text("", encoding="utf-8")

#     is_valid, errors = validator.validate_csv_file(filename, str(fpath))
#     assert is_valid is False
#     assert "File is empty (no header row found)" in errors


# def test_validate_csv_file_skips_blank_line_and_reports(tmp_path: Path):
#     filename = "CLINICALDATA_20251212120000.csv"
#     fpath = tmp_path / filename

#     with fpath.open("w", newline="", encoding="utf-8") as f:
#         f.write(",".join(validator.EXPECTED_COLUMNS) + "\n")
#         f.write("\n")  # blank line -> should be reported as empty/malformed
#         f.write(",".join(_good_row_list()) + "\n")

#     is_valid, errors = validator.validate_csv_file(filename, str(fpath))
#     assert is_valid is False
#     assert any("Empty or malformed row encountered" in e for e in errors)


# def test_validate_csv_file_bad_header(tmp_path: Path):
#     filename = "CLINICALDATA_20251212120000.csv"
#     fpath = tmp_path / filename

#     with fpath.open("w", newline="", encoding="utf-8") as f:
#         w = csv.writer(f)
#         w.writerow(["A", "B", "C"])
#         w.writerow(["1", "2", "3"])

#     is_valid, errors = validator.validate_csv_file(filename, str(fpath))
#     assert is_valid is False
#     assert "Header has 3 fields; expected 9" in errors


# def test_validate_csv_file_filename_error_added(tmp_path: Path):
#     # Wrong prefix triggers filename error, even if content is valid
#     filename = "WRONG_20251212120000.csv"
#     fpath = tmp_path / filename

#     with fpath.open("w", newline="", encoding="utf-8") as f:
#         w = csv.writer(f)
#         w.writerow(validator.EXPECTED_COLUMNS)
#         w.writerow(_good_row_list())

#     is_valid, errors = validator.validate_csv_file(filename, str(fpath))
#     assert is_valid is False
#     assert any(e.startswith("Filename error:") for e in errors)
