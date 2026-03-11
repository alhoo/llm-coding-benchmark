# Problem P08: Median of Two Sorted Arrays

## Problem Statement

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the **median** of the two sorted arrays.

The overall run time complexity must be **O(log(min(m, n)))**.

---

## Examples

### Example 1:
```
Input: nums1 = [1, 3], nums2 = [2]
Output: 2.0
Explanation: merged = [1, 2, 3], median = 2.0
```

### Example 2:
```
Input: nums1 = [1, 2], nums2 = [3, 4]
Output: 2.5
Explanation: merged = [1, 2, 3, 4], median = (2 + 3) / 2 = 2.5
```

### Example 3:
```
Input: nums1 = [], nums2 = [1]
Output: 1.0
```

### Example 4:
```
Input: nums1 = [2], nums2 = []
Output: 2.0
```

---

## Constraints

- `nums1.length == m`
- `nums2.length == n`
- `0 <= m <= 1000`
- `0 <= n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`
- Both `nums1` and `nums2` are sorted in non-decreasing order.

---

## Hints

1. The naive O(m+n) merge approach is NOT acceptable.
2. Binary search on the **smaller** array to find the correct partition.
3. The partition point `i` in `nums1` and `j = (m+n+1)//2 - i` in `nums2` satisfies: all elements on the left ≤ all elements on the right.
4. Check boundary conditions: `i=0`, `i=m`, `j=0`, `j=n` require special handling (`-inf`, `+inf`).
5. If `m+n` is odd, median = `max(left_max1, left_max2)`.

---

## Function Signature

### Python
```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases pass
2. **Time Complexity** (40 points) — O(log(min(m, n))) — binary search approach
3. **Space Complexity** (10 points) — O(1) — no merging into new array
