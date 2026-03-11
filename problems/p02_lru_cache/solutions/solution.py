"""
Reference solution for LRU Cache problem.
Time Complexity: O(1) average for both get and put
Space Complexity: O(capacity)
"""


class LRUCache:
    """
    LRU Cache using a doubly-linked list + hash map.

    The doubly-linked list maintains insertion order (MRU at head, LRU at tail).
    The hash map provides O(1) key lookup.
    Sentinel head/tail nodes eliminate null checks.
    """

    class _Node:
        __slots__ = ("key", "val", "prev", "next")

        def __init__(self, key: int = 0, val: int = 0):
            self.key = key
            self.val = val
            self.prev: "LRUCache._Node | None" = None
            self.next: "LRUCache._Node | None" = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, LRUCache._Node] = {}

        self._head = self._Node()  # MRU sentinel
        self._tail = self._Node()  # LRU sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: "_Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: "_Node") -> None:
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

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
        node = self._Node(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.capacity:
            lru = self._tail.prev
            self._remove(lru)
            del self.cache[lru.key]


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)          # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)          # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
    print("All tests passed!")
