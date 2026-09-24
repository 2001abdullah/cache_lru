"""Simple example showing the basic LRU behavior."""

from lru_cache import LRUCache


def main():
    cache = LRUCache(2)

    print("Capacity = 2")
    cache.put("A", 10)
    cache.put("B", 20)
    print("get(A) ->", cache.get("A"))

    cache.put("C", 30)
    print("get(B) after insert C ->", cache.get("B"))
    print("get(C) ->", cache.get("C"))
    print("get(A) ->", cache.get("A"))

    print("\nExtra example:")
    cache2 = LRUCache(3)
    cache2.put("x", 1)
    cache2.put("y", 2)
    cache2.put("z", 3)
    cache2.get("x")
    cache2.put("w", 4)
    print("get(y) ->", cache2.get("y"))
    print("get(w) ->", cache2.get("w"))

    try:
        LRUCache(0)
    except ValueError as e:
        print("\nInvalid capacity raises ValueError:", e)


if __name__ == "__main__":
    main()
