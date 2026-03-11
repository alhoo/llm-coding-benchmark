# Problem P12: LFU Cache

## Problem Statement

Design a data structure for a **Least Frequently Used (LFU)** cache.

Implement the `LFUCache` class:

- `LFUCache(int capacity)` — Initialize the cache with **positive** size `capacity`.
- `int get(int key)` — Return the value of the `key` if it exists, otherwise return `-1`.
- `void put(int key, int value)` — Update the value of `key` if it exists, or insert the `key-value` pair. When the cache reaches `capacity`, **evict the least frequently used** key before inserting a new one. If there is a tie in frequency, evict the **least recently used** key among the tied keys.

Both `get` and `put` operations **increment the frequency** of the accessed key.

The functions `get` and `put` must each run in **O(1) average time complexity**.

---

## Examples

### Example 1:
```
Input:
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, 3, null, 1, 3, 4]

Explanation:
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache={1: freq=1}
lfu.put(2, 2);   // cache={1: freq=1, 2: freq=1}
lfu.get(1);      // return 1, key 1 freq becomes 2
                  // cache={1: freq=2, 2: freq=1}
lfu.put(3, 3);   // key 2 is LFU (freq=1), evict key 2
                  // cache={1: freq=2, 3: freq=1}
lfu.get(2);      // return -1 (not found)
lfu.get(3);      // return 3, key 3 freq becomes 2
lfu.put(4, 4);   // key 1 and 3 both have freq=2
                  // key 1 was accessed more recently than key 3?
                  // Actually: key 3 was accessed in get(3), key 1 in get(1) before that
                  // key 1 is LRU among freq=2 keys → evict key 1
                  // cache={3: freq=2, 4: freq=1}
                  // Wait: actually key 3 get was more recent, so key 1 is LRU → evict key 1
lfu.get(1);      // return -1 (evicted)
lfu.get(3);      // return 3
lfu.get(4);      // return 4
```

### Example 2:
```
Input:
["LFUCache", "put", "get"]
[[0], [0, 0], [0]]

Output:
[null, null, -1]

Explanation: Capacity 0 means nothing can be stored.
```

---

## Constraints

- `0 <= capacity <= 10^4`
- `0 <= key <= 10^5`
- `0 <= value <= 10^9`
- At most `2 * 10^5` calls will be made to `get` and `put`.

---

## Hints

1. You need to track both **frequency** and **recency** for each key.
2. Maintain a hash map from frequency → ordered collection of keys at that frequency.
3. Use `collections.OrderedDict` (or a doubly-linked list) for each frequency bucket to get O(1) LRU eviction within a bucket.
4. Track `min_freq` to know which frequency bucket to evict from.
5. When a key's frequency increases, move it from the old bucket to the new bucket. If the old bucket becomes empty and was the `min_freq`, increment `min_freq`.

---

## Function Signature

### Python
```python
class LFUCache:
    def __init__(self, capacity: int):
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass
```

### JavaScript
```javascript
class LFUCache {
    constructor(capacity) {}
    get(key) {}
    put(key, value) {}
}
```

### Java
```java
class LFUCache {
    public LFUCache(int capacity) {}
    public int get(int key) {}
    public void put(int key, int value) {}
}
```

### C++
```cpp
class LFUCache {
public:
    LFUCache(int capacity) {}
    int get(int key) {}
    void put(int key, int value) {}
};
```

---

## Evaluation Criteria

1. **Correctness** (50 points) — All test cases pass, proper LFU eviction with LRU tie-breaking
2. **Time Complexity** (35 points) — O(1) average for both `get` and `put`
3. **Code Quality** (15 points) — Clean frequency-bucket design, proper encapsulation
