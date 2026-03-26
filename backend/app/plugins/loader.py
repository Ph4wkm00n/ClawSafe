"""Plugin loader — discovers and loads plugins from the plugins directory."""

from __future__ import annotations

import importlib
import importlib.util
import logging
from pathlib import Path

from app.plugins.base import FixerPlugin, NotifierPlugin, ScannerPlugin

logger = logging.getLogger(__name__)

_scanner_plugins: list[ScannerPlugin] = []
_fixer_plugins: list[FixerPlugin] = []
_notifier_plugins: list[NotifierPlugin] = []


def load_plugins(plugins_dir: str = "plugins") -> dict:
    """Discover and load all plugins from the given directory."""
    directory = Path(plugins_dir)
    if not directory.exists():
        logger.info("Plugins directory not found: %s", plugins_dir)
        return {"loaded": 0, "errors": 0}

    loaded = 0
    errors = 0

    for py_file in sorted(directory.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(py_file.stem, str(py_file))
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if not isinstance(attr, type):
                    continue
                if issubclass(attr, ScannerPlugin) and attr is not ScannerPlugin:
                    _scanner_plugins.append(attr())
                    loaded += 1
                    logger.info("Loaded scanner plugin: %s", attr_name)
                elif issubclass(attr, FixerPlugin) and attr is not FixerPlugin:
                    _fixer_plugins.append(attr())
                    loaded += 1
                elif issubclass(attr, NotifierPlugin) and attr is not NotifierPlugin:
                    _notifier_plugins.append(attr())
                    loaded += 1
        except Exception as e:
            logger.warning("Failed to load plugin %s: %s", py_file.name, e)
            errors += 1

    logger.info("Loaded %d plugins (%d errors)", loaded, errors)
    return {"loaded": loaded, "errors": errors}


def get_scanner_plugins() -> list[ScannerPlugin]:
    return _scanner_plugins


def get_fixer_plugins() -> list[FixerPlugin]:
    return _fixer_plugins


def get_notifier_plugins() -> list[NotifierPlugin]:
    return _notifier_plugins


def list_all_plugins() -> list[dict]:
    """List all loaded plugins with metadata."""
    result = []
    for p in _scanner_plugins:
        result.append({"name": p.meta.name, "type": "scanner", "version": p.meta.version, "description": p.meta.description})
    for p in _fixer_plugins:
        result.append({"name": p.meta.name, "type": "fixer", "version": p.meta.version, "description": p.meta.description})
    for p in _notifier_plugins:
        result.append({"name": p.meta.name, "type": "notifier", "version": p.meta.version, "description": p.meta.description})
    return result
