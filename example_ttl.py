"""Simple TTL example for the LRU cache."""

import time

from lru_cache_ttl import LRUCacheTTL


def main():
    cache = LRUCacheTTL(capacity=2)
    cache.put("A", 10, ttl=0.5)
    cache.put("B", 20)
    print("Before expiry ->", cache.get("A"))

    time.sleep(0.6)
    print("After expiry ->", cache.get("A"))
    print("B still alive ->", cache.get("B"))

    cache2 = LRUCacheTTL(capacity=2, default_ttl=0.3)
    cache2.put("X", 100)
    cache2.put("Y", 200, ttl=None)

    time.sleep(0.4)
    print("X expired ->", cache2.get("X"))
    print("Y never expired ->", cache2.get("Y"))


if __name__ == "__main__":
    main()
