"""
Test harness for Minimum Cost Maximum Flow problem (Python)
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
    spec = importlib.util.spec_from_file_location("p17_min_cost_flow_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestMinCostMaxFlow:
    """Test suite for Minimum Cost Maximum Flow problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().min_cost_max_flow

    def test_single_edge(self, solution):
        assert solution(2, [[0, 1, 5, 3]], 0, 1) == (5, 15)

    def test_two_paths_different_costs(self, solution):
        """Cheaper path should be used first to minimize total cost."""
        edges = [[0, 1, 5, 1], [1, 3, 5, 2], [0, 2, 5, 10], [2, 3, 5, 20]]
        assert solution(4, edges, 0, 3) == (10, 165)

    def test_parallel_edges_different_costs(self, solution):
        """Parallel edges: cheaper one used first."""
        assert solution(3, [[0, 1, 5, 1], [0, 1, 5, 3]], 0, 1) == (10, 20)

    def test_no_edges(self, solution):
        assert solution(2, [], 0, 1) == (0, 0)

    def test_disconnected_sink(self, solution):
        assert solution(3, [[0, 1, 5, 1]], 0, 2) == (0, 0)

    def test_bottleneck(self, solution):
        edges = [[0, 1, 100, 1], [1, 2, 1, 1], [2, 3, 100, 1], [3, 4, 100, 1]]
        assert solution(5, edges, 0, 4) == (1, 4)

    def test_diamond_reroute(self, solution):
        """Diamond graph where flow must be rerouted through residual edges."""
        edges = [[0, 1, 3, 1], [0, 2, 3, 2], [1, 3, 2, 1], [2, 3, 2, 1], [1, 2, 2, 0]]
        assert solution(4, edges, 0, 3) == (4, 9)

    def test_anti_parallel_edges(self, solution):
        """Edges in both directions between the same nodes."""
        edges = [[0, 1, 10, 2], [1, 0, 5, 3], [1, 2, 15, 1], [0, 2, 10, 5]]
        assert solution(3, edges, 0, 2) == (20, 80)

    def test_zero_cost(self, solution):
        assert solution(2, [[0, 1, 10, 0]], 0, 1) == (10, 0)

    def test_complex_6_nodes(self, solution):
        """Complex 6-node network requiring multiple augmenting paths."""
        edges = [
            [0, 1, 5, 2], [0, 2, 8, 4],
            [1, 2, 3, 1], [1, 3, 7, 6],
            [2, 3, 5, 3], [2, 4, 4, 2],
            [3, 5, 10, 5], [4, 5, 6, 3],
            [4, 3, 2, 1],
        ]
        assert solution(6, edges, 0, 5) == (13, 147)

    def test_three_parallel_paths(self, solution):
        """Three independent paths with increasing per-unit costs."""
        edges = [
            [0, 1, 10, 1], [0, 2, 10, 2], [0, 3, 10, 3],
            [1, 4, 10, 1], [2, 4, 10, 1], [3, 4, 10, 1],
        ]
        assert solution(5, edges, 0, 4) == (30, 90)

    def test_self_loop(self, solution):
        """Self-loops should not affect the flow or cost."""
        edges = [[0, 0, 100, 1], [0, 1, 5, 2], [1, 1, 50, 1], [1, 2, 3, 4]]
        assert solution(3, edges, 0, 2) == (3, 18)

    def test_single_node_path(self, solution):
        """Direct edge from source to sink with various costs."""
        edges = [[0, 1, 1, 100], [0, 1, 1, 200], [0, 1, 1, 300]]
        assert solution(2, edges, 0, 1) == (3, 600)

    def test_rerouting_saves_cost(self, solution):
        """
        Graph where initial greedy path is suboptimal.
        Rerouting through residual graph yields lower total cost.
        
        Edges:
          0→1 cap=2 cost=1
          0→2 cap=2 cost=5
          1→2 cap=1 cost=1
          1→3 cap=1 cost=6
          2→3 cap=2 cost=1
        
        Greedy would push 0→1→3 (cost 7) and 0→2→3 (cost 6).
        But SPFA finds 0→1→2→3 (cost 3) first, then reroutes.
        """
        edges = [
            [0, 1, 2, 1], [0, 2, 2, 5],
            [1, 2, 1, 1], [1, 3, 1, 6],
            [2, 3, 2, 1],
        ]
        flow, cost = solution(4, edges, 0, 3)
        assert flow == 3
        assert cost == 16

    def test_equal_cost_paths(self, solution):
        """All paths have the same per-unit cost."""
        edges = [[0, 1, 5, 3], [0, 2, 5, 3], [1, 3, 5, 3], [2, 3, 5, 3]]
        assert solution(4, edges, 0, 3) == (10, 60)

    def test_source_bottleneck(self, solution):
        """Source has limited outgoing capacity."""
        edges = [[0, 1, 2, 1], [0, 2, 3, 2], [1, 3, 100, 1], [2, 3, 100, 1]]
        assert solution(4, edges, 0, 3) == (5, 13)

    def test_multiple_parallel_same_pair(self, solution):
        """Many parallel edges between the same pair, different costs."""
        edges = [[0, 1, 1, i] for i in range(10)]
        flow, cost = solution(2, edges, 0, 1)
        assert flow == 10
        assert cost == sum(range(10))  # 0+1+2+...+9 = 45

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["n"], case["edges"], case["source"], case["sink"])
        assert result == (case["expected_flow"], case["expected_cost"]), (
            f"Failed '{case['name']}': expected ({case['expected_flow']}, {case['expected_cost']}), got {result}"
        )

    def test_time_complexity(self, solution):
        """
        SPFA-based MCMF should handle moderate-sized graphs.
        200 nodes, ~2000 edges.
        """
        import random
        random.seed(42)
        n = 200
        edges = []
        for _ in range(2000):
            u = random.randint(0, n - 2)
            v = random.randint(u + 1, n - 1)
            cap = random.randint(1, 50)
            cost = random.randint(0, 100)
            edges.append([u, v, cap, cost])

        start = time.perf_counter()
        flow, cost = solution(n, edges, 0, n - 1)
        elapsed = time.perf_counter() - start

        assert flow >= 0
        assert cost >= 0
        assert elapsed < 10.0, (
            f"n={n}, 2000 edges took {elapsed:.3f}s — expected < 10s for SPFA-based MCMF"
        )

    def test_time_complexity_dense(self, solution):
        """Denser graph stress test."""
        import random
        random.seed(123)
        n = 100
        edges = []
        for u in range(n - 1):
            for v in range(u + 1, min(u + 8, n)):
                edges.append([u, v, random.randint(1, 20), random.randint(1, 50)])

        start = time.perf_counter()
        flow, cost = solution(n, edges, 0, n - 1)
        elapsed = time.perf_counter() - start

        assert flow >= 0
        assert cost >= 0
        assert elapsed < 10.0, (
            f"Dense graph took {elapsed:.3f}s — expected < 10s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
