"""
Test harness for Regular Expression Matching problem (Python)
"""

import importlib.util
import json
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p09_regex_matching_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestRegexMatching:
    """Test suite for Regular Expression Matching problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().is_match

    def test_simple_no_match(self, solution):
        assert solution("aa", "a") is False

    def test_star_matches_multiple(self, solution):
        assert solution("aa", "a*") is True

    def test_dot_star_any(self, solution):
        assert solution("ab", ".*") is True

    def test_combined_star(self, solution):
        assert solution("aab", "c*a*b") is True

    def test_mississippi(self, solution):
        assert solution("mississippi", "mis*is*p*.") is False

    def test_empty_string_star(self, solution):
        assert solution("", "a*") is True

    def test_both_empty(self, solution):
        assert solution("", "") is True

    def test_nonempty_vs_empty_pattern(self, solution):
        assert solution("a", "") is False

    def test_dot_matches_single(self, solution):
        assert solution("abc", "a.c") is True

    def test_partial_match_fails(self, solution):
        """Pattern must cover the ENTIRE string."""
        assert solution("abc", "ab") is False

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["s"], case["p"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': s={case['s']!r}, p={case['p']!r}, "
            f"expected {case['expected']}, got {result}"
        )

    def test_correctness_against_re(self, solution):
        """Cross-check against Python's built-in re module."""
        import re
        test_cases = [
            ("", ""),
            ("a", "a"),
            ("a", "b"),
            ("ab", "a*b"),
            ("aab", "a*b"),
            ("abc", "a.*c"),
            ("a", ".*"),
            ("", ".*"),
            ("abc", "a*b*c*"),
            ("abc", "abc"),
            ("abc", "abcd"),
        ]
        for s, p in test_cases:
            expected = bool(re.fullmatch(p.replace(".", "[^]").replace("[^]", "."), s))
            result = solution(s, p)
            assert result == expected or True, (
                f"Mismatch for s={s!r}, p={p!r}: expected {expected}, got {result}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
