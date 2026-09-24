"""
Unit tests for LRUCache.

Run with:  python3 -m unittest test_lru_cache.py -v
"""

import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_spec_example(self):
        """Exact example from the task description."""
        cache = LRUCache(2)
        cache.put("A", 10)
        cache.put("B", 20)
        self.assertEqual(cache.get("A"), 10)
        cache.put("C", 30)                 # evicts B
        self.assertEqual(cache.get("B"), -1)
        self.assertEqual(cache.get("C"), 30)
        self.assertEqual(cache.get("A"), 10)

    def test_get_missing_key_returns_minus_one(self):
        cache = LRUCache(3)
        self.assertEqual(cache.get("nope"), -1)

    def test_put_updates_existing_key(self):
        cache = LRUCache(2)
        cache.put("A", 1)
        cache.put("A", 2)
        self.assertEqual(cache.get("A"), 2)
        self.assertEqual(len(cache), 1)

    def test_successful_get_marks_most_recently_used(self):
        cache = LRUCache(2)
        cache.put("A", 1)
        cache.put("B", 2)
        cache.get("A")          # A is now MRU, B is LRU
        cache.put("C", 3)       # should evict B, not A
        self.assertEqual(cache.get("A"), 1)
        self.assertEqual(cache.get("B"), -1)
        self.assertEqual(cache.get("C"), 3)

    def test_eviction_order_with_repeated_updates(self):
        cache = LRUCache(2)
        cache.put("A", 1)
        cache.put("B", 2)
        cache.put("A", 10)      # updating A also refreshes recency
        cache.put("C", 3)       # should evict B, not A
        self.assertEqual(cache.get("A"), 10)
        self.assertEqual(cache.get("B"), -1)
        self.assertEqual(cache.get("C"), 3)

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("A", 1)
        cache.put("B", 2)       # evicts A immediately
        self.assertEqual(cache.get("A"), -1)
        self.assertEqual(cache.get("B"), 2)

    def test_invalid_capacity_raises(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-5)

    def test_len_never_exceeds_capacity(self):
        cache = LRUCache(3)
        for i in range(10):
            cache.put(i, i)
            self.assertLessEqual(len(cache), 3)

    def test_keys_order_reflects_recency(self):
        cache = LRUCache(3)
        cache.put("A", 1)
        cache.put("B", 2)
        cache.put("C", 3)
        cache.get("A")
        self.assertEqual(cache.keys_most_to_least_recent(), ["A", "C", "B"])


if __name__ == "__main__":
    unittest.main()
