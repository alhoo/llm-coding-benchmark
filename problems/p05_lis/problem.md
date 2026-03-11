# Problem P05: Longest Increasing Subsequence

## Problem Statement

Given an integer array `nums`, return the **length** of the longest strictly increasing subsequence.

A **subsequence** is a sequence derived from the array by deleting some or no elements without changing the order of the remaining elements.

**Optimize for O(n log n) time complexity.**

---

## Examples

### Example 1:
```
Input: nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
Explanation: The LIS is [2, 3, 7, 101], length 4.
```

### Example 2:
```
Input: nums = [0, 1, 0, 3, 2, 3]
Output: 4
```

### Example 3:
```
Input: nums = [7, 7, 7, 7, 7, 7, 7]
Output: 1
```

### Example 4:
```
Input: nums = [1]
Output: 1
```

---

## Constraints

- `1 <= nums.length <= 2500`
- `-10^4 <= nums[i] <= 10^4`

---

## Hints

1. A simple DP approach gives O(n²): `dp[i]` = length of LIS ending at index `i`.
2. The optimal O(n log n) approach uses **patience sorting** with binary search.
3. Maintain a `tails` array where `tails[i]` is the smallest tail element of all increasing subsequences of length `i+1`.
4. For each number, binary search in `tails` to find where it fits.

---

## Function Signature

### Python
```python
def length_of_lis(nums: list[int]) -> int:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return correct length
2. **Time Complexity** (40 points) — O(n log n) via binary search + patience sort
3. **Code Quality** (10 points) — Clear, idiomatic implementation
