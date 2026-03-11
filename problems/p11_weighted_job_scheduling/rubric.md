# Evaluation Rubric: P11 - Weighted Job Scheduling

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Basic overlap | 10 | Pick best non-overlapping subset |
| Adjacent jobs | 10 | `end == start` of next → both taken |
| All overlapping | 5 | All overlap → pick single best |
| Single job | 5 | Trivial base case |
| Skip middle | 10 | DP required — greedy fails |
| Greedy trap | 10 | Greedy by profit gives wrong answer |

**Scoring**:
- Pass all: 50 points
- Fail 1 case: 35 points
- Fail 2 cases: 20 points
- Fail 3+ cases: 0 points

---

## 2. Time Complexity (40 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| O(n log n) — sort + DP + binary search | 40 | Optimal |
| O(n²) — DP without binary search | 20 | Correct but suboptimal |
| O(2^n) — brute force / backtracking | 0 | Unacceptable |

**Verification Method**:
- Timing test: n=50,000 should complete in < 1 second
- Check for binary search (e.g. `bisect` usage) after sorting

---

## 3. Code Quality (10 points)

### Algorithm Clarity (5 points)
- ✅ **5 points**: Clear sort-then-DP structure with binary search
- ⚠️ **3 points**: Correct but convoluted indexing
- ❌ **0 points**: Obscure or incorrect approach

### Edge Cases (5 points)
- ✅ **5 points**: Handles single job, all-overlapping, adjacent boundaries
- ❌ **0 points**: Crashes or off-by-one on boundary cases

---

## Common LLM Failures

### ❌ Failure Pattern 1: O(n²) DP Without Binary Search

```python
def max_profit_scheduling(start_time, end_time, profit):
    jobs = sorted(zip(end_time, start_time, profit))
    dp = [0] * len(jobs)
    for i in range(len(jobs)):
        dp[i] = jobs[i][2]
        for j in range(i):  # ❌ Linear scan instead of binary search
            if jobs[j][0] <= jobs[i][1]:
                dp[i] = max(dp[i], dp[j] + jobs[i][2])
    return max(dp)
```

**Score**: 70/100 (Correct but O(n²))

---

### ❌ Failure Pattern 2: Off-by-One in Binary Search

```python
# Using bisect_left instead of bisect_right causes missed compatible jobs
k = bisect.bisect_left(ends, s, 0, i)  # ❌ Wrong: may skip a compatible job
```

---

### ❌ Failure Pattern 3: Greedy by Profit

```python
# Sorting by profit and greedily picking non-overlapping jobs
# fails on cases where two smaller jobs beat one large job
```

**Score**: 30/100 (Incorrect for many cases)

---

## ✅ Reference Solution

```python
import bisect

def max_profit_scheduling(start_time, end_time, profit):
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
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(n log n)
- ✅ Space Complexity: O(n)
