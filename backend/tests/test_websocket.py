"""Tests for WebSocket and event bus."""

import pytest

from app.services.event_bus import emit, subscribe


@pytest.mark.anyio
async def test_event_bus_emits_to_subscribers():
    received = []

    async def handler(event_type: str, data: dict) -> None:
        received.append((event_type, data))

    subscribe(handler)
    await emit("test_event", {"key": "value"})

    assert len(received) >= 1
    assert received[-1] == ("test_event", {"key": "value"})


@pytest.mark.anyio
async def test_ws_manager_broadcast():
    from app.services.ws_manager import manager

    # With no connections, broadcast should not error
    await manager.broadcast({"type": "test", "data": {}})
