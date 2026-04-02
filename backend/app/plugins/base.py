"""Plugin base classes for ClawSafe extensibility."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PluginMeta:
    """Plugin metadata."""
    name: str = ""
    version: str = "0.1.0"
    description: str = ""
    plugin_type: str = ""  # "scanner", "fixer", "notifier"
    sandboxed: bool = True  # Execute in isolated subprocess


class ScannerPlugin(ABC):
    """Base class for custom scanner plugins."""
    meta = PluginMeta()

    @abstractmethod
    async def scan(self, config: dict | None) -> list[dict]:
        """Run custom scan. Return list of findings."""
        ...

    def get_category(self) -> str:
        """Which scoring category this plugin affects."""
        return "security"


class FixerPlugin(ABC):
    """Base class for custom fixer plugins."""
    meta = PluginMeta()

    @abstractmethod
    async def fix(self, action_id: str, config: dict) -> dict:
        """Apply fix. Return {success: bool, message: str}."""
        ...

    @abstractmethod
    def supported_actions(self) -> list[str]:
        """Return action IDs this plugin handles."""
        ...


class NotifierPlugin(ABC):
    """Base class for custom notification plugins."""
    meta = PluginMeta()

    @abstractmethod
    async def send(self, event_type: str, payload: dict) -> bool:
        """Send notification. Return True on success."""
        ...
