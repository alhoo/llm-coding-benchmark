"""
Test harness for Topological Sort problem (Python)
"""

import importlib.util
import json
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p04_topological_sort_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def is_valid_topological_order(n: int, edges: list, order: list) -> bool:
    """Verify that `order` is a valid topological ordering for the given graph."""
    if len(order) != n:
        return False
    position = {node: i for i, node in enumerate(order)}
    return all(position[u] < position[v] for u, v in edges)


class TestTopologicalSort:
    """Test suite for Topological Sort problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().topological_sort

    def test_basic_dag(self, solution):
        """Standard DAG returns a valid topological ordering."""
        edges = [[5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]]
        result = solution(6, edges)
        assert is_valid_topological_order(6, edges, result)

    def test_simple_cycle(self, solution):
        """Two-node cycle returns empty list."""
        assert solution(2, [[0, 1], [1, 0]]) == []

    def test_self_loop(self, solution):
        """Self-loop is a cycle; returns empty list."""
        assert solution(3, [[0, 1], [1, 1]]) == []

    def test_single_node(self, solution):
        """Single node with no edges."""
        result = solution(1, [])
        assert result == [0]

    def test_chain(self, solution):
        """Linear chain: 0→1→2→3→4 has exactly one valid order."""
        edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
        result = solution(5, edges)
        assert result == [0, 1, 2, 3, 4]

    def test_disconnected_graph(self, solution):
        """Disconnected graph includes all nodes."""
        edges = [[0, 1], [2, 3]]
        result = solution(4, edges)
        assert is_valid_topological_order(4, edges, result)

    def test_no_edges(self, solution):
        """Graph with no edges: all nodes appear in output."""
        result = solution(5, [])
        assert sorted(result) == [0, 1, 2, 3, 4]

    def test_longer_cycle(self, solution):
        """4-node cycle returns empty list."""
        assert solution(4, [[0, 1], [1, 2], [2, 3], [3, 0]]) == []

    def test_diamond(self, solution):
        """Diamond-shaped DAG (0→1, 0→2, 1→3, 2→3) is a valid DAG."""
        edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
        result = solution(4, edges)
        assert is_valid_topological_order(4, edges, result)

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["n"], case["edges"])
        if case["has_cycle"]:
            assert result == [], (
                f"Expected [] for cycle in '{case['name']}', got {result}"
            )
        else:
            assert is_valid_topological_order(case["n"], case["edges"], result), (
                f"Invalid topological order for '{case['name']}': {result}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
