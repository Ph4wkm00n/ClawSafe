"""WebSocket connection manager — broadcasts events to connected clients."""

from __future__ import annotations

import logging
from typing import Set

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("WebSocket connected (%d total)", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        logger.info("WebSocket disconnected (%d remaining)", len(self.active_connections))

    async def broadcast(self, message: dict) -> None:
        """Broadcast message to all connected clients."""
        dead = set()
        for ws in self.active_connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.active_connections.discard(ws)

    async def handle_event(self, event_type: str, data: dict) -> None:
        """Event bus handler — broadcasts events to WebSocket clients."""
        await self.broadcast({"type": event_type, "data": data})


manager = ConnectionManager()
