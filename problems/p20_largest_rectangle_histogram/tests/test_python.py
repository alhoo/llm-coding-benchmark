"""
Test harness for Largest Rectangle in Histogram (Python).
Tests correctness and O(n) time complexity.
"""

import json
import os
import time
import pytest
from pathlib import Path
import importlib.util


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def _solution_path():
    """Path to solution: temp file when run by benchmark, else reference."""
    problem_dir = Path(__file__).parent.parent
    bench_file = os.environ.get("BENCHMARK_SOLUTION_FILE")
    if bench_file:
        return problem_dir / bench_file
    return problem_dir / "solutions" / "solution.py"


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p20_histogram_solution",
        _solution_path(),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.largest_rectangle_area


class TestLargestRectangleHistogram:
    """Test suite for Largest Rectangle in Histogram."""

    @pytest.fixture
    def solution(self):
        return _load_solution()

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["heights"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {result} "
            f"for heights={case['heights']}"
        )

    def test_empty_input(self, solution):
        """Empty array should return 0."""
        assert solution([]) == 0

    def test_time_complexity(self, solution):
        """
        Verify O(n) time complexity.

        Uses 50,000 bars. O(n) should complete in < 1.5 seconds.
        O(n²) would take 50+ seconds and will timeout.
        """
        n = 50_000
        # Construct a histogram that stresses the algorithm:
        # Alternating pattern that forces stack operations
        heights = [1 + (i % 100) for i in range(n)]

        start = time.perf_counter()
        result = solution(heights)
        elapsed = time.perf_counter() - start

        # Verify we got some result (sanity check)
        assert isinstance(result, int) and result >= 0

        # O(n) should finish in under 1.5 seconds on typical hardware
        # O(n²) would take 2500x longer (~50+ seconds)
        assert elapsed < 1.5, (
            f"Solution took {elapsed:.3f}s for n={n}. "
            "Expected O(n) — completes in < 1.5s. "
            "O(n²) implementation will fail this test."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
