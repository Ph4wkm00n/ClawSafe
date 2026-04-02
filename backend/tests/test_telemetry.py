from unittest.mock import MagicMock

from app.core.telemetry import setup_telemetry


def test_telemetry_disabled_by_default():
    """Telemetry setup should be a no-op when disabled."""
    app = MagicMock()
    # Should not raise
    setup_telemetry(app)
