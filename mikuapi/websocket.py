

import json


class WebSocket:
    def __init__(self, scope, receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send

    async def accept(self):
        await self.send({
            "type": "websocket.accept"
        })

    async def receive_text(self):
        message = await self.receive()
        return message.get("text")

    async def send_text(self, data):
        await self.send({
            "type": "websocket.send",
            "text": data
        })

    async def close(self):
        await self.send({
            "type": "websocket.close"
        })