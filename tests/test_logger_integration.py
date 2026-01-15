import os
from pathlib import Path
import re

import logger


def test_log_error_creates_error_report(tmp_path: Path, monkeypatch):
    # Make a fake Errors directory
    errors_dir = tmp_path / "Errors"

    # Force UUID to be predictable (so test is stable)
    monkeypatch.setattr(logger.UUIDService, "get_uuid", lambda self: "TEST-UUID-1234")

    logger.log_error("file.csv", "Some error happened", str(errors_dir))

    report_path = errors_dir / "error_report.log"
    assert report_path.exists()

    content = report_path.read_text(encoding="utf-8").strip()
    # Expected format: timestamp | guid | filename | message
    parts = [p.strip() for p in content.split("|")]
    assert len(parts) == 4
    assert parts[1] == "TEST-UUID-1234"
    assert parts[2] == "file.csv"
    assert parts[3] == "Some error happened"


def test_uuid_fallback_format(tmp_path: Path, monkeypatch):
    # Force API to fail so fallback is used
    monkeypatch.setattr(logger.UUIDService, "_get_uuid_from_api", lambda self: None)

    uuid_service = logger.UUIDService()
    uid = uuid_service.get_uuid()

    assert uid.startswith("LOCAL-")
    # LOCAL-YYYYMMDDHHMMSSffffff (basic check)
    assert re.match(r"^LOCAL-\d{20}$", uid) is not None
