# mikuapi/middleware/logging.py

import time


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start = time.time()

        await self.app(scope, receive, send)

        duration = (time.time() - start) * 1000
        print(f"[{scope['method']}] {scope['path']} - {duration:.2f}ms")