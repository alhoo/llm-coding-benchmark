"""
Reference solution for Weighted Job Scheduling.
Sort by end time, then DP with binary search for the latest compatible job.
Time Complexity: O(n log n)
Space Complexity: O(n)
"""

import bisect


def max_profit_scheduling(
    start_time: list[int], end_time: list[int], profit: list[int]
) -> int:
    """
    Return the maximum profit from a subset of non-overlapping jobs.

    Strategy:
      1. Sort jobs by end time.
      2. Build a DP array where dp[i] = max profit using the first i jobs.
      3. For job i, binary search in the sorted end-times to find the latest
         job that finishes at or before this job's start time.
      4. dp[i] = max(dp[i-1], dp[k] + profit_i), where k is the binary
         search result.

    Args:
        start_time: Start times of each job.
        end_time: End times of each job.
        profit: Profit of each job.

    Returns:
        Maximum achievable profit from non-overlapping jobs.
    """
    n = len(start_time)
    if n == 0:
        return 0

    jobs = sorted(zip(end_time, start_time, profit))
    ends = [j[0] for j in jobs]
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        e, s, p = jobs[i - 1]
        k = bisect.bisect_right(ends, s, 0, i - 1)
        dp[i] = max(dp[i - 1], dp[k] + p)

    return dp[n]


if __name__ == "__main__":
    assert max_profit_scheduling([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]) == 120
    assert max_profit_scheduling(
        [1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]
    ) == 150
    assert max_profit_scheduling([1, 1, 1], [2, 3, 4], [5, 6, 4]) == 6
    assert max_profit_scheduling([1], [10], [42]) == 42
    assert max_profit_scheduling([1, 2], [2, 3], [10, 20]) == 30
    print("All tests passed!")
