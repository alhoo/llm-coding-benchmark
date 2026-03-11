# Evaluation Rubric: P06 - Merge K Sorted Lists

## Total Points: 100

---

## 1. Correctness (55 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Three lists | 15 | `[[1,4,5],[1,3,4],[2,6]]` → `[1,1,2,3,4,4,5,6]` |
| Empty input `[]` | 10 | Returns `None` |
| Single empty list `[[]]` | 10 | Returns `None` |
| Single list | 10 | Returns the list unchanged |
| Lists with negative values | 10 | Handles negatives correctly |

---

## 2. Time Complexity (35 points)

| Implementation | Points | Description |
|----------------|--------|-------------|
| Min-heap O(N log k) | 35 | Optimal |
| Divide & conquer O(N log k) | 35 | Also optimal |
| Merge one-by-one O(kN) | 10 | Correct but suboptimal |
| Collect all + sort O(N log N) | 5 | Works but ignores sorted property |
| Brute force | 0 | No credit |

---

## 3. Code Quality (10 points)

### Correctness of Heap Usage (5 points)
- ✅ **5 points**: Avoids comparing `ListNode` objects directly (uses tuple `(val, id, node)`)
- ❌ **0 points**: Crashes when two nodes have equal values due to node comparison

### Clarity (5 points)
- ✅ **5 points**: Clean implementation, clear variable names
- ⚠️ **2 points**: Works but convoluted

---

## Common LLM Failures

### ❌ Failure Pattern 1: ListNode Comparison Error

```python
import heapq
heap = []
for node in lists:
    if node:
        heapq.heappush(heap, (node.val, node))  # ❌ Crashes if two vals equal!
```

**Score**: 55/100 (Fails on equal-value nodes)

---

### ❌ Failure Pattern 2: O(kN) Sequential Merge

```python
def merge_k_lists(lists):
    result = lists[0]
    for i in range(1, len(lists)):
        result = merge_two(result, lists[i])  # O(kN) total
    return result
```

**Score**: 55/100 (Correct but suboptimal)

---

## ✅ Reference Solution

```python
import heapq

def merge_k_lists(lists):
    heap = []
    counter = 0  # tie-breaker to avoid comparing ListNode objects

    for node in lists:
        if node:
            heapq.heappush(heap, (node.val, counter, node))
            counter += 1

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, _, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, counter, node.next))
            counter += 1

    return dummy.next
```

**Score**: 100/100
