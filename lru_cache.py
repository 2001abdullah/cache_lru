"""Simple LRU cache implementation."""


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self._map = {}

        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _Node) -> None:
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def get(self, key):
        node = self._map.get(key)
        if node is None:
            return -1

        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key, value) -> None:
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._remove(existing)
            self._add_front(existing)
            return

        if len(self._map) >= self.capacity:
            lru_node = self._tail.prev
            self._remove(lru_node)
            del self._map[lru_node.key]

        node = _Node(key, value)
        self._map[key] = node
        self._add_front(node)

    def __len__(self) -> int:
        return len(self._map)

    def keys_most_to_least_recent(self):
        keys = []
        node = self._head.next
        while node is not self._tail:
            keys.append(node.key)
            node = node.next
        return keys
