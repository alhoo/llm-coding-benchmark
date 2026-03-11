"""
Test harness for LRU Cache problem (Python)
"""

import importlib.util
import json
import os
import time
import pytest
from pathlib import Path


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def _solution_path():
    """Path to solution module: temp file when run by benchmark, else reference."""
    problem_dir = Path(__file__).parent.parent
    bench_file = os.environ.get("BENCHMARK_SOLUTION_FILE")
    if bench_file:
        return problem_dir / bench_file
    return problem_dir / "solutions" / "solution.py"


def run_operations(lru_class, capacity, operations, args):
    """Execute a sequence of operations on an LRUCache instance."""
    cache = lru_class(capacity)
    results = []
    for op, arg in zip(operations, args):
        if op == "put":
            cache.put(arg[0], arg[1])
            results.append(None)
        elif op == "get":
            results.append(cache.get(arg[0]))
    return results


class TestLRUCache:
    """Test suite for LRU Cache problem."""

    @pytest.fixture
    def lru_class(self):
        spec = importlib.util.spec_from_file_location(
            "p02_lru_cache_solution",
            _solution_path(),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.LRUCache

    def test_basic_lru_eviction(self, lru_class):
        """Evicts LRU element when capacity exceeded."""
        cache = lru_class(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)
        assert cache.get(2) == -1  # key 2 was LRU (key 1 was accessed after insert)
        cache.put(4, 4)
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_get_missing_key(self, lru_class):
        """Returns -1 for missing keys."""
        cache = lru_class(3)
        assert cache.get(0) == -1
        assert cache.get(100) == -1

    def test_get_updates_recency(self, lru_class):
        """get() should promote the key to most-recently-used."""
        cache = lru_class(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.get(1)       # key 1 becomes MRU
        cache.put(3, 3)    # should evict key 2, not key 1
        assert cache.get(1) == 1
        assert cache.get(2) == -1

    def test_overwrite_updates_recency(self, lru_class):
        """put() on existing key updates value and marks as MRU."""
        cache = lru_class(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(1, 100)  # update key 1 (makes it MRU)
        cache.put(3, 3)    # should evict key 2
        assert cache.get(1) == 100
        assert cache.get(2) == -1
        assert cache.get(3) == 3

    def test_capacity_one(self, lru_class):
        """Capacity-1 cache evicts on every new insertion."""
        cache = lru_class(1)
        cache.put(1, 10)
        assert cache.get(1) == 10
        cache.put(2, 20)
        assert cache.get(1) == -1
        assert cache.get(2) == 20

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, lru_class, case):
        """Run operation sequences from JSON test cases."""
        results = run_operations(
            lru_class,
            case["capacity"],
            case["operations"],
            case["args"],
        )
        assert results == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {results}"
        )

    def test_time_complexity(self, lru_class):
        """
        Verify O(1) average time for get/put via timing on large cache.
        10,000 operations should complete in well under 1 second.
        """
        capacity = 1000
        cache = lru_class(capacity)

        start = time.perf_counter()
        for i in range(10_000):
            cache.put(i % capacity, i)
            cache.get((i + 1) % capacity)
        elapsed = time.perf_counter() - start

        assert elapsed < 1.0, (
            f"10,000 operations took {elapsed:.3f}s — expected < 1.0s for O(1) implementation"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
