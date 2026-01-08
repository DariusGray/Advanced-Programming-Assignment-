from validator import validate_filename_pattern, validate_header, EXPECTED_COLUMNS

def test_valid_filename():
    ok, msg = validate_filename_pattern("CLINICALDATA_20250101123045.csv")
    assert ok is True
    assert msg is None

def test_invalid_filename_prefix():
    ok, msg = validate_filename_pattern("BAD_20250101123045.csv")
    assert ok is False

def test_header_ok():
    errors = validate_header(EXPECTED_COLUMNS)
    assert errors == []
