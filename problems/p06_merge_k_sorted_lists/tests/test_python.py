"""
Test harness for Merge K Sorted Lists problem (Python)
"""

import importlib.util
import json
import time
import pytest
from pathlib import Path


def _load_solution():
    spec = importlib.util.spec_from_file_location(
        "p06_merge_k_sorted_lists_solution",
        Path(__file__).parent.parent / "solutions" / "solution.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test_cases():
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        return json.load(f)


def list_to_linked(values: list, ListNode):
    dummy = ListNode()
    curr = dummy
    for v in values:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_to_list(head) -> list:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


class TestMergeKLists:
    """Test suite for Merge K Sorted Lists problem."""

    @pytest.fixture
    def solution(self):
        return _load_solution().merge_k_lists

    @pytest.fixture
    def ListNode(self):
        return _load_solution().ListNode

    def test_three_lists(self, solution, ListNode):
        lists = [list_to_linked([1, 4, 5], ListNode),
                 list_to_linked([1, 3, 4], ListNode),
                 list_to_linked([2, 6], ListNode)]
        assert linked_to_list(solution(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

    def test_empty_input(self, solution):
        assert solution([]) is None

    def test_single_empty_list(self, solution):
        assert solution([None]) is None

    def test_single_list(self, solution, ListNode):
        lists = [list_to_linked([1, 2, 3], ListNode)]
        assert linked_to_list(solution(lists)) == [1, 2, 3]

    def test_negatives(self, solution, ListNode):
        lists = [list_to_linked([-3, -1, 0], ListNode),
                 list_to_linked([-2, 2, 4], ListNode)]
        assert linked_to_list(solution(lists)) == [-3, -2, -1, 0, 2, 4]

    def test_duplicates(self, solution, ListNode):
        lists = [list_to_linked([1, 1, 2], ListNode),
                 list_to_linked([1, 2, 3], ListNode)]
        assert linked_to_list(solution(lists)) == [1, 1, 1, 2, 2, 3]

    @pytest.mark.parametrize("case", load_test_cases())
    def test_all_cases(self, solution, ListNode, case):
        """Run all JSON-defined test cases."""
        linked_lists = [list_to_linked(lst, ListNode) if lst else None
                        for lst in case["lists"]]
        result = linked_to_list(solution(linked_lists))
        assert result == case["expected"], (
            f"Failed '{case['name']}': expected {case['expected']}, got {result}"
        )

    def test_time_complexity(self, solution, ListNode):
        """
        O(N log k) should handle k=100 lists of 100 elements quickly.
        """
        k, n = 100, 100
        import random
        lists = []
        for _ in range(k):
            vals = sorted(random.sample(range(10000), n))
            lists.append(list_to_linked(vals, ListNode))

        start = time.perf_counter()
        result_head = solution(lists)
        elapsed = time.perf_counter() - start

        result = linked_to_list(result_head)
        assert len(result) == k * n
        assert result == sorted(result)
        assert elapsed < 1.0, (
            f"Took {elapsed:.3f}s for {k}×{n} elements — expected < 1.0s for O(N log k)"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
