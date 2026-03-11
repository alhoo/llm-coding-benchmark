# Evaluation Rubric: P13 - Smallest Range Covering K Lists

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Classic 3-list example | 10 | Standard case with varying list lengths |
| Identical lists | 5 | All lists share elements → range of size 0 |
| Single-element lists | 10 | Forced to span from min to max |
| Overlapping ranges | 10 | Optimal range found in the overlap region |
| Negative numbers | 5 | Correct handling of negative values |
| Single list (k=1) | 5 | Degenerate case: range is [first, first] |
| Large gap between lists | 5 | Must bridge a wide gap |

**Scoring**:
- Pass all: 50 points
- Fail 1 case: 35 points
- Fail 2 cases: 20 points
- Fail 3+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Expected: O(n log k) where n = total elements, k = number of lists

| Implementation | Points | Description |
|----------------|--------|-------------|
| Min-heap with k pointers + max tracking | 35 | Optimal O(n log k) |
| Sort all + sliding window | 20 | O(n log n) — correct but suboptimal for large k |
| Brute force all combinations | 0 | O(n^k) — unacceptable |

**Verification Method**:
- Timing test: k=3000, 50 elements per list should complete in < 2 seconds
- Check for heap usage (e.g. `heapq`)

---

## 3. Code Quality (15 points)

### Algorithm Design (8 points)
- ✅ **8 points**: Clean min-heap approach with proper max tracking and termination
- ⚠️ **4 points**: Works but convoluted pointer management
- ❌ **0 points**: Incorrect termination or missing coverage check

### Edge Cases (4 points)
- ✅ **4 points**: Handles k=1, identical values, negative numbers, single-element lists
- ❌ **0 points**: Crashes or wrong answer on edge cases

### Best Practices (3 points)
- ✅ **3 points**: Clean variable names, proper tuple packing in heap
- ❌ **0 points**: Confusing variable names, magic numbers

---

## Common LLM Failures

### ❌ Failure Pattern 1: Forgetting to Track Current Max

```python
def smallest_range(nums):
    heap = [(lst[0], i, 0) for i, lst in enumerate(nums)]
    heapq.heapify(heap)
    # ❌ Only tracks min via heap, doesn't maintain current_max
    # Result: range calculation is wrong
```

**Score**: 25/100 (Fundamental logic error)

---

### ❌ Failure Pattern 2: Not Breaking When a List is Exhausted

```python
while heap:
    min_val, list_idx, elem_idx = heapq.heappop(heap)
    if elem_idx + 1 < len(nums[list_idx]):
        heapq.heappush(heap, ...)
    # ❌ Continues after a list is exhausted
    # The range no longer covers all lists!
```

**Score**: 40/100 (May return invalid ranges that don't cover all lists)

---

### ❌ Failure Pattern 3: O(n log n) Sort-Then-Slide Approach

```python
# Flatten all lists, sort, then slide a window
# Works but is O(n log n) instead of O(n log k)
all_elements = sorted((val, i) for i, lst in enumerate(nums) for val in lst)
```

**Score**: 70/100 (Correct but suboptimal complexity)

---

## ✅ Reference Solution

```python
import heapq

def smallest_range(nums):
    heap = []
    current_max = float('-inf')
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])

    best = [heap[0][0], current_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)
        if current_max - min_val < best[1] - best[0]:
            best = [min_val, current_max]
        if elem_idx + 1 >= len(nums[list_idx]):
            break
        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)

    return best
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(n log k)
- ✅ Space Complexity: O(k)
