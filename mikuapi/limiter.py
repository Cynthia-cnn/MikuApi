# mikuapi/limiter.py

import time


class RateLimiter:
    def __init__(self):
        self.storage = {}

    def is_allowed(self, key, limit, window):
        now = time.time()

        if key not in self.storage:
            self.storage[key] = []

        requests = self.storage[key]

        # hapus request lama
        self.storage[key] = [t for t in requests if now - t < window]

        if len(self.storage[key]) >= limit:
            return False

        self.storage[key].append(now)
        return True


limiter = RateLimiter()


def limit(max_requests=5, window=1):
    def decorator(func):
        func._rate_limit = (max_requests, window)
        return func
    return decorator