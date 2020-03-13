from pymemcache.client import base

TIME = 60 * 60


class Cache:
    def __init__(self, full_path=('127.0.0.1', 11211)):
        self.cache = base.Client(full_path)

    def cache_set(self, key, value, time=TIME):
        self.cache.set(key, value, time)

    def cache_get(self, key):
        return self.cache.get(key)
