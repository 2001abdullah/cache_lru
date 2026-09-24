# LRU Cache

A Least Recently Used (LRU) cache implementing `Cache(capacity)`, `get(key)`,
and `put(key, value)` in **O(1) average time**, written in Python 3
(standard library only — no external dependencies).

## Files

```
lru_cache.py          Core implementation: LRUCache class
lru_cache_ttl.py       Bonus: LRUCacheTTL, adds optional TTL/expiration
example.py             Runs the exact scenario from the task spec + a few
                        extra checks, prints every operation's result
example_ttl.py          Bonus: demonstrates TTL expiration behavior
test_lru_cache.py       Unit tests (unittest) covering every requirement
screenshots/            Real, unedited terminal output from running the
                         scripts above (see "Output screenshots" below)
```

## Data structures used, and why

Two structures work together:

1. **A hash map (`dict`)**: `key -> Node`. Gives O(1) average lookup,
   insert, and delete by key — this is what makes `get(key)` fast.
2. **A doubly linked list (DLL)** of nodes, ordered by recency: the node
   right after the `head` sentinel is the *most* recently used, and the
   node right before the `tail` sentinel is the *least* recently used.
   A DLL gives O(1) removal and insertion **at arbitrary positions**
   (as long as you already have a pointer to the node, which the hash
   map gives you) — that's what a plain array/list or a `dict` alone
   cannot do in O(1).

Neither structure alone is enough:
- A hash map alone has no concept of "order", so you couldn't find the
  least-recently-used entry without scanning everything — O(n).
- A linked list alone would need an O(n) scan to find a given key.

Combined, `map[key]` gives you the node in O(1), and the DLL lets you
move that node to the front (on a hit) or drop the node at the tail
(on eviction) in O(1) — hence O(1) average for both operations.

Two dummy sentinel nodes (`_head`, `_tail`) are used so insertion/removal
never has to special-case "is this the first/last real node?" — every
real node always has a valid `prev` and `next` to link against.

### How LRU ordering is maintained

- **`get(key)`**: if found, the node is unlinked from its current spot
  in the DLL and re-inserted right after `_head` (making it the most
  recently used), then its value is returned. Miss returns `-1` without
  touching the list.
- **`put(key, value)`**:
  - Key exists → update its value, then move it to the front (same as
    a successful `get`).
  - Key is new and the cache is at capacity → remove the node just
    before `_tail` (the actual least-recently-used entry) from both the
    DLL and the hash map, *then* insert the new node at the front.
  - Key is new and there's room → just insert at the front.

## Complexity

| Operation | Time (average) | Why |
|---|---|---|
| `get(key)` | **O(1)** | dict lookup + O(1) DLL unlink/relink |
| `put(key, value)` | **O(1)** | dict lookup/insert + O(1) DLL unlink/relink (+ O(1) eviction of the tail node when full) |
| Space | **O(capacity)** | one dict entry + one DLL node per cached key, bounded by `capacity` |

(`get`/`put` are O(1) *average* the same way Python `dict` operations are
described as O(1) average — amortized hash table behavior. There's no
scanning or sorting anywhere in this implementation.)

## How to run it

Requires Python 3.10+ (for the `X | None` type hint in the bonus file;
`lru_cache.py` itself works on any Python 3).

```bash
cd lru_cache

# Run the required-behavior example (matches the task's sample scenario)
python3 example.py

# Run the unit tests
python3 -m unittest test_lru_cache.py -v

# Bonus: TTL/expiration demo
python3 example_ttl.py
```

No install step is needed — everything is standard library.

## Output screenshots

`screenshots/` contains three PNGs, each a direct render of real terminal
output captured from actually running the commands above (not hand-typed
or edited):

- `output_main_example.png` — `python3 example.py`, matching the task's
  exact sample (`put`/`get` sequence, LRU eviction, `-1` for a missing/evicted
  key), plus a second capacity-3 walkthrough and the capacity-validation check.
- `output_unit_tests.png` — `python3 -m unittest test_lru_cache.py -v`,
  all 9 tests passing.
- `output_ttl_bonus.png` — `python3 example_ttl.py` (see bonus section below).

## Bonus: TTL / expiration support

`lru_cache_ttl.py` adds `LRUCacheTTL(LRUCache)`:

- `put(key, value, ttl=None)` — `ttl` is seconds until that entry expires.
  If omitted, it falls back to the cache's `default_ttl` (set in the
  constructor); pass `ttl=None` explicitly to make one entry never expire
  even if a default is set.
- **Expiration is checked lazily**, inside `get()`/`put()`: each key has
  an absolute expiry timestamp stored alongside it, and `get()` checks
  `time.monotonic() >= expiry` before returning a value. If expired, the
  entry is removed on the spot and treated as a cache miss (`-1`).
- An optional `purge_expired()` does an O(n) sweep to proactively drop
  every currently-expired entry, for callers who want memory reclaimed
  without waiting for a `get()`/LRU eviction to trigger it.

**Trade-offs of the lazy approach:**
- ✅ No background thread/timer needed; `get`/`put` stay O(1) average.
- ✅ Simple to reason about — expiration is just one extra `if` check.
- ⚠️ An expired entry that's never looked up again will sit in the cache
  (still counting toward `capacity`) until normal LRU pressure evicts it,
  or until `purge_expired()` is called. For a cache doing frequent
  reads/writes this is rarely noticeable; for a mostly-idle cache with a
  short TTL, memory can be reclaimed later than the TTL would suggest.
- An alternative (not implemented here) would be a background sweep
  thread or a min-heap of expiry times for proactive, timer-driven
  eviction — more moving parts, and unnecessary for most use cases.

See `example_ttl.py` and `screenshots/output_ttl_bonus.png` for the
expiration behavior in action.
