# Problem P20: Largest Rectangle in Histogram (Complexity Optimization)

## Problem Statement

You are given a **working but inefficient** implementation that finds the area of the largest rectangle in a histogram. The implementation is **correct** but has **O(n²) time complexity**.

Your task: **Recognize the underlying pattern and optimize it to O(n) time complexity** while preserving exact correctness.

---

## What the Function Does

Given an array `heights` where each element represents the height of a bar in a histogram (drawn with width 1), return the **area** of the largest rectangle that can be formed within the histogram.

A rectangle's area = height × width, where:
- **Height** = the minimum bar height in the span
- **Width** = the number of bars in the span

---

## Examples

### Example 1:
```
Input: heights = [2, 1, 5, 6, 2, 3]
Output: 10
Explanation: The largest rectangle has height 5 and width 2 (bars at indices 2 and 3).
Area = 5 × 2 = 10.
```

### Example 2:
```
Input: heights = [2, 4]
Output: 4
Explanation: Either rectangle of height 2 (width 2) or height 4 (width 1). Max = 4.
```

### Example 3:
```
Input: heights = [1]
Output: 1
```

### Example 4:
```
Input: heights = [2, 1, 2]
Output: 3
Explanation: Rectangle spanning all three bars, height 1, width 3. Area = 3.
```

---

## Required Interface

Your optimized solution **must** expose exactly:

```python
def largest_rectangle_area(heights: list[int]) -> int:
    """
    Return the area of the largest rectangle in the histogram.
    Must run in O(n) time.
    """
```

---

## Constraints

- `1 <= len(heights) <= 10^5`
- `0 <= heights[i] <= 10^4`

---

## Why This Is Hard

The naive approach (provided below) considers each bar as a potential rectangle height and expands left/right to find boundaries. This is O(n²).

The optimal O(n) solution requires recognizing a **monotonic stack** pattern: when you see a bar shorter than the previous one, you can immediately compute the maximum rectangle that uses the previous bar as height—because you've found its right boundary. The left boundary is the bar below it in the stack.

Most LLMs will either:
1. Keep the O(n²) approach (fails the time complexity test)
2. Attempt optimizations that break correctness on edge cases
3. Fail to recognize the monotonic stack pattern

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return the exact expected area
2. **Time Complexity** (40 points) — O(n) verified via timing on large input (50,000 bars)
3. **Code Quality** (10 points) — Clear, idiomatic implementation

---

## Hints (Use Sparingly)

1. The naive solution expands left and right from each bar. Can you process bars in a single pass?
2. When does a bar's "rectangle" end? When you encounter a shorter bar.
3. A **stack** that maintains bars in increasing height order can answer "what's the previous smaller bar?" in O(1) amortized time.
