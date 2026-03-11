"""
Reference solution for Median of Two Sorted Arrays.
Uses binary search on the smaller array.
Time Complexity: O(log(min(m, n)))
Space Complexity: O(1)
"""


def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Find the median of two sorted arrays in O(log(min(m,n))) time.

    Performs binary search on the smaller array to find the correct
    partition point such that:
      max(left partition) <= min(right partition)

    The partition divides both arrays so the left half contains exactly
    (m+n+1)//2 elements total.

    Args:
        nums1: First sorted array
        nums2: Second sorted array

    Returns:
        Median of the combined sorted sequence as a float.

    Example:
        >>> find_median_sorted_arrays([1, 3], [2])
        2.0
        >>> find_median_sorted_arrays([1, 2], [3, 4])
        2.5
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i

        max_left1 = nums1[i - 1] if i > 0 else float("-inf")
        min_right1 = nums1[i] if i < m else float("inf")
        max_left2 = nums2[j - 1] if j > 0 else float("-inf")
        min_right2 = nums2[j] if j < n else float("inf")

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 1:
                return float(max(max_left1, max_left2))
            return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            hi = i - 1
        else:
            lo = i + 1

    return 0.0


if __name__ == "__main__":
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert find_median_sorted_arrays([], [1]) == 1.0
    assert find_median_sorted_arrays([2], []) == 2.0
    assert find_median_sorted_arrays([0, 0], [0, 0]) == 0.0
    assert find_median_sorted_arrays([1, 2, 3, 4, 5], [6]) == 3.5
    print("All tests passed!")
