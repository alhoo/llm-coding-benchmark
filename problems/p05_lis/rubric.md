# Evaluation Rubric: P05 - Longest Increasing Subsequence

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Standard case | 10 | `[10,9,2,5,3,7,101,18]` → 4 |
| Alternating | 10 | `[0,1,0,3,2,3]` → 4 |
| All equal | 10 | `[7,7,7,7]` → 1 (strictly increasing) |
| Single element | 5 | `[1]` → 1 |
| Already sorted | 10 | `[1,2,3,4,5]` → 5 |
| Reverse sorted | 5 | `[5,4,3,2,1]` → 1 |

---

## 2. Time Complexity (40 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| O(n log n) — patience sort + binary search | 40 | Optimal |
| O(n²) — DP with nested loops | 20 | Correct but suboptimal |
| O(n³) or worse | 0 | Unacceptable |

**Verification Method**:
- Timing test: array of 2500 elements should be instantaneous
- Check for `bisect` usage (Python) or manual binary search

---

## 3. Code Quality (10 points)

### Clarity (5 points)
- ✅ **5 points**: Clear `tails` array with binary search, well-named variables
- ⚠️ **3 points**: Correct but hard-to-follow indexing
- ❌ **0 points**: Obscure implementation

### Edge Cases (5 points)
- ✅ **5 points**: Handles single element and all-equal arrays
- ❌ **0 points**: Crashes or returns wrong answer on edge cases

---

## Common LLM Failures

### ❌ Failure Pattern 1: O(n²) DP Only

```python
def length_of_lis(nums):
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Score**: 70/100 (Correct but O(n²), fails complexity requirement)

---

### ❌ Failure Pattern 2: Binary Search Off-by-One

```python
# Using bisect_right instead of bisect_left causes incorrect results
# for strictly increasing subsequence
import bisect
tails = []
for num in nums:
    pos = bisect.bisect_right(tails, num)  # ❌ Should be bisect_left
    ...
```

---

## ✅ Reference Solution

```python
import bisect

def length_of_lis(nums: list[int]) -> int:
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(n log n)
- ✅ Space Complexity: O(n)
