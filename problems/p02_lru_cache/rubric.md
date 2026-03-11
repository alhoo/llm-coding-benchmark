# Evaluation Rubric: P02 - LRU Cache

## Total Points: 100

---

## 1. Correctness (60 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Basic get/put | 10 | Insert and retrieve values |
| LRU eviction | 15 | Evict least recently used on overflow |
| Access updates recency | 15 | `get` moves key to most-recently-used |
| Capacity = 1 | 10 | Single-element cache edge case |
| Overwrite existing key | 10 | `put` on existing key updates value and recency |

**Scoring**:
- Pass all: 60 points
- Fail 1 case: 45 points
- Fail 2 cases: 25 points
- Fail 3+ cases: 0 points

---

## 2. Time Complexity (30 points)

### Expected Complexity: O(1) average for both `get` and `put`

| Implementation | Points | Description |
|----------------|--------|-------------|
| HashMap + Doubly Linked List | 30 | Optimal O(1) both operations |
| `collections.OrderedDict` | 25 | Correct complexity, uses stdlib shortcut |
| HashMap + array/list | 10 | O(n) for eviction — fails requirement |
| Linear search | 0 | O(n) — fails requirement |

**Verification Method**:
- Timing test: 10,000 operations on capacity-1000 cache should be fast
- Code inspection: check for linear scans

---

## 3. Space Complexity (0 points, but noted)

- **O(capacity)**: Expected
- **O(n)** where n >> capacity: Red flag

---

## 4. Code Quality (10 points)

### Design (5 points)
- ✅ **5 points**: Clean node-based doubly linked list with sentinels
- ⚠️ **3 points**: Works but uses Python `OrderedDict` (less educational)
- ❌ **0 points**: Array-based with linear scan

### Correctness of Eviction Logic (3 points)
- ✅ **3 points**: Both `get` and `put` correctly update recency
- ⚠️ **1 point**: Only `put` updates recency

### Best Practices (2 points)
- ✅ **2 points**: Proper encapsulation, clear method naming
- ❌ **0 points**: Global state, poor naming

---

## Common LLM Failures

### ❌ Failure Pattern 1: Forgetting `get` Updates Recency

```python
def get(self, key: int) -> int:
    if key in self.cache:
        return self.cache[key]  # ❌ Doesn't move to MRU position!
    return -1
```

**Score**: 45/100 (Fails "access updates recency" test)

---

### ❌ Failure Pattern 2: O(n) Eviction

```python
def put(self, key: int, value: int) -> None:
    if len(self.cache) >= self.capacity:
        # Find LRU by scanning usage times — O(n)!
        lru_key = min(self.usage_time, key=self.usage_time.get)
        del self.cache[lru_key]
```

**Score**: 60/100 (Correct but O(n))

---

## ✅ Reference Solution

```python
class LRUCache:
    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = self.Node()  # sentinel head (MRU side)
        self.tail = self.Node()  # sentinel tail (LRU side)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = self.Node(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

**Score**: 100/100
