# mikuapi/app.py

from .routing import Router
from .asgi import ASGIApp


class MikuAPI:
    def __init__(self):
        self.router = Router()
        self.asgi = ASGIApp(self.router)
        self.middleware_stack = self.asgi

    def get(self, path, response_model=None):
        return self.router.get(path, response_model=response_model)

    def post(self, path, response_model=None):
        return self.router.post(path, response_model=response_model)

    def add_middleware(self, middleware_class):
        self.middleware_stack = middleware_class(self.middleware_stack)

    async def __call__(self, scope, receive, send):
        await self.middleware_stack(scope, receive, send)