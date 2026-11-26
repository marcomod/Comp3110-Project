"""Select one-to-one matches from scored line candidates."""

from collections.abc import Iterable


def resolve_matches(
    scored_candidates: Iterable[tuple[int, int, float]],
    *,
    threshold: float = 0.45,
) -> list[tuple[int, int]]:
    """Return matches in old line order from (old_line, new_line, score) triples.

    Line numbers are 1-based. Process scores above the threshold from highest
    to lowest. Ties favor the lower old line number, then the lower new line
    number.
    """
    ranked = sorted(
        (candidate for candidate in scored_candidates if candidate[2] > threshold),
        key=lambda candidate: (-candidate[2], candidate[0], candidate[1]),
    )

    matches: dict[int, int] = {}
    used_new_lines: set[int] = set()
    for old_line, new_line, _ in ranked:
        if old_line in matches or new_line in used_new_lines:
            continue
        matches[old_line] = new_line
        used_new_lines.add(new_line)

    return sorted(matches.items())
