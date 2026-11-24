"""Rank unmatched source lines using SimHash."""

from bisect import bisect_left, bisect_right
from collections import Counter
from hashlib import blake2b
from heapq import nsmallest


_HASH_BYTES = 8
_CONTEXT_LINES = 4


def _simhash(text: str) -> int:
    if not text:
        return 0

    # Character pairs capture small edits without language-specific tokens.
    features = Counter(text[index:index + 2] for index in range(max(1, len(text) - 1)))
    votes = [0] * (_HASH_BYTES * 8)
    for feature, frequency in features.items():
        digest = blake2b(feature.encode("utf-8"), digest_size=_HASH_BYTES).digest()
        bits = int.from_bytes(digest, "big")
        for bit in range(len(votes)):
            votes[bit] += frequency if bits & (1 << bit) else -frequency

    return sum(1 << bit for bit, vote in enumerate(votes) if vote > 0)


def _fingerprint_lines(lines: list[str], numbers: list[int]) -> dict[int, tuple[int, int]]:
    nonblank = [number for number, line in enumerate(lines, start=1) if line]
    fingerprints = {}
    for number in numbers:
        if not 1 <= number <= len(lines):
            raise ValueError(f"Line number {number} is out of range")

        left = bisect_left(nonblank, number)
        right = bisect_right(nonblank, number)
        before = nonblank[max(0, left - _CONTEXT_LINES):left]
        after = nonblank[right:right + _CONTEXT_LINES]
        context = " ".join(lines[neighbor - 1] for neighbor in before + after)
        fingerprints[number] = (_simhash(lines[number - 1]), _simhash(context))

    return fingerprints


def _weighted_distance(old: tuple[int, int], new: tuple[int, int]) -> int:
    old_content, old_context = old
    new_content, new_context = new
    content_distance = bin(old_content ^ new_content).count("1")
    context_distance = bin(old_context ^ new_context).count("1")
    # Integer weights preserve the 60/40 ranking without rounding differences.
    return 3 * content_distance + 2 * context_distance


def shortlist_candidates(
    old_lines: list[str],
    new_lines: list[str],
    unmatched_old: list[int],
    unmatched_new: list[int],
    *,
    k: int = 15,
) -> dict[int, list[int]]:
    """Return up to k ranked new line numbers for each unmatched old line.

    Pass all lines from both files, normalized with lhdiff.normalize_line,
    and the 1-based unmatched line numbers from lhdiff.find_unchanged_lines.
    If distances tie, the lower new line number comes first.
    """
    if k < 1:
        raise ValueError("k must be positive")
    if not unmatched_old or not unmatched_new:
        return {number: [] for number in unmatched_old}

    old_fingerprints = _fingerprint_lines(old_lines, unmatched_old)
    new_fingerprints = _fingerprint_lines(new_lines, unmatched_new)
    candidates = {}
    for old_number, old_fingerprint in old_fingerprints.items():
        ranked = (
            (_weighted_distance(old_fingerprint, new_fingerprint), new_number)
            for new_number, new_fingerprint in new_fingerprints.items()
        )
        candidates[old_number] = [new_number for _, new_number in nsmallest(k, ranked)]

    return candidates
