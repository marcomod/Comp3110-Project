"""Starter for tracking lines between two versions of a text file."""

import argparse
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


@dataclass
class DiffResult:
    """Matches and unmatched lines, using 1-based line numbers."""

    matches: list[tuple[int, int]]
    unmatched_old: list[int]
    unmatched_new: list[int]


def normalize_line(line: str) -> str:
    return " ".join(line.lower().split())


def find_unchanged_lines(old_lines: list[str], new_lines: list[str]) -> DiffResult:
    """Find in-order matches after normalization and keep unmatched line numbers."""
    old_normalized = [normalize_line(line) for line in old_lines]
    new_normalized = [normalize_line(line) for line in new_lines]
    matcher = SequenceMatcher(None, old_normalized, new_normalized, autojunk=False)

    result = DiffResult(matches=[], unmatched_old=[], unmatched_new=[])
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        old_numbers = range(old_start + 1, old_end + 1)
        new_numbers = range(new_start + 1, new_end + 1)
        if tag == "equal":
            result.matches.extend(zip(old_numbers, new_numbers))
        else:
            result.unmatched_old.extend(old_numbers)
            result.unmatched_new.extend(new_numbers)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print old-new line pairs after normalizing case and whitespace."
    )
    parser.add_argument("old_file", type=Path, help="path to the older version")
    parser.add_argument("new_file", type=Path, help="path to the newer version")
    args = parser.parse_args()

    try:
        with args.old_file.open(encoding="utf-8") as old_file:
            old_lines = old_file.readlines()
        with args.new_file.open(encoding="utf-8") as new_file:
            new_lines = new_file.readlines()
    except (OSError, UnicodeError) as error:
        parser.error(str(error))

    result = find_unchanged_lines(old_lines, new_lines)
    for old_number, new_number in result.matches:
        print(f"{old_number}-{new_number}")


if __name__ == "__main__":
    main()
