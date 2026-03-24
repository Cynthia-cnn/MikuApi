# mikuapi/asgi.py

class ASGIApp:
    def __init__(self, router):
        self.router = router

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            response = await self.router.resolve(scope, receive, send)

            if response:
                await send({
                    "type": "http.response.start",
                    "status": response.status,
                    "headers": [
                        (b"content-type", response.content_type.encode())
                    ],
                })

                await send({
                    "type": "http.response.body",
                    "body": response.render(),
                })

        elif scope["type"] == "websocket":
            await self.router.resolve(scope, receive, send)