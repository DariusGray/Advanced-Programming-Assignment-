# # tests/test_validator.py
# import pytest
# from validator import validate_filename_pattern, validate_header, validate_record


# @pytest.fixture
# def expected_header():
#     return [
#         "PatientID",
#         "TrialCode",
#         "DrugCode",
#         "Dosage_mg",
#         "StartDate",
#         "EndDate",
#         "Outcome",
#         "SideEffects",
#         "Analyst",
#     ]


# @pytest.fixture
# def row_factory():
#     def make(**overrides):
#         base = {
#             "PatientID": "P001",
#             "TrialCode": "TRIAL01",
#             "DrugCode": "DRUG01",
#             "Dosage_mg": "10",
#             "StartDate": "2025-01-01",
#             "EndDate": "2025-01-10",
#             "Outcome": "Improved",
#             "SideEffects": "None",
#             "Analyst": "Alice",
#         }
#         base.update(overrides)
#         return [
#             base["PatientID"],
#             base["TrialCode"],
#             base["DrugCode"],
#             base["Dosage_mg"],
#             base["StartDate"],
#             base["EndDate"],
#             base["Outcome"],
#             base["SideEffects"],
#             base["Analyst"],
#         ]
#     return make


# @pytest.mark.parametrize(
#     "filename, ok_expected",
#     [
#         ("CLINICALDATA_20250101123045.csv", True),
#         ("CLINICALDATA_20250101123045", True),
#         ("CLINICALDATA_2025010112304.csv", False),    # 13 digits
#         ("CLINICALDATA_2025AA01123045.csv", False),   # non-digit
#         ("DATA_20250101123045.csv", False),           # wrong prefix
#         ("CLINICALDATA_20251301123045.csv", False),   # invalid month
#     ],
# )
# def test_validate_filename_pattern(filename, ok_expected):
#     ok, _ = validate_filename_pattern(filename)
#     assert ok is ok_expected


# def test_validate_header_ok(expected_header):
#     assert validate_header(expected_header) == []


# def test_validate_header_mismatch(expected_header):
#     wrong = expected_header.copy()
#     wrong[0] = "PatientId"
#     errors = validate_header(wrong)
#     assert errors
#     assert "Header mismatch" in errors[0]


# def test_validate_record_wrong_column_count(row_factory):
#     seen = set()
#     row = row_factory()
#     row.pop()  # 8 columns
#     errs = validate_record(row, 2, seen)
#     assert errs
#     assert "Expected" in errs[0]


# @pytest.mark.parametrize(
#     "field, expected_msg",
#     [
#         ("PatientID", "PatientID is mandatory."),
#         ("TrialCode", "TrialCode is mandatory."),
#         ("DrugCode", "DrugCode is mandatory."),
#         ("Outcome", "Outcome is mandatory."),
#         ("SideEffects", "SideEffects is mandatory."),
#         ("Analyst", "Analyst is mandatory."),
#     ],
# )
# def test_validate_record_mandatory_fields(row_factory, field, expected_msg):
#     seen = set()
#     row = row_factory(**{field: ""})
#     errs = validate_record(row, 2, seen)
#     assert any(expected_msg in e for e in errs)


# @pytest.mark.parametrize("dosage", ["0", "-1", "abc", "1.2", ""])
# def test_validate_record_bad_dosage(row_factory, dosage):
#     seen = set()
#     row = row_factory(Dosage_mg=dosage)
#     errs = validate_record(row, 2, seen)
#     assert any("Dosage_mg must be a positive integer." in e for e in errs)


# @pytest.mark.parametrize(
#     "start, end, expected_substring",
#     [
#         ("2025-01-xx", "2025-01-10", "StartDate"),
#         ("2025-01-01", "2025-01-xx", "EndDate"),
#         ("2025-01-10", "2025-01-01", "EndDate cannot be before StartDate"),
#     ],
# )
# def test_validate_record_dates(row_factory, start, end, expected_substring):
#     seen = set()
#     row = row_factory(StartDate=start, EndDate=end)
#     errs = validate_record(row, 2, seen)
#     assert any(expected_substring in e for e in errs)


# def test_validate_record_duplicate(row_factory):
#     seen = set()
#     row = row_factory()
#     assert validate_record(row, 2, seen) == []
#     errs = validate_record(row, 3, seen)
#     assert any("Duplicate record detected." in e for e in errs)
