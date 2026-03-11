"""
Test harness for LFU Cache problem (Python)
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
    spec = importlib.util.spec_from_file_location("p12_lfu_cache_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def run_operations(lfu_class, capacity, operations, args):
    """Execute a sequence of operations on an LFUCache instance."""
    cache = lfu_class(capacity)
    results = []
    for op, arg in zip(operations, args):
        if op == "put":
            cache.put(arg[0], arg[1])
            results.append(None)
        elif op == "get":
            results.append(cache.get(arg[0]))
    return results


class TestLFUCache:
    """Test suite for LFU Cache problem."""

    @pytest.fixture
    def lfu_class(self):
        return _load_solution().LFUCache

    def test_basic_lfu_eviction(self, lfu_class):
        """Evicts the least frequently used key."""
        cache = lfu_class(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1    # freq(1)=2, freq(2)=1
        cache.put(3, 3)             # evict key 2 (lowest freq)
        assert cache.get(2) == -1
        assert cache.get(3) == 3    # freq(3)=2
        cache.put(4, 4)             # freq(1)=2, freq(3)=2; key 1 is LRU → evict 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_zero_capacity(self, lfu_class):
        """Capacity 0 stores nothing."""
        cache = lfu_class(0)
        cache.put(0, 0)
        assert cache.get(0) == -1

    def test_capacity_one(self, lfu_class):
        """Capacity 1 evicts on every new insertion."""
        cache = lfu_class(1)
        cache.put(1, 10)
        assert cache.get(1) == 10
        cache.put(2, 20)
        assert cache.get(1) == -1
        assert cache.get(2) == 20

    def test_frequency_tiebreak_by_lru(self, lfu_class):
        """When multiple keys share the min frequency, evict the LRU one."""
        cache = lfu_class(3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.get(1)    # freq(1)=2
        cache.get(2)    # freq(2)=2
        # freq(3)=1 → should be evicted on next insert
        cache.put(4, 4)
        assert cache.get(3) == -1
        assert cache.get(4) == 4

    def test_overwrite_updates_frequency(self, lfu_class):
        """put() on existing key updates value AND increments frequency."""
        cache = lfu_class(2)
        cache.put(1, 1)     # freq(1)=1
        cache.put(2, 2)     # freq(2)=1
        cache.put(1, 10)    # updates value, freq(1)=2
        cache.put(3, 3)     # evict key 2 (freq=1, not key 1 with freq=2)
        assert cache.get(1) == 10
        assert cache.get(2) == -1

    def test_get_missing_key(self, lfu_class):
        """Getting a non-existent key returns -1."""
        cache = lfu_class(3)
        assert cache.get(99) == -1
        cache.put(1, 100)
        assert cache.get(99) == -1

    def test_promote_through_frequencies(self, lfu_class):
        """Key accessed many times has high frequency and survives eviction."""
        cache = lfu_class(2)
        cache.put(1, 1)     # freq(1)=1
        cache.put(2, 2)     # freq(2)=1
        cache.get(1)        # freq(1)=2
        cache.get(1)        # freq(1)=3
        cache.get(1)        # freq(1)=4
        cache.put(3, 3)     # evict key 2 (freq=1)
        assert cache.get(2) == -1
        assert cache.get(1) == 1

    def test_evict_then_reinsert(self, lfu_class):
        """Evicted key reinserted as fresh with freq=1."""
        cache = lfu_class(2)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.get(1)        # freq(1)=2
        cache.put(3, 3)     # evict key 2
        assert cache.get(2) == -1
        cache.put(2, 20)    # reinsert key 2 with new value, freq=1
        assert cache.get(2) == 20

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, lfu_class, case):
        """Run operation sequences from JSON test cases."""
        results = run_operations(
            lfu_class,
            case["capacity"],
            case["operations"],
            case["args"],
        )
        assert results == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {results}"
        )

    def test_time_complexity(self, lfu_class):
        """
        O(1) average for get/put: 100,000 operations should complete quickly.
        """
        capacity = 1000
        cache = lfu_class(capacity)

        start = time.perf_counter()
        for i in range(100_000):
            cache.put(i % (capacity * 2), i)
            cache.get(i % capacity)
        elapsed = time.perf_counter() - start

        assert elapsed < 2.0, (
            f"100,000 operations took {elapsed:.3f}s — expected < 2.0s for O(1) implementation"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
