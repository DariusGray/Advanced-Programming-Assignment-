# tdd_versions/validator_red.py
# RED: just enough structure for imports; everything fails meaningfully.

from typing import List, Optional, Set, Tuple


def validate_filename_pattern(filename: str) -> Tuple[bool, Optional[str]]:
    raise NotImplementedError("TDD RED: not implemented yet")


def validate_header(header_row: List[str]) -> List[str]:
    raise NotImplementedError("TDD RED: not implemented yet")


def validate_record(
    row: List[str],
    line_number: int,
    seen_records: Set[tuple],
) -> List[str]:
    raise NotImplementedError("TDD RED: not implemented yet")
