# Problem P11: Weighted Job Scheduling

## Problem Statement

You are given `n` jobs where each job `i` has a start time `start_time[i]`, an end time `end_time[i]`, and a profit `profit[i]`.

Find the **maximum profit** you can earn by selecting a subset of **non-overlapping** jobs. Two jobs are considered non-overlapping if one ends before or at the time the other starts (i.e., `end_time[i] <= start_time[j]`).

**Optimize for O(n log n) time complexity.**

---

## Examples

### Example 1:
```
Input: start_time = [1, 2, 3, 3], end_time = [3, 4, 5, 6], profit = [50, 10, 40, 70]
Output: 120
Explanation: Pick jobs (1→3, profit 50) and (3→6, profit 70). Total = 120.
```

### Example 2:
```
Input: start_time = [1, 2, 3, 4, 6], end_time = [3, 5, 10, 6, 9], profit = [20, 20, 100, 70, 60]
Output: 150
Explanation: Pick jobs (1→3, profit 20) + (4→6, profit 70) + (6→9, profit 60) = 150.
```

### Example 3:
```
Input: start_time = [1, 1, 1], end_time = [2, 3, 4], profit = [5, 6, 4]
Output: 6
Explanation: All jobs overlap; pick the most profitable one (profit 6).
```

### Example 4:
```
Input: start_time = [1], end_time = [10], profit = [42]
Output: 42
```

---

## Constraints

- `1 <= n <= 5 * 10^4`
- `1 <= start_time[i] < end_time[i] <= 10^9`
- `1 <= profit[i] <= 10^4`

---

## Hints

1. Sort jobs by end time. Then for each job, decide: skip it, or take it plus the best profit from compatible earlier jobs.
2. After sorting, use dynamic programming: `dp[i]` = max profit considering the first `i` jobs.
3. For each job, binary search for the latest non-overlapping job (the rightmost job whose end time ≤ current job's start time).
4. Transition: `dp[i] = max(dp[i-1], dp[k] + profit[i])` where `k` is found via binary search.

---

## Function Signature

### Python
```python
def max_profit_scheduling(start_time: list[int], end_time: list[int], profit: list[int]) -> int:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return the correct maximum profit
2. **Time Complexity** (40 points) — O(n log n) via sorting + DP with binary search
3. **Code Quality** (10 points) — Clear, idiomatic implementation
