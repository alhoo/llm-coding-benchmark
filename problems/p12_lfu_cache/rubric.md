# Evaluation Rubric: P12 - LFU Cache

## Total Points: 100

---

## 1. Correctness (50 points)

| Test Case | Points | Description |
|-----------|--------|-------------|
| Basic LFU eviction | 10 | Evict key with lowest frequency |
| Frequency tie-breaking | 15 | Among same-frequency keys, evict the LRU one |
| Overwrite updates frequency | 10 | `put` on existing key increments frequency |
| Capacity 0 / Capacity 1 | 5 | Edge cases for degenerate capacities |
| Promote through frequencies | 5 | High-frequency key survives multiple evictions |
| Evict and reinsert | 5 | Re-inserted key starts with freq=1 |

**Scoring**:
- Pass all: 50 points
- Fail 1 case: 35 points
- Fail 2 cases: 20 points
- Fail 3+ cases: 0 points

---

## 2. Time Complexity (35 points)

### Expected: O(1) average for both `get` and `put`

| Implementation | Points | Description |
|----------------|--------|-------------|
| HashMap + frequency-bucketed OrderedDicts | 35 | Optimal O(1) for all operations |
| HashMap + doubly-linked list per frequency | 35 | Also O(1), manual linked list variant |
| HashMap + sorted structure (e.g. SortedList) | 15 | O(log n) — suboptimal |
| Linear scan for min frequency | 5 | O(n) — fails requirement |

**Verification Method**:
- Timing test: 100,000 operations should complete in < 2 seconds
- Check for linear scans over keys or frequencies

---

## 3. Code Quality (15 points)

### Design (8 points)
- ✅ **8 points**: Clean frequency-bucket architecture with O(1) min_freq tracking
- ⚠️ **4 points**: Works but overly complex or uses non-standard patterns
- ❌ **0 points**: Incorrect architecture

### Edge Cases (4 points)
- ✅ **4 points**: Handles capacity 0, reinsert after eviction, overwrite semantics
- ❌ **0 points**: Crashes on edge cases

### Best Practices (3 points)
- ✅ **3 points**: Proper encapsulation, clear method naming, no global state
- ❌ **0 points**: Poor naming, global mutable state

---

## Common LLM Failures

### ❌ Failure Pattern 1: Forgetting to Update min_freq

```python
def _touch(self, key):
    freq = self.freq[key]
    del self.freq_keys[freq][key]
    # ❌ Forgot: if freq_keys[freq] is now empty AND freq == min_freq,
    #    then min_freq must be incremented
    self.freq[key] = freq + 1
    self.freq_keys[freq + 1][key] = None
```

**Score**: 35/100 (Evicts wrong key when min_freq bucket is stale)

---

### ❌ Failure Pattern 2: put() Doesn't Increment Frequency for Existing Keys

```python
def put(self, key, value):
    if key in self.val:
        self.val[key] = value  # ❌ Doesn't call _touch(key) — frequency stays the same
        return
```

**Score**: 45/100 (Overwritten keys get evicted prematurely)

---

### ❌ Failure Pattern 3: O(n) Eviction via Scanning All Keys

```python
def put(self, key, value):
    if len(self.val) >= self.capacity:
        # ❌ Scans all keys to find minimum frequency
        lfu_key = min(self.freq, key=self.freq.get)
        del self.val[lfu_key]
```

**Score**: 60/100 (Correct but O(n) eviction)

---

## ✅ Reference Solution

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._min_freq = 0
        self._val = {}
        self._freq = {}
        self._freq_keys = defaultdict(OrderedDict)

    def _touch(self, key):
        freq = self._freq[key]
        del self._freq_keys[freq][key]
        if not self._freq_keys[freq]:
            del self._freq_keys[freq]
            if self._min_freq == freq:
                self._min_freq += 1
        self._freq[key] = freq + 1
        self._freq_keys[freq + 1][key] = None

    def get(self, key):
        if key not in self._val:
            return -1
        self._touch(key)
        return self._val[key]

    def put(self, key, value):
        if self.capacity <= 0:
            return
        if key in self._val:
            self._val[key] = value
            self._touch(key)
            return
        if len(self._val) >= self.capacity:
            evict_key, _ = self._freq_keys[self._min_freq].popitem(last=False)
            if not self._freq_keys[self._min_freq]:
                del self._freq_keys[self._min_freq]
            del self._val[evict_key]
            del self._freq[evict_key]
        self._val[key] = value
        self._freq[key] = 1
        self._freq_keys[1][key] = None
        self._min_freq = 1
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(1) average
- ✅ Space Complexity: O(capacity)
