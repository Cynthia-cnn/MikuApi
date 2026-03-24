# mikuapi/response.py

import json


class JSONResponse:
    def __init__(self, content, status=200):
        self.content = content
        self.status = status
        self.content_type = "application/json"

    def render(self):
        return json.dumps(self.content).encode()


class HTMLResponse:
    def __init__(self, content, status=200):
        self.content = content
        self.status = status
        self.content_type = "text/html"

    def render(self):
        return self.content