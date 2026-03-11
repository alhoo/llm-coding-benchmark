"""
Reference solution for Smallest Range Covering Elements from K Lists.
Uses a min-heap with one pointer per list, tracking the current max.
Time Complexity: O(n log k) where n = total elements, k = number of lists
Space Complexity: O(k) for the heap
"""

import heapq


def smallest_range(nums: list[list[int]]) -> list[int]:
    """
    Find the smallest range [a, b] containing at least one element from each list.

    Strategy:
      1. Initialize a min-heap with the first element from each list.
         Track the current maximum across all heap entries.
      2. The current range is [heap_min, current_max].
      3. Pop the minimum, advance that list's pointer, push the next element,
         update current_max.
      4. Each iteration, compare [new_min, current_max] to the best range.
      5. Stop when any list is exhausted — no valid range can be formed.

    Args:
        nums: List of k sorted integer lists.

    Returns:
        [a, b] representing the smallest valid range.
    """
    heap: list[tuple[int, int, int]] = []
    current_max = float("-inf")

    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])

    best = [heap[0][0], current_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)

        if current_max - min_val < best[1] - best[0]:
            best = [min_val, current_max]

        if elem_idx + 1 >= len(nums[list_idx]):
            break

        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)

    return best


if __name__ == "__main__":
    assert smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]) == [
        20,
        24,
    ]
    assert smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]]) == [1, 1]
    assert smallest_range([[10], [11], [13]]) == [10, 13]
    assert smallest_range([[1, 5, 8], [4, 12], [7, 8, 10]]) == [4, 7]
    print("All tests passed!")
