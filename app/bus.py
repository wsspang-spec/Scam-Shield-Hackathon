"""Tiny broadcaster for dashboard websockets."""
from __future__ import annotations

import asyncio
import json

from fastapi import WebSocket


class Bus:
    def __init__(self):
        self._clients: set[WebSocket] = set()
        self.history: list[dict] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._clients.add(ws)
        for ev in self.history[-200:]:
            await ws.send_text(json.dumps(ev))

    def disconnect(self, ws: WebSocket) -> None:
        self._clients.discard(ws)

    async def publish(self, event: dict) -> None:
        self.history.append(event)
        payload = json.dumps(event, default=str)
        dead = []
        for ws in list(self._clients):
            try:
                await ws.send_text(payload)
            except Exception:  # noqa: BLE001
                dead.append(ws)
        for ws in dead:
            self._clients.discard(ws)

    def reset(self) -> None:
        self.history.clear()


bus = Bus()
