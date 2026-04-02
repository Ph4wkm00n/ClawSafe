from app.plugins.base import PluginMeta


def test_plugin_meta_has_sandboxed_field():
    meta = PluginMeta()
    assert meta.sandboxed is True


def test_plugin_meta_sandboxed_override():
    meta = PluginMeta()
    meta.sandboxed = False
    assert meta.sandboxed is False
