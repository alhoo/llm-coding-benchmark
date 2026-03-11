# Problem P06: Merge K Sorted Lists

## Problem Statement

You are given an array of `k` linked-lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

---

## Examples

### Example 1:
```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
  1 → 4 → 5
  1 → 3 → 4
  2 → 6
Merging them into one sorted list: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6
```

### Example 2:
```
Input: lists = []
Output: []
```

### Example 3:
```
Input: lists = [[]]
Output: []
```

---

## Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.

---

## Hints

1. A naive approach merges lists one by one: O(kN) where N is total nodes.
2. **Min-heap approach**: Push the head of each list into a priority queue. Pop the minimum, advance that list, push the next node. O(N log k).
3. **Divide and conquer**: Merge pairs of lists repeatedly. O(N log k).
4. Both heap and divide-and-conquer achieve O(N log k).

---

## ListNode Definition

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

---

## Function Signature

### Python
```python
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    pass
```

---

## Evaluation Criteria

1. **Correctness** (55 points) — All test cases pass
2. **Time Complexity** (35 points) — O(N log k) where N = total nodes, k = number of lists
3. **Code Quality** (10 points) — Clean, idiomatic implementation
