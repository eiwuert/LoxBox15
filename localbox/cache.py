from time import time


class TimedCache(object):
    """
    TimedCache is a dictionary with a timeout. The class is initalised with a
    timeout, and data will be invalid after the timeout has expired. Invalid
    data will only be removed from the cache after it is referenced by get()
    or the clean() function is called.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TimedCache, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, timeout=600):
        self.cache = {}
        self.timeout = timeout

    def invalidate(self, key):
        """
        Invalidates an entry in the cache by removing it
        """
        del self.cache[key]

    def add(self, key, value):
        """
        Adds an key and value pair to the cache.
        """
        store = (value, time() + self.timeout)
        self.cache[key] = store

    def get(self, key):
        """
        Returns the value of a certain key in the cache. Returns None when key
        is not found or if the timeout has expired. Also cleans the entry in
        the latter case
        """
        if key in self.cache:
            (value, date) = self.cache[key]
            if date > time():
                return value
            del self.cache[key]
        return None

    def clean(self):
        """
        check every key-value pair in the database and remove expired pairs.
        """
        for key, store in self.cache:
            date = store[1]
            if date < time():
                del self.cache[key]
