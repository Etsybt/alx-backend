#!/usr/bin/python3
"""
1-fifo_cache
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    a FIFO caching system that inherits from BaseCaching
    """
    def __init__(self):
        """
        Initialize
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.order.append(key)
        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = self.order.pop(0)
            del self.cache_data[first_key]
            print(f"DISCARD: {first_key}")

    def get(self, key):
        """
        Get an item by key
        """
        return self.cache_data.get(key) if key is not None else None
