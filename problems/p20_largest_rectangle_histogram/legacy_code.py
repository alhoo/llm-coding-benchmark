"""
LEGACY IMPLEMENTATION - Correct but O(n²) time complexity.
This is the reference naive solution. Your task is to optimize to O(n).
DO NOT submit this code - produce an optimized solution.
"""


def largest_rectangle_area(heights: list[int]) -> int:
    """
    Naive O(n²) solution: For each bar, expand left and right to find
    the boundaries (first bar shorter than current), then compute area.

    Time: O(n²) — for each of n bars, we may scan O(n) bars left and right.
    Space: O(1)
    """
    if not heights:
        return 0

    n = len(heights)
    max_area = 0

    for i in range(n):
        h = heights[i]

        # Expand left: find left boundary (first index where height < h)
        left = i
        while left > 0 and heights[left - 1] >= h:
            left -= 1

        # Expand right: find right boundary (first index where height < h)
        right = i
        while right < n - 1 and heights[right + 1] >= h:
            right += 1

        # Rectangle with height h spans from left to right (inclusive)
        width = right - left + 1
        area = h * width
        max_area = max(max_area, area)

    return max_area
