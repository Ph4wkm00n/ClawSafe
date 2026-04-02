"""Plugin loader — discovers and loads plugins from the plugins directory."""

from __future__ import annotations

import asyncio
import importlib
import importlib.util
import logging
from concurrent.futures import ProcessPoolExecutor
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
        result.append({
            "name": p.meta.name, "type": "scanner", "version": p.meta.version,
            "description": p.meta.description, "sandboxed": p.meta.sandboxed,
        })
    for p in _fixer_plugins:
        result.append({
            "name": p.meta.name, "type": "fixer", "version": p.meta.version,
            "description": p.meta.description, "sandboxed": p.meta.sandboxed,
        })
    for p in _notifier_plugins:
        result.append({
            "name": p.meta.name, "type": "notifier", "version": p.meta.version,
            "description": p.meta.description, "sandboxed": p.meta.sandboxed,
        })
    return result


# ── Sandboxed Execution ───────────────────────────────────────────────────

_executor = ProcessPoolExecutor(max_workers=2)

SANDBOX_TIMEOUT = 30  # seconds
SANDBOX_MAX_MEMORY_MB = 256


def _run_in_sandbox(func_name: str, plugin_module_path: str, *args):
    """Run a plugin function in an isolated subprocess with resource limits."""
    import resource as res_mod

    # Set memory limit
    mem_bytes = SANDBOX_MAX_MEMORY_MB * 1024 * 1024
    try:
        res_mod.setrlimit(res_mod.RLIMIT_AS, (mem_bytes, mem_bytes))
    except (ValueError, res_mod.error):
        pass  # Not all platforms support RLIMIT_AS

    # Set CPU time limit
    try:
        res_mod.setrlimit(res_mod.RLIMIT_CPU, (SANDBOX_TIMEOUT, SANDBOX_TIMEOUT))
    except (ValueError, res_mod.error):
        pass

    # Import and run the plugin
    spec = importlib.util.spec_from_file_location("sandbox_plugin", plugin_module_path)
    if spec is None or spec.loader is None:
        return {"error": "Failed to load plugin module"}

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    func = getattr(module, func_name, None)
    if func is None:
        return {"error": f"Function {func_name} not found in plugin"}

    try:
        return func(*args)
    except Exception as e:
        return {"error": str(e)}


async def run_sandboxed(plugin_path: str, func_name: str, *args, timeout: int = SANDBOX_TIMEOUT):
    """Execute a plugin function in a sandboxed subprocess with timeout."""
    loop = asyncio.get_event_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(_executor, _run_in_sandbox, func_name, plugin_path, *args),
            timeout=timeout,
        )
        return result
    except asyncio.TimeoutError:
        logger.error("Sandboxed execution timed out for %s:%s", plugin_path, func_name)
        return {"error": "Execution timed out"}
    except Exception as e:
        logger.error("Sandboxed execution failed: %s", e)
        return {"error": str(e)}
