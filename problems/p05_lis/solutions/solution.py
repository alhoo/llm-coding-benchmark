"""
Reference solution for Longest Increasing Subsequence.
Uses patience sorting with binary search.
Time Complexity: O(n log n)
Space Complexity: O(n)
"""

import bisect


def length_of_lis(nums: list[int]) -> int:
    """
    Return the length of the longest strictly increasing subsequence.

    Uses patience sorting: maintains a 'tails' array where tails[i] is the
    smallest possible tail value for an increasing subsequence of length i+1.
    Binary search locates the insertion point in O(log n) per element.

    Args:
        nums: List of integers

    Returns:
        Length of the longest strictly increasing subsequence.

    Example:
        >>> length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    tails: list[int] = []

    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)


if __name__ == "__main__":
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7, 7, 7, 7]) == 1
    assert length_of_lis([1]) == 1
    assert length_of_lis([1, 2, 3, 4, 5]) == 5
    assert length_of_lis([5, 4, 3, 2, 1]) == 1
    print("All tests passed!")
