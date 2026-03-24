

import json
from mikuapi.exceptions import HTTPException
from mikuapi.logger import logger


class ErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)

        except HTTPException as e:
            response = {
                "error": e.detail,
                "status": e.status
            }

            await send({
                "type": "http.response.start",
                "status": e.status,
                "headers": [(b"content-type", b"application/json")]
            })

            await send({
                "type": "http.response.body",
                "body": json.dumps(response).encode()
            })

        except Exception as e:
            logger.error(str(e))

            response = {
                "error": "Internal Server Error"
            }

            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"application/json")]
            })

            await send({
                "type": "http.response.body",
                "body": json.dumps(response).encode()
            })