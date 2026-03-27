class ExceptionHandler:
    def __init__(self, app, debug=True):
        self.app = app
        self.debug = debug

    async def __call__(self, scope, receive, send):
        try:
            await self.app(scope, receive, send)

        except Exception as e:
            import json

            # DEFAULT
            status = 500
            message = "Internal Server Error"

    
            if isinstance(e, HTTPException):
                status = e.status_code
                message = e.detail

            
            elif isinstance(e, ValueError):
                status = 400
                message = str(e)


            if self.debug:
                message = str(e)

            response = {
                "error": message,
                "type": e.__class__.__name__
            }

            await send({
                "type": "http.response.start",
                "status": status,
                "headers": [(b"content-type", b"application/json")]
            })

            await send({
                "type": "http.response.body",
                "body": json.dumps(response).encode()
            })