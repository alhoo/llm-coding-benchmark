"""
Reference solution for LFU Cache.
Uses a hash map per frequency bucket (OrderedDict for LRU ordering within each bucket).
Time Complexity: O(1) average for get and put
Space Complexity: O(capacity)
"""

from collections import OrderedDict, defaultdict


class LFUCache:
    """
    LFU Cache with O(1) get/put.

    Data structures:
      - _val:       key → value
      - _freq:      key → current access frequency
      - _freq_keys: freq → OrderedDict of keys (insertion order = LRU order)
      - _min_freq:  current minimum frequency across all keys

    On access (get or put-update), a key moves from its current frequency
    bucket to freq+1. If the old bucket was min_freq and is now empty,
    min_freq increments.

    On eviction, the first (oldest) key in _freq_keys[_min_freq] is removed.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._min_freq = 0
        self._val: dict[int, int] = {}
        self._freq: dict[int, int] = {}
        self._freq_keys: dict[int, OrderedDict] = defaultdict(OrderedDict)

    def _touch(self, key: int) -> None:
        freq = self._freq[key]
        del self._freq_keys[freq][key]
        if not self._freq_keys[freq]:
            del self._freq_keys[freq]
            if self._min_freq == freq:
                self._min_freq += 1
        self._freq[key] = freq + 1
        self._freq_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self._val:
            return -1
        self._touch(key)
        return self._val[key]

    def put(self, key: int, value: int) -> None:
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


if __name__ == "__main__":
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    assert lfu.get(1) == 1
    lfu.put(3, 3)
    assert lfu.get(2) == -1
    assert lfu.get(3) == 3
    lfu.put(4, 4)
    assert lfu.get(1) == -1
    assert lfu.get(3) == 3
    assert lfu.get(4) == 4

    lfu0 = LFUCache(0)
    lfu0.put(0, 0)
    assert lfu0.get(0) == -1

    print("All tests passed!")
