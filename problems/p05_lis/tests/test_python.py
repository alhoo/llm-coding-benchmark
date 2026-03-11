"""
Test harness for Longest Increasing Subsequence problem (Python)
"""

import importlib.util
import json
import time
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p05_lis_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestLIS:
    """Test suite for Longest Increasing Subsequence problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().length_of_lis

    def test_standard_case(self, solution):
        assert solution([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    def test_alternating(self, solution):
        assert solution([0, 1, 0, 3, 2, 3]) == 4

    def test_all_equal(self, solution):
        """Strictly increasing — repeated values don't count."""
        assert solution([7, 7, 7, 7, 7, 7, 7]) == 1

    def test_single_element(self, solution):
        assert solution([1]) == 1

    def test_sorted_ascending(self, solution):
        assert solution([1, 2, 3, 4, 5]) == 5

    def test_sorted_descending(self, solution):
        assert solution([5, 4, 3, 2, 1]) == 1

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["nums"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': nums={case['nums']}, "
            f"expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution):
        """
        O(n log n) should handle n=2500 instantly.
        An O(n²) implementation would take noticeable time.
        """
        import random
        nums = random.sample(range(10000), 2500)

        start = time.perf_counter()
        result = solution(nums)
        elapsed = time.perf_counter() - start

        assert 1 <= result <= 2500
        assert elapsed < 0.5, (
            f"Took {elapsed:.3f}s for n=2500 — expected < 0.5s for O(n log n)"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
