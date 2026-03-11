"""
Test harness for Smallest Range Covering K Lists problem (Python)
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
    spec = importlib.util.spec_from_file_location("p13_smallest_range_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestSmallestRange:
    """Test suite for Smallest Range Covering K Lists problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().smallest_range

    def test_classic_three_lists(self, solution):
        result = solution([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
        assert result == [20, 24]

    def test_identical_lists(self, solution):
        """All lists identical — optimal range is a single point."""
        result = solution([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
        assert result == [1, 1]

    def test_single_element_lists(self, solution):
        """Each list has one element — range must span all."""
        result = solution([[10], [11], [13]])
        assert result == [10, 13]

    def test_overlapping_ranges(self, solution):
        result = solution([[1, 5, 8], [4, 12], [7, 8, 10]])
        assert result == [4, 7]

    def test_single_list(self, solution):
        """Only one list — range is just its first element."""
        result = solution([[3, 7, 11]])
        assert result == [3, 3]

    def test_negative_numbers(self, solution):
        """Lists with negative values."""
        result = solution([[-5, -3, 0], [-4, -1, 2], [-6, -2, 1]])
        assert result == [-6, -4]

    def test_large_gap(self, solution):
        """One list is far from others — range must bridge the gap."""
        result = solution([[1, 2, 3], [100, 200, 300], [50, 150, 250]])
        assert result == [3, 100]

    def test_all_same_values(self, solution):
        """Every element is the same."""
        result = solution([[5, 5, 5], [5, 5], [5, 5, 5, 5]])
        assert result == [5, 5]

    def test_range_covers_all_lists(self, solution):
        """Verify the returned range actually covers all lists."""
        nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
        a, b = solution(nums)
        for lst in nums:
            assert any(a <= x <= b for x in lst), (
                f"Range [{a}, {b}] doesn't cover list {lst}"
            )

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["nums"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution):
        """
        O(n log k) should handle k=3000, 50 elements each (n=150,000) quickly.
        """
        import random
        k = 3000
        nums = [sorted(random.sample(range(-100000, 100001), 50)) for _ in range(k)]

        start = time.perf_counter()
        result = solution(nums)
        elapsed = time.perf_counter() - start

        assert len(result) == 2
        assert result[0] <= result[1]
        assert elapsed < 2.0, (
            f"Took {elapsed:.3f}s for k={k}, 50 elems each — expected < 2.0s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
