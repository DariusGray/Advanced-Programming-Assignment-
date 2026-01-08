# from pathlib import Path

# import logger


# def test_log_error_creates_error_report_and_writes_line(tmp_path: Path):
#     errors_dir = tmp_path / "Errors"

#     logger.log_error("file.csv", "Some error message", str(errors_dir))

#     report = errors_dir / "error_report.log"
#     assert report.exists()

#     content = report.read_text(encoding="utf-8").strip()
#     # Expected format: timestamp | UUID4 | filename | message
#     parts = [p.strip() for p in content.split("|")]
#     assert len(parts) == 4
#     assert parts[2] == "file.csv"
#     assert parts[3] == "Some error message"


# def test_log_errors_writes_multiple_lines(tmp_path: Path):
#     errors_dir = tmp_path / "Errors"

#     logger.log_errors("a.csv", ["E1", "E2"], str(errors_dir))

#     report = errors_dir / "error_report.log"
#     content = report.read_text(encoding="utf-8").strip().splitlines()
#     assert len(content) == 2
#     assert content[0].endswith(" | a.csv | E1")
#     assert content[1].endswith(" | a.csv | E2")


# def test_has_been_processed_and_mark_processed(tmp_path: Path, monkeypatch):
#     processed_log = tmp_path / "processed_files.log"

#     # Patch the imported constant inside logger module
#     monkeypatch.setattr(logger, "PROCESSED_LOG_PATH", str(processed_log))

#     assert logger.has_been_processed("A.csv") is False

#     logger.mark_processed("A.csv")
#     assert logger.has_been_processed("A.csv") is True

#     # Another file should still be False
#     assert logger.has_been_processed("B.csv") is False
