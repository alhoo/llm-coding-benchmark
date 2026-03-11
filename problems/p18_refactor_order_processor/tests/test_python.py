"""
Test harness for Refactor Order Processor (Python).
Tests correctness and pattern recognition in refactored code.
"""

import ast
import importlib.util
import json
import os
import pytest
from pathlib import Path


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


def _load_process_order():
    spec = importlib.util.spec_from_file_location(
        "p18_refactor_solution",
        _solution_path(),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.process_order


class TestRefactorOrderProcessor:
    """Test suite for refactored order processor."""

    @pytest.fixture
    def process_order(self):
        return _load_process_order()

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, process_order, case):
        """Run all JSON-defined test cases - verifies behavioral correctness."""
        order = case["order"]
        expected = case["expected"]
        result = process_order(order)
        assert result == expected, (
            f"Failed '{case['name']}': expected {expected}, got {result}"
        )

    def test_pattern_no_monolithic_function(self, process_order):
        """
        Pattern recognition: Refactored code should extract logic into helpers.
        A single function > 80 lines suggests copy-paste rather than refactoring.
        """
        path = _solution_path()
        with open(path) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
                assert lines <= 85, (
                    f"Function '{node.name}' has {lines} lines. "
                    "Extract validation, tax, shipping into separate functions."
                )

    def test_pattern_extracted_helpers(self, process_order):
        """
        Pattern recognition: Should have multiple functions (extracted validation,
        tax, shipping, or discount logic) - not one giant process_order.
        """
        path = _solution_path()
        with open(path) as f:
            tree = ast.parse(f.read())
        funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        assert len(funcs) >= 2, (
            "Refactored code should extract logic into helper functions, "
            f"not a single {len(funcs)}-function module."
        )
