# Problem P02: LRU Cache

## Problem Statement

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.

Implement the `LRUCache` class:

- `LRUCache(int capacity)` — Initialize the LRU cache with **positive** size `capacity`.
- `int get(int key)` — Return the value of the `key` if it exists, otherwise return `-1`.
- `void put(int key, int value)` — Update the value of `key` if it exists. Otherwise, add the `key-value` pair. If the number of keys exceeds the `capacity`, **evict the least recently used key**.

The functions `get` and `put` must each run in **O(1) average time complexity**.

---

## Examples

### Example 1:
```
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1, cache is {2=2, 1=1}
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {3=3, 4=4}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
```

---

## Constraints

- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`
- `0 <= value <= 10^5`
- At most `2 * 10^5` calls will be made to `get` and `put`.

---

## Hints

1. A hash map alone gives O(1) get/put, but not O(1) eviction of the LRU item.
2. A doubly-linked list maintains order by recency efficiently.
3. Combine a hash map (key → node) with a doubly-linked list (ordered by recency).
4. Use sentinel head/tail nodes to simplify edge cases.

---

## Function Signature

### Python
```python
class LRUCache:
    def __init__(self, capacity: int):
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass
```

### JavaScript
```javascript
class LRUCache {
    constructor(capacity) {}
    get(key) {}
    put(key, value) {}
}
```

### Java
```java
class LRUCache {
    public LRUCache(int capacity) {}
    public int get(int key) {}
    public void put(int key, int value) {}
}
```

### C++
```cpp
class LRUCache {
public:
    LRUCache(int capacity) {}
    int get(int key) {}
    void put(int key, int value) {}
};
```

---

## Evaluation Criteria

1. **Correctness** (60 points) — All test cases pass
2. **Time Complexity** (30 points) — O(1) average for both `get` and `put`
3. **Code Quality** (10 points) — Clean implementation, proper encapsulation
