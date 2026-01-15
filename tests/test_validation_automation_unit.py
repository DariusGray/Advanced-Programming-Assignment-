import os
import re
from pathlib import Path

from scripts.validation_automation import (
    _timestamp_name,
    generate_good_file,
    generate_bad_file,
)

# Import expected header to verify correct schema
from validator import EXPECTED_COLUMNS


def test_timestamp_name_format():
    name = _timestamp_name(__import__("datetime").datetime(2025, 1, 2, 3, 4, 5))
    # Must match CLINICALDATA_YYYYMMDDHHMMSS.csv
    assert re.match(r"^CLINICALDATA_\d{14}\.csv$", name) is not None


def test_generate_good_file_creates_csv(tmp_path: Path):
    filename, path = generate_good_file(str(tmp_path))

    assert filename.endswith(".csv")
    assert os.path.exists(path)

    # Read back and check header + row count
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # First line should be header
    header = lines[0].split(",")
    assert header == EXPECTED_COLUMNS

    # Good file should have 3 rows 
    assert len(lines) == 1 + 3


def test_generate_bad_file_creates_csv(tmp_path: Path):
    filename, path = generate_bad_file(str(tmp_path))

    assert filename.endswith(".csv")
    assert os.path.exists(path)

    # Ensure header is correct
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    assert first_line.split(",") == EXPECTED_COLUMNS

    # Bad file should have 4 rows
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    assert len(lines) == 1 + 4
