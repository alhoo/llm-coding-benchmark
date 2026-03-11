"""
Test harness for Word Ladder problem (Python)
"""

import importlib.util
import json
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p07_word_ladder_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


class TestWordLadder:
    """Test suite for Word Ladder problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().ladder_length

    def test_standard_path(self, solution):
        """Classic hit → cog example."""
        assert solution("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5

    def test_end_not_in_list(self, solution):
        """No path when endWord is not in wordList."""
        assert solution("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0

    def test_single_step(self, solution):
        """One transformation gives sequence length 2."""
        assert solution("hot", "dot", ["dot", "dog"]) == 2

    def test_unreachable(self, solution):
        """endWord in list but no valid transformation path."""
        assert solution("abc", "xyz", ["xyz"]) == 0

    def test_direct_transform(self, solution):
        """begin and end differ by exactly one letter."""
        assert solution("a", "c", ["b", "c"]) == 2

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, case):
        """Run all JSON-defined test cases."""
        result = solution(case["begin_word"], case["end_word"], case["word_list"])
        assert result == case["expected"], (
            f"Failed '{case['name']}': "
            f"begin={case['begin_word']!r}, end={case['end_word']!r}, "
            f"expected {case['expected']}, got {result}"
        )

    def test_bfs_gives_shortest(self, solution):
        """
        Verify BFS finds the SHORTEST path, not just any path.
        There are two paths:
          cat → bat → bad → bed (length 4)
          cat → car → bar → bad → bed (length 5)
        Correct answer is 4.
        """
        word_list = ["bat", "bad", "bed", "car", "bar"]
        result = solution("cat", "bed", word_list)
        assert result == 4, f"Expected shortest path of 4, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
