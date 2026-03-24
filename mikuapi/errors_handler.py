# mikuapi/errors_handler.py

class ExceptionHandler:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            response = {
                "error": str(e),
                "type": e.__class__.__name__
            }

            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"application/json")]
            })

            import json
            await send({
                "type": "http.response.body",
                "body": json.dumps(response).encode()
            })