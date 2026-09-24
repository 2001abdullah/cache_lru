"""LRU cache with optional TTL support."""

import time

from lru_cache import LRUCache, _Node


class LRUCacheTTL(LRUCache):
    def __init__(self, capacity: int, default_ttl: float | None = None):
        super().__init__(capacity)
        self.default_ttl = default_ttl
        self._expires_at = {}

    def _is_expired(self, key) -> bool:
        expiry = self._expires_at.get(key)
        return expiry is not None and time.monotonic() >= expiry

    def get(self, key):
        node = self._map.get(key)
        if node is None:
            return -1

        if self._is_expired(key):
            self._remove(node)
            del self._map[key]
            del self._expires_at[key]
            return -1

        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key, value, ttl: float | None = "__default__") -> None:
        if ttl == "__default__":
            ttl = self.default_ttl

        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            self._remove(existing)
            self._add_front(existing)
        else:
            if len(self._map) >= self.capacity:
                lru_node = self._tail.prev
                self._remove(lru_node)
                del self._map[lru_node.key]
                self._expires_at.pop(lru_node.key, None)

            node = _Node(key, value)
            self._map[key] = node
            self._add_front(node)

        self._expires_at[key] = None if ttl is None else time.monotonic() + ttl

    def purge_expired(self) -> int:
        expired_keys = [k for k in list(self._map) if self._is_expired(k)]
        for k in expired_keys:
            node = self._map[k]
            self._remove(node)
            del self._map[k]
            del self._expires_at[k]
        return len(expired_keys)
