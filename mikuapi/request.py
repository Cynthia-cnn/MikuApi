import json
from urllib.parse import parse_qs


class Request:
    def __init__(self, scope, receive):
        self.scope = scope
        self.receive = receive

        self.method = scope["method"]
        self.path = scope["path"]

        self._query = None
        self._body = None
        self._headers = None

    def query_params(self):
        if self._query is None:
            raw = self.scope.get("query_string", b"").decode()
            parsed = parse_qs(raw)

            self._query = {
                k: v if len(v) > 1 else v[0]
                for k, v in parsed.items()
            }

        return self._query

    async def body(self):
        if self._body is None:
            body = b""
            more = True

            while more:
                message = await self.receive()
                body += message.get("body", b"")
                more = message.get("more_body", False)

            self._body = body

        return self._body

    async def json(self):
        body = await self.body()
        if not body:
            return {}

        content_type = self.headers().get("content-type", "")

        if "application/json" in content_type:
            try:
                return json.loads(body.decode())
            except:
                raise ValueError("Invalid JSON body")

        return {}

    def headers(self):
        if self._headers is None:
            headers = {}
            for k, v in self.scope.get("headers", []):
                headers[k.decode()] = v.decode()
            self._headers = headers
        return self._headers