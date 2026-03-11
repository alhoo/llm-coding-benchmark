"""
Test harness for Maximum Network Flow (Dinic's Algorithm) problem (Python)
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
    spec = importlib.util.spec_from_file_location("p15_max_flow_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestMaxFlow:
    """Test suite for Maximum Network Flow problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().max_flow

    def test_simple_diamond(self, solution):
        result = solution(4, [[0, 1, 10], [0, 2, 10], [1, 2, 2], [1, 3, 4], [2, 3, 8]], 0, 3)
        assert result == 12

    def test_clrs_example(self, solution):
        edges = [
            [0, 1, 16], [0, 2, 13], [1, 2, 10], [1, 3, 12],
            [2, 1, 4], [2, 4, 14], [3, 2, 9], [3, 5, 20],
            [4, 3, 7], [4, 5, 4],
        ]
        assert solution(6, edges, 0, 5) == 23

    def test_single_edge(self, solution):
        assert solution(2, [[0, 1, 100]], 0, 1) == 100

    def test_parallel_paths(self, solution):
        edges = [[0, 1, 1000000], [0, 2, 1000000], [1, 3, 1000000], [2, 3, 1000000]]
        assert solution(4, edges, 0, 3) == 2000000

    def test_parallel_edges(self, solution):
        """Multiple edges between the same pair of nodes should sum."""
        assert solution(3, [[0, 1, 5], [0, 1, 3]], 0, 1) == 8

    def test_no_edges(self, solution):
        assert solution(3, [], 0, 2) == 0

    def test_disconnected_sink(self, solution):
        assert solution(4, [[0, 1, 10], [1, 2, 10]], 0, 3) == 0

    def test_bottleneck(self, solution):
        """Flow is limited by the bottleneck edge."""
        edges = [[0, 1, 100], [1, 2, 1], [2, 3, 100], [3, 4, 100]]
        assert solution(5, edges, 0, 4) == 1

    def test_anti_parallel_edges(self, solution):
        """Edges going in both directions between two nodes."""
        edges = [[0, 1, 10], [1, 0, 5], [1, 2, 15], [0, 2, 10], [2, 3, 20]]
        assert solution(4, edges, 0, 3) == 20

    def test_complex_network(self, solution):
        """7-node network requiring multiple augmenting path iterations."""
        edges = [
            [0, 1, 10], [0, 2, 8], [0, 3, 12],
            [1, 4, 5], [1, 2, 3],
            [2, 4, 7], [2, 5, 4],
            [3, 2, 6], [3, 5, 9],
            [4, 6, 15],
            [5, 6, 10],
            [5, 4, 2],
        ]
        assert solution(7, edges, 0, 6) == 24

    def test_three_parallel_paths(self, solution):
        edges = [
            [0, 1, 5], [1, 2, 5], [2, 7, 5],
            [0, 3, 10], [3, 4, 10], [4, 7, 10],
            [0, 5, 7], [5, 6, 7], [6, 7, 7],
        ]
        assert solution(8, edges, 0, 7) == 22

    def test_unit_capacity(self, solution):
        """Unit capacities — max flow equals number of vertex-disjoint paths."""
        edges = [
            [0, 1, 1], [0, 2, 1], [0, 3, 1],
            [1, 4, 1], [2, 4, 1], [2, 5, 1], [3, 5, 1],
            [4, 5, 1],
        ]
        assert solution(6, edges, 0, 5) == 3

    def test_self_loop_ignored(self, solution):
        """Self-loops should not affect the flow."""
        edges = [[0, 0, 100], [0, 1, 5], [1, 1, 50], [1, 2, 3]]
        assert solution(3, edges, 0, 2) == 3

    def test_source_equals_bottleneck(self, solution):
        """Source has limited outgoing capacity."""
        edges = [[0, 1, 3], [0, 2, 4], [1, 3, 100], [2, 3, 100]]
        assert solution(4, edges, 0, 3) == 7

    def test_multiple_parallel_edges_same_pair(self, solution):
        """Many parallel edges between the same pair."""
        edges = [[0, 1, 1]] * 10
        assert solution(2, edges, 0, 1) == 10

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["n"], case["edges"], case["source"], case["sink"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution):
        """
        Dinic's algorithm O(V^2 E) should handle dense graphs reasonably.
        500 nodes, ~5000 edges.
        """
        import random
        n = 500
        edges = []
        for _ in range(5000):
            u = random.randint(0, n - 2)
            v = random.randint(u + 1, n - 1)
            cap = random.randint(1, 1000)
            edges.append([u, v, cap])

        start = time.perf_counter()
        result = solution(n, edges, 0, n - 1)
        elapsed = time.perf_counter() - start

        assert result >= 0
        assert elapsed < 5.0, (
            f"n={n}, 5000 edges took {elapsed:.3f}s — expected < 5s for Dinic's"
        )

    def test_time_complexity_dense(self, solution):
        """Stress test with a denser graph."""
        import random
        n = 200
        edges = []
        for u in range(n - 1):
            for v in range(u + 1, min(u + 6, n)):
                edges.append([u, v, random.randint(1, 100)])

        start = time.perf_counter()
        result = solution(n, edges, 0, n - 1)
        elapsed = time.perf_counter() - start

        assert result >= 0
        assert elapsed < 5.0, (
            f"Dense graph took {elapsed:.3f}s — expected < 5s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
