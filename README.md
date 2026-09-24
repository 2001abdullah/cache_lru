# LRU Cache

A simple Least Recently Used (LRU) cache written in Python.

It stores values in a dictionary and keeps them in recency order using a doubly linked list. That lets `get()` and `put()` work in average O(1) time.

## Files

- `lru_cache.py` — basic LRU cache
- `lru_cache_ttl.py` — LRU cache with optional expiration
- `example.py` — basic usage example
- `example_ttl.py` — TTL demonstration
- `test_lru_cache.py` — unit tests

## How it works

The cache keeps two things:

1. A dictionary: `key -> node`
2. A doubly linked list: keeps the newest items at the front and the oldest at the back

When a key is accessed with `get()`, it is moved to the front. When the cache is full, the oldest item at the back is removed.

## Core methods

### `get(key)`

- returns the value if the key exists
- returns `-1` if it does not exist
- updates the item to be the most recently used

### `put(key, value)`

- inserts a new key/value pair
- updates the value if the key already exists
- removes the least recently used item if the cache is full

## TTL version

`lru_cache_ttl.py` extends the main cache with expiration support.

You can do this:

```python
from lru_cache_ttl import LRUCacheTTL

cache = LRUCacheTTL(capacity=2, default_ttl=1.0)
cache.put("A", 10)
cache.put("B", 20)

print(cache.get("A"))
```

You can also set a custom TTL per item:

```python
cache.put("C", 30, ttl=0.5)
```

A value with an expired TTL is treated like a cache miss.

## Run it

```bash
cd e:\lru_cache
python example.py
python example_ttl.py
python -m unittest -q
```

If your system uses a different Python path, run the explicit interpreter instead:

```bash
& "C:\Users\User pc\.local\bin\python3.14.exe" example.py
& "C:\Users\User pc\.local\bin\python3.14.exe" example_ttl.py
& "C:\Users\User pc\.local\bin\python3.14.exe" -m unittest -q
```

## Notes

This project is intentionally small and easy to read. The main idea is simple: keep fast lookups with a dictionary and keep eviction order with a linked list.
