#!/usr/bin/python3
"""
LFUCache module
"""
from base_caching import BaseCaching
from collections import OrderedDict, defaultdict


class LFUCache(BaseCaching):
    """
    LFU caching system that inherits from BaseCaching
    """

    def __init__(self):
        """
        Initialize
        """
        super().__init__()
        self.cache_data = {}
        self.frequency = defaultdict(int)
        self.usage_order = OrderedDict()

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.usage_order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used item
                min_freq = min(self.frequency.values())
                lfu_keys = [
                    k for k, freq in
                    self.frequency.items() if freq == min_freq]

                if len(lfu_keys) == 1:
                    key_to_discard = lfu_keys[0]
                else:
                    # If there is more than one LFU key, use LRU among them
                    key_to_discard = next(
                        k for k in self.usage_order if k in lfu_keys)

                del self.cache_data[key_to_discard]
                del self.frequency[key_to_discard]
                del self.usage_order[key_to_discard]
                print(f"DISCARD: {key_to_discard}")

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.usage_order[key] = None

    def get(self, key):
        """
        Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        self.frequency[key] += 1
        self.usage_order.move_to_end(key)
        return self.cache_data[key]
