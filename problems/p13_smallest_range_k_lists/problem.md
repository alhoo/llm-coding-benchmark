# Problem P13: Smallest Range Covering Elements from K Lists

## Problem Statement

You have `k` lists of sorted integers in non-decreasing order. Find the **smallest range** `[a, b]` that includes **at least one number from each** of the `k` lists.

The range `[a, b]` is smaller than `[c, d]` if `b - a < d - c`, or if `b - a == d - c` and `a < c`.

---

## Examples

### Example 1:
```
Input: nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
Output: [20, 24]
Explanation:
  List 0: 24 is in [20, 24].
  List 1: 20 is in [20, 24].
  List 2: 22 is in [20, 24].
```

### Example 2:
```
Input: nums = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
Output: [1, 1]
Explanation: All lists contain 1, so [1, 1] (range of size 0) is optimal.
```

### Example 3:
```
Input: nums = [[10], [11], [13]]
Output: [10, 13]
```

### Example 4:
```
Input: nums = [[1, 5, 8], [4, 12], [7, 8, 10]]
Output: [4, 7]
Explanation:
  List 0: 5 is in [4, 7].
  List 1: 4 is in [4, 7].
  List 2: 7 is in [4, 7].
```

---

## Constraints

- `k == nums.length`
- `1 <= k <= 3500`
- `1 <= nums[i].length <= 50`
- `-10^5 <= nums[i][j] <= 10^5`
- `nums[i]` is sorted in non-decreasing order.

---

## Hints

1. Think of this as a "sliding window" across all `k` lists simultaneously.
2. Use a **min-heap** containing one element from each list. The range is `[heap_min, current_max]`.
3. Pop the minimum element and advance its list pointer. Push the next element from that list, updating the current max.
4. Each time, check if the new range `[new_min, current_max]` is smaller than the best so far.
5. Stop when any list is exhausted (the range must cover all lists).
6. Time complexity: O(n log k) where n is the total number of elements.

---

## Function Signature

### Python
```python
def smallest_range(nums: list[list[int]]) -> list[int]:
    pass
```

### JavaScript
```javascript
function smallestRange(nums) {
    // Your code here
}
```

### Java
```java
public class Solution {
    public int[] smallestRange(List<List<Integer>> nums) {
        // Your code here
    }
}
```

### C++
```cpp
class Solution {
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        // Your code here
    }
};
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases return the correct smallest range
2. **Time Complexity** (35 points) — O(n log k) using a min-heap approach
3. **Code Quality** (15 points) — Clear heap management, proper termination logic
