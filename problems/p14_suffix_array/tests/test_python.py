"""
Test harness for Suffix Array, LCP Array & Distinct Substrings problem (Python)
"""

import importlib.util
import json
import os
import time
import pytest
from pathlib import Path


def _load_solution():
    problem_dir = Path(__file__).parent.parent
    bench_file = os.environ.get("BENCHMARK_SOLUTION_FILE")
    path = problem_dir / bench_file if bench_file else problem_dir / "solutions" / "solution.py"
    spec = importlib.util.spec_from_file_location("p14_suffix_array_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestSuffixArray:
    """Test suite for Suffix Array construction."""

    @pytest.fixture
    def build_sa(self):
        return _load_solution().build_suffix_array

    def test_banana(self, build_sa):
        assert build_sa("banana") == [5, 3, 1, 0, 4, 2]

    def test_single_char(self, build_sa):
        assert build_sa("z") == [0]

    def test_all_same(self, build_sa):
        assert build_sa("aaaa") == [3, 2, 1, 0]

    def test_all_unique(self, build_sa):
        assert build_sa("abcde") == [0, 1, 2, 3, 4]

    def test_mississippi(self, build_sa):
        assert build_sa("mississippi") == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]

    def test_empty_string(self, build_sa):
        assert build_sa("") == []

    def test_two_chars(self, build_sa):
        assert build_sa("ba") == [1, 0]

    def test_sorted_order_property(self, build_sa):
        """The suffix array must produce lexicographically sorted suffixes."""
        s = "the quick brown fox jumps over the lazy dog"
        s = s.replace(" ", "")
        sa = build_sa(s)
        suffixes = [s[i:] for i in sa]
        assert suffixes == sorted(suffixes)

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases_sa(self, build_sa, case):
        result = build_sa(case["s"])
        assert result == case["expected_sa"], (
            f"Failed SA for '{case['name']}': expected {case['expected_sa']}, got {result}"
        )


class TestLCPArray:
    """Test suite for LCP Array construction (Kasai's algorithm)."""

    @pytest.fixture
    def build_lcp(self):
        return _load_solution().build_lcp_array

    @pytest.fixture
    def build_sa(self):
        return _load_solution().build_suffix_array

    def test_banana(self, build_lcp):
        assert build_lcp("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]

    def test_all_same(self, build_lcp):
        assert build_lcp("aaaa", [3, 2, 1, 0]) == [0, 1, 2, 3]

    def test_all_unique(self, build_lcp):
        assert build_lcp("abcde", [0, 1, 2, 3, 4]) == [0, 0, 0, 0, 0]

    def test_single_char(self, build_lcp):
        assert build_lcp("z", [0]) == [0]

    def test_empty(self, build_lcp):
        assert build_lcp("", []) == []

    def test_lcp_first_element_zero(self, build_lcp, build_sa):
        """lcp[0] must always be 0 (no predecessor)."""
        for s in ["banana", "abcabc", "mississippi", "aaaa"]:
            sa = build_sa(s)
            lcp = build_lcp(s, sa)
            assert lcp[0] == 0, f"lcp[0] should be 0 for '{s}'"

    def test_lcp_values_bounded(self, build_lcp, build_sa):
        """Each lcp[i] must not exceed the length of the shorter suffix."""
        s = "abacaba"
        sa = build_sa(s)
        lcp = build_lcp(s, sa)
        n = len(s)
        for i in range(1, n):
            max_possible = min(n - sa[i], n - sa[i - 1])
            assert lcp[i] <= max_possible

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases_lcp(self, build_lcp, case):
        result = build_lcp(case["s"], case["expected_sa"])
        assert result == case["expected_lcp"], (
            f"Failed LCP for '{case['name']}': expected {case['expected_lcp']}, got {result}"
        )


class TestDistinctSubstrings:
    """Test suite for counting distinct substrings."""

    @pytest.fixture
    def count_distinct(self):
        return _load_solution().count_distinct_substrings

    def test_banana(self, count_distinct):
        assert count_distinct("banana") == 15

    def test_abab(self, count_distinct):
        assert count_distinct("abab") == 7

    def test_all_same(self, count_distinct):
        assert count_distinct("aaaa") == 4

    def test_all_unique(self, count_distinct):
        assert count_distinct("abcde") == 15

    def test_single_char(self, count_distinct):
        assert count_distinct("z") == 1

    def test_empty(self, count_distinct):
        assert count_distinct("") == 0

    def test_mississippi(self, count_distinct):
        assert count_distinct("mississippi") == 53

    def test_abcabc(self, count_distinct):
        assert count_distinct("abcabc") == 15

    def test_two_chars(self, count_distinct):
        """'ba' has 3 distinct substrings: 'b', 'a', 'ba'."""
        assert count_distinct("ba") == 3

    def test_cross_check_brute_force(self, count_distinct):
        """Cross-check against brute-force set-based counting on small strings."""
        test_strings = ["ab", "aab", "abc", "abab", "abcabc", "aabaa", "xyxyx"]
        for s in test_strings:
            brute = len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})
            assert count_distinct(s) == brute, (
                f"Mismatch for '{s}': formula={count_distinct(s)}, brute={brute}"
            )

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases_distinct(self, count_distinct, case):
        result = count_distinct(case["s"])
        assert result == case["expected_distinct"], (
            f"Failed distinct count for '{case['name']}': "
            f"expected {case['expected_distinct']}, got {result}"
        )

    def test_time_complexity(self, count_distinct):
        """
        O(n log^2 n) should handle n=100,000 within a few seconds.
        """
        import random
        import string
        s = "".join(random.choices(string.ascii_lowercase, k=100_000))

        start = time.perf_counter()
        result = count_distinct(s)
        elapsed = time.perf_counter() - start

        assert result > 0
        assert elapsed < 10.0, (
            f"n=100,000 took {elapsed:.3f}s — expected < 10s for O(n log^2 n)"
        )

    def test_time_complexity_repeated(self, count_distinct):
        """Worst case for suffix arrays: highly repetitive string."""
        s = "a" * 50_000 + "b" * 50_000

        start = time.perf_counter()
        result = count_distinct(s)
        elapsed = time.perf_counter() - start

        assert result > 0
        assert elapsed < 10.0, (
            f"Repetitive n=100,000 took {elapsed:.3f}s — expected < 10s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
