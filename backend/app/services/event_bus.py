"""In-process event bus for real-time broadcasting."""

from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

EventHandler = Callable[[str, dict], Coroutine[Any, Any, None]]

_handlers: list[EventHandler] = []


def subscribe(handler: EventHandler) -> None:
    """Register an event handler."""
    _handlers.append(handler)


async def emit(event_type: str, data: dict) -> None:
    """Emit an event to all subscribers."""
    for handler in _handlers:
        try:
            await handler(event_type, data)
        except Exception as e:
            logger.warning("Event handler failed for %s: %s", event_type, e)
