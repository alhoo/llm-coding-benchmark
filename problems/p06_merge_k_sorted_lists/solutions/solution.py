"""
Reference solution for Merge K Sorted Lists.
Uses a min-heap for O(N log k) performance.
Time Complexity: O(N log k) where N = total nodes, k = number of lists
Space Complexity: O(k) for the heap
"""

import heapq


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    """
    Merge k sorted linked lists into one sorted linked list.

    Uses a min-heap seeded with the head of each list. A monotonically
    increasing counter breaks ties to avoid comparing ListNode objects.

    Args:
        lists: List of sorted linked list heads (may be None)

    Returns:
        Head of the merged sorted linked list.

    Example:
        >>> # [1->4->5, 1->3->4, 2->6] -> 1->1->2->3->4->4->5->6
    """
    heap: list[tuple[int, int, ListNode]] = []
    counter = 0

    for node in lists:
        if node is not None:
            heapq.heappush(heap, (node.val, counter, node))
            counter += 1

    dummy = ListNode(0)
    curr = dummy

    while heap:
        _, _, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, counter, node.next))
            counter += 1

    return dummy.next


def list_to_linked(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    curr = dummy
    for v in values:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_to_list(head: ListNode | None) -> list[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    lists = [list_to_linked([1, 4, 5]), list_to_linked([1, 3, 4]), list_to_linked([2, 6])]
    assert linked_to_list(merge_k_lists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]

    assert merge_k_lists([]) is None
    assert merge_k_lists([None]) is None

    print("All tests passed!")
