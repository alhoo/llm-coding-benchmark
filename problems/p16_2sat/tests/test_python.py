"""
Test harness for 2-SAT Solver problem (Python)
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
    spec = importlib.util.spec_from_file_location("p16_2sat_solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def verify_assignment(n, clauses, assignment):
    """Verify that an assignment satisfies all clauses."""
    assert isinstance(assignment, list), "Assignment must be a list"
    assert len(assignment) == n, f"Assignment length {len(assignment)} != n={n}"
    for a, b in clauses:
        val_a = assignment[a - 1] if a > 0 else not assignment[-a - 1]
        val_b = assignment[b - 1] if b > 0 else not assignment[-b - 1]
        assert val_a or val_b, (
            f"Clause [{a}, {b}] not satisfied by assignment {assignment}"
        )


class TestSolve2SAT:
    """Test suite for 2-SAT Solver problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().solve_2sat

    def test_simple_or(self, solution):
        """(x1 OR x2) — at least one must be True."""
        result = solution(2, [[1, 2]])
        assert result is not None
        verify_assignment(2, [[1, 2]], result)

    def test_forced_true(self, solution):
        """(x1 OR x1) forces x1 = True."""
        result = solution(1, [[1, 1]])
        assert result is not None
        assert result[0] is True

    def test_forced_false(self, solution):
        """(NOT x1 OR NOT x1) forces x1 = False."""
        result = solution(1, [[-1, -1]])
        assert result is not None
        assert result[0] is False

    def test_contradiction(self, solution):
        """x1 AND NOT x1 — UNSAT."""
        assert solution(1, [[1, 1], [-1, -1]]) is None

    def test_biconditional(self, solution):
        """(x1 ↔ x2): both must have the same value."""
        clauses = [[1, -2], [-1, 2]]
        result = solution(2, clauses)
        assert result is not None
        verify_assignment(2, clauses, result)
        assert result[0] == result[1], "x1 ↔ x2 requires equal values"

    def test_xor(self, solution):
        """(x1 XOR x2): must differ."""
        clauses = [[1, 2], [-1, -2]]
        result = solution(2, clauses)
        assert result is not None
        verify_assignment(2, clauses, result)
        assert result[0] != result[1], "x1 XOR x2 requires different values"

    def test_all_four_clauses_unsat(self, solution):
        """All four 2-clauses on two variables — UNSAT."""
        assert solution(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]]) is None

    def test_no_clauses(self, solution):
        """No clauses — trivially satisfiable."""
        result = solution(3, [])
        assert result is not None
        assert len(result) == 3

    def test_tautological_clauses(self, solution):
        """Tautological clauses (x OR NOT x) are always satisfied."""
        clauses = [[1, -1], [2, -2]]
        result = solution(2, clauses)
        assert result is not None
        assert len(result) == 2

    def test_chain_implications_all_true(self, solution):
        """Chain x1→x2→x3→x4 with x1 forced True."""
        clauses = [[-1, 2], [-2, 3], [-3, 4], [1, 1]]
        result = solution(4, clauses)
        assert result is not None
        verify_assignment(4, clauses, result)
        assert all(result), "Chain from forced x1 should make all True"

    def test_chain_contradiction(self, solution):
        """Chain from forced x1 to x3, but x3 is forced False — UNSAT."""
        assert solution(3, [[1, 1], [-1, 2], [-2, 3], [-3, -3]]) is None

    def test_independent_xor_pairs(self, solution):
        """Two independent XOR pairs: (x1 XOR x2) and (x3 XOR x4)."""
        clauses = [[1, 2], [-1, -2], [3, 4], [-3, -4]]
        result = solution(4, clauses)
        assert result is not None
        verify_assignment(4, clauses, result)
        assert result[0] != result[1]
        assert result[2] != result[3]

    def test_diamond_implications(self, solution):
        """Diamond: x1 forced True, implies x2 and x3, both imply x4."""
        clauses = [[-1, 2], [-1, 3], [-2, 4], [-3, 4], [1, 1]]
        result = solution(4, clauses)
        assert result is not None
        verify_assignment(4, clauses, result)
        assert result[0] is True
        assert result[3] is True

    def test_many_clauses_sat(self, solution):
        """10 variables with 15 clauses — SAT."""
        clauses = [
            [1, 2], [-1, 3], [-2, 4], [3, -5], [-4, 6],
            [5, -7], [-6, 8], [7, -9], [-8, 10], [9, -10],
            [1, -3], [2, -4], [-5, 7], [6, -8], [-9, 10],
        ]
        result = solution(10, clauses)
        assert result is not None
        verify_assignment(10, clauses, result)

    def test_duplicate_clauses(self, solution):
        """Duplicate clauses should not cause issues."""
        clauses = [[1, 2], [1, 2], [1, 2], [-1, -2]]
        result = solution(2, clauses)
        assert result is not None
        verify_assignment(2, clauses, result)

    def test_self_referencing_clause(self, solution):
        """Clause [x, -x] is a tautology, should not constrain anything."""
        clauses = [[1, -1]]
        result = solution(1, clauses)
        assert result is not None
        assert len(result) == 1

    def test_long_implication_chain(self, solution):
        """x1 forced True, chain of 50 implications."""
        n = 51
        clauses = [[1, 1]]
        for i in range(1, n):
            clauses.append([-i, i + 1])
        result = solution(n, clauses)
        assert result is not None
        verify_assignment(n, clauses, result)
        assert all(result), "All variables should be True via chain"

    def test_long_chain_contradiction(self, solution):
        """x1 forced True, chain of 50, last forced False — UNSAT."""
        n = 51
        clauses = [[1, 1]]
        for i in range(1, n):
            clauses.append([-i, i + 1])
        clauses.append([-n, -n])
        assert solution(n, clauses) is None

    def test_bipartite_structure(self, solution):
        """Variables split into two groups with cross-constraints."""
        clauses = [
            [1, 3], [2, 4], [-1, -3], [-2, -4],
            [1, -4], [-2, 3],
        ]
        result = solution(4, clauses)
        assert result is not None
        verify_assignment(4, clauses, result)

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["n"], case["clauses"])
        if case["satisfiable"]:
            assert result is not None, f"Expected SAT for '{case['name']}', got None"
            verify_assignment(case["n"], case["clauses"], result)
            if "forced" in case:
                for var_str, expected_val in case["forced"].items():
                    var_idx = int(var_str) - 1
                    assert result[var_idx] == expected_val, (
                        f"'{case['name']}': variable x{var_str} should be {expected_val}"
                    )
        else:
            assert result is None, (
                f"Expected UNSAT for '{case['name']}', got {result}"
            )

    def test_time_complexity_large_sat(self, solution):
        """
        Large satisfiable instance: 50,000 variables, 100,000 clauses.
        O(n + m) SCC should handle this in well under 5 seconds.
        """
        import random
        random.seed(42)
        n = 50_000
        clauses = []
        for _ in range(100_000):
            a = random.randint(1, n) * random.choice([1, -1])
            b = random.randint(1, n) * random.choice([1, -1])
            clauses.append([a, b])

        start = time.perf_counter()
        result = solution(n, clauses)
        elapsed = time.perf_counter() - start

        if result is not None:
            assert len(result) == n
        assert elapsed < 5.0, (
            f"50k vars, 100k clauses took {elapsed:.3f}s — expected < 5s for SCC-based"
        )

    def test_time_complexity_large_chain(self, solution):
        """
        Chain of 100,000 implications. Stress test for iterative DFS.
        Recursive implementations will hit RecursionError.
        """
        n = 100_000
        clauses = [[1, 1]]
        for i in range(1, n):
            clauses.append([-i, i + 1])

        start = time.perf_counter()
        result = solution(n, clauses)
        elapsed = time.perf_counter() - start

        assert result is not None, "Long chain should be SAT"
        assert len(result) == n
        assert result[0] is True
        assert elapsed < 5.0, (
            f"100k chain took {elapsed:.3f}s — expected < 5s"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
