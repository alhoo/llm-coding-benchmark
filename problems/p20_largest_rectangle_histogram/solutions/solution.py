"""
Reference solution for Largest Rectangle in Histogram.
Uses monotonic stack for O(n) time complexity.
"""


def largest_rectangle_area(heights: list[int]) -> int:
    """
    Return the area of the largest rectangle in the histogram.

    Uses a monotonic stack: we maintain indices of bars in increasing height order.
    When we see a bar shorter than the stack top, we've found the right boundary
    for all bars in the stack that are taller. Pop them, compute their rectangle
    (height * width where width = current_index - left_boundary - 1), update max.

    Time: O(n) — each bar pushed and popped at most once
    Space: O(n) for the stack
    """
    if not heights:
        return 0

    stack: list[int] = []  # indices of bars in increasing height order
    max_area = 0
    n = len(heights)

    for i in range(n):
        while stack and heights[i] < heights[stack[-1]]:
            # Pop: we've found the right boundary for this bar
            h_idx = stack.pop()
            h = heights[h_idx]
            # Left boundary: bar below in stack, or -1 if stack empty
            left = stack[-1] if stack else -1
            width = i - left - 1
            area = h * width
            max_area = max(max_area, area)

        stack.append(i)

    # Process remaining bars in stack (their right boundary is n)
    while stack:
        h_idx = stack.pop()
        h = heights[h_idx]
        left = stack[-1] if stack else -1
        width = n - left - 1
        area = h * width
        max_area = max(max_area, area)

    return max_area
