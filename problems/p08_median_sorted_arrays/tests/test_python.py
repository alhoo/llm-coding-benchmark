"""
Test harness for Median of Two Sorted Arrays problem (Python)
"""

import importlib.util
import json
import time
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p08_median_sorted_arrays_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestMedianSortedArrays:
    """Test suite for Median of Two Sorted Arrays problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().find_median_sorted_arrays

    def test_odd_length(self, solution):
        assert solution([1, 3], [2]) == 2.0

    def test_even_length(self, solution):
        assert solution([1, 2], [3, 4]) == 2.5

    def test_first_empty(self, solution):
        assert solution([], [1]) == 1.0

    def test_second_empty(self, solution):
        assert solution([2], []) == 2.0

    def test_all_same(self, solution):
        assert solution([0, 0], [0, 0]) == 0.0

    def test_non_overlapping(self, solution):
        assert solution([1, 2, 3, 4, 5], [6]) == 3.5

    def test_single_elements(self, solution):
        assert solution([1], [2]) == 1.5

    def test_negative_numbers(self, solution):
        assert solution([-5, -3, -1], [-4, -2, 0]) == -2.5

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["nums1"], case["nums2"])
        assert abs(result - case["expected"]) < 1e-9, (
            f"Failed '{case['name']}': "
            f"nums1={case['nums1']}, nums2={case['nums2']}, "
            f"expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution):
        """
        O(log(min(m,n))) should be near-instant for m=n=1000.
        An O(m+n) implementation would be measurably slower on large inputs.
        We time-test with sorted arrays to ensure no linear scan.
        """
        import random
        m, n = 1000, 1000
        nums1 = sorted(random.sample(range(1_000_000), m))
        nums2 = sorted(random.sample(range(1_000_000), n))

        start = time.perf_counter()
        for _ in range(10_000):
            solution(nums1, nums2)
        elapsed = time.perf_counter() - start

        assert elapsed < 2.0, (
            f"10,000 calls took {elapsed:.3f}s — expected < 2.0s for O(log(min(m,n)))"
        )

    def test_correctness_against_naive(self, solution):
        """Cross-check against the trivial O(m+n) merge implementation."""
        import random
        for _ in range(50):
            m = random.randint(0, 20)
            n = random.randint(1, 20)
            nums1 = sorted(random.randint(-100, 100) for _ in range(m))
            nums2 = sorted(random.randint(-100, 100) for _ in range(n))

            merged = sorted(nums1 + nums2)
            total = len(merged)
            if total % 2 == 1:
                expected = float(merged[total // 2])
            else:
                expected = (merged[total // 2 - 1] + merged[total // 2]) / 2.0

            result = solution(nums1, nums2)
            assert abs(result - expected) < 1e-9, (
                f"Mismatch: nums1={nums1}, nums2={nums2}, "
                f"expected={expected}, got={result}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
