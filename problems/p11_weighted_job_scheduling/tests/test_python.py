"""
Test harness for Weighted Job Scheduling problem (Python)
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
    spec = importlib.util.spec_from_file_location("p11_weighted_job_scheduling_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestWeightedJobScheduling:
    """Test suite for Weighted Job Scheduling problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().max_profit_scheduling

    def test_basic_overlap(self, solution):
        assert solution([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120

    def test_all_overlapping(self, solution):
        """All jobs overlap — pick the single most profitable."""
        assert solution([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6

    def test_adjacent_non_overlapping(self, solution):
        """Jobs exactly adjacent (end == start of next) should all be taken."""
        assert solution([1, 2, 3], [2, 3, 4], [10, 20, 30]) == 60

    def test_single_job(self, solution):
        assert solution([1], [10], [42]) == 42

    def test_skip_middle_job(self, solution):
        """Optimal to skip the middle job and take first + last."""
        assert solution([1, 2, 4], [3, 5, 6], [60, 10, 60]) == 120

    def test_greedy_by_profit_fails(self, solution):
        """Greedy picking highest profit first gives suboptimal result."""
        assert solution([1, 1, 2, 4], [5, 3, 4, 6], [70, 30, 40, 50]) == 90

    def test_identical_intervals(self, solution):
        """All jobs have the same time range — take the most profitable."""
        assert solution([1, 1, 1, 1], [5, 5, 5, 5], [1, 2, 3, 4]) == 4

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["start_time"], case["end_time"], case["profit"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution):
        """
        O(n log n) should handle n=50,000 quickly.
        An O(n²) implementation would take noticeable time.
        """
        import random
        n = 50_000
        start_time = [random.randint(1, 10**6) for _ in range(n)]
        end_time = [s + random.randint(1, 1000) for s in start_time]
        profit = [random.randint(1, 10000) for _ in range(n)]

        start = time.perf_counter()
        result = solution(start_time, end_time, profit)
        elapsed = time.perf_counter() - start

        assert result > 0
        assert elapsed < 1.0, (
            f"Took {elapsed:.3f}s for n={n} — expected < 1.0s for O(n log n)"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
