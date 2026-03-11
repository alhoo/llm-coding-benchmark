# Evaluation Rubric: P08 - Median of Two Sorted Arrays

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Both arrays non-empty, odd total | 10 | `[1,3], [2]` → 2.0 |
| Both arrays non-empty, even total | 10 | `[1,2], [3,4]` → 2.5 |
| One array empty | 10 | `[], [1]` → 1.0 |
| All elements in one array | 10 | `[1,2,3,4,5], [6]` → 3.5 |
| Arrays of different sizes | 10 | `[1,2,3], [4,5,6,7,8]` → 5.0 |

---

## 2. Time Complexity (40 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| O(log(min(m,n))) — binary search on smaller array | 40 | Optimal, as required |
| O(log(m+n)) — binary search variant | 30 | Near-optimal, acceptable |
| O(m+n) — merge arrays | 0 | Fails the complexity requirement |
| O((m+n) log(m+n)) — sort merged | 0 | Fails the complexity requirement |

**Note**: The problem explicitly requires O(log(min(m,n))). Most LLMs default to O(m+n) merge.

---

## 3. Space Complexity (10 points)

| Implementation | Points |
|----------------|--------|
| O(1) — in-place binary search | 10 |
| O(m+n) — creates merged array | 0 |

---

## Common LLM Failures

### ❌ Failure Pattern 1: O(m+n) Merge (Most Common)

```python
def find_median_sorted_arrays(nums1, nums2):
    merged = sorted(nums1 + nums2)  # ❌ O(m+n) space and O((m+n)log(m+n)) time
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0
```

**Score**: 50/100 (Correct answers, wrong complexity)

---

### ❌ Failure Pattern 2: Binary Search With Wrong Boundary Handling

```python
# Forgets to handle i=0 or i=m edge cases
# Leads to index out of bounds or wrong partition
max_left1 = nums1[i-1]  # ❌ Crashes when i=0
```

---

## ✅ Reference Solution

```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2

    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i

        max_left1  = nums1[i-1] if i > 0 else float('-inf')
        min_right1 = nums1[i]   if i < m else float('inf')
        max_left2  = nums2[j-1] if j > 0 else float('-inf')
        min_right2 = nums2[j]   if j < n else float('inf')

        if max_left1 <= min_right2 and max_left2 <= min_right1:
            if (m + n) % 2 == 1:
                return float(max(max_left1, max_left2))
            return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            hi = i - 1
        else:
            lo = i + 1

    return 0.0
```

**Score**: 100/100
