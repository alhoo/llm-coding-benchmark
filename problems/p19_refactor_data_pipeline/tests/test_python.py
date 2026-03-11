"""
Test harness for Refactor Data Pipeline (Python).
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
    problem_dir = Path(__file__).parent.parent
    bench_file = os.environ.get("BENCHMARK_SOLUTION_FILE")
    if bench_file:
        return problem_dir / bench_file
    return problem_dir / "solutions" / "solution.py"


def _load_transform_records():
    spec = importlib.util.spec_from_file_location(
        "p19_refactor_solution",
        _solution_path(),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.transform_records


class TestRefactorDataPipeline:
    """Test suite for refactored data transformation pipeline."""

    @pytest.fixture
    def transform_records(self):
        return _load_transform_records()

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, transform_records, case):
        """Run all JSON-defined test cases - verifies behavioral correctness."""
        records = case["records"]
        schema = case["schema"]
        expected = case["expected"]
        result = transform_records(records, schema)
        assert result == expected, (
            f"Failed '{case['name']}': expected {expected}, got {result}"
        )

    def test_pattern_unified_aggregation(self, transform_records):
        """
        Pattern recognition: Refactored code should consolidate the six
        aggregation operations. Legacy has 6 nearly identical if/elif blocks.
        Refactored should use helpers, a dispatcher, or strategy map.
        """
        path = _solution_path()
        with open(path) as f:
            content = f.read()
        # Legacy-style: 6 consecutive "elif op ==" blocks
        elif_op_count = content.count('elif op ==') + content.count("elif op ==")
        # Refactored: handler dict, or multiple _agg_ helpers
        has_handlers = "handlers" in content or ("op" in content and '"sum"' in content)
        has_agg_helpers = "_agg_" in content or "def _aggregate" in content
        # Allow up to 2 elif op (e.g. for concat with separator) - not 6
        assert elif_op_count <= 3 or has_handlers or has_agg_helpers, (
            "Refactor: consolidate the six aggregation blocks into helpers or a dispatcher."
        )

    def test_pattern_extracted_helpers(self, transform_records):
        """
        Pattern recognition: Should have multiple functions - validation and
        aggregation logic extracted, not one giant transform_records.
        """
        path = _solution_path()
        with open(path) as f:
            tree = ast.parse(f.read())
        funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        assert len(funcs) >= 3, (
            "Refactored code should extract validation and aggregation logic "
            f"into helpers, not a single {len(funcs)}-function module."
        )
