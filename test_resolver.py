import unittest

from resolver import resolve_matches


class ResolveMatchesTest(unittest.TestCase):
    def test_higher_score_wins_and_other_line_uses_fallback(self):
        scores = [
            (1, 8, 0.84),
            (2, 8, 0.95),
            (1, 9, 0.80),
            (2, 10, 0.79),
            (3, 9, 0.72),
        ]

        self.assertEqual(resolve_matches(scores), [(1, 9), (2, 8)])

    def test_threshold_excludes_equal_and_lower_scores(self):
        scores = [(1, 8, 0.44), (2, 9, 0.45), (3, 10, 0.60), (4, 11, 0.75)]

        self.assertEqual(resolve_matches(scores), [(3, 10), (4, 11)])
        self.assertEqual(resolve_matches(scores, threshold=0.60), [(4, 11)])

    def test_equal_scores_favor_lower_line_numbers(self):
        scores = [(2, 9, 0.8), (2, 8, 0.8), (1, 9, 0.8), (1, 8, 0.8)]

        self.assertEqual(resolve_matches(iter(scores)), [(1, 8), (2, 9)])

    def test_empty_candidates(self):
        self.assertEqual(resolve_matches([]), [])
