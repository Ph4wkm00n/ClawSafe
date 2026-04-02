import os
from unittest.mock import patch

from app.services.scoring import detect_environment, _apply_environment_weight


def test_detect_environment_default():
    with patch.dict(os.environ, {}, clear=True):
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.deploy_environment = ""
            env = detect_environment()
            # Returns "staging" in Docker, "development" otherwise
            assert env in ("development", "staging")


def test_detect_environment_from_setting():
    with patch("app.core.config.settings") as mock_settings:
        mock_settings.deploy_environment = "production"
        env = detect_environment()
        assert env == "production"


def test_environment_weight_development():
    # Development weight is 0.5x
    with patch("app.services.scoring.detect_environment", return_value="development"):
        assert _apply_environment_weight(60) == 30


def test_environment_weight_production():
    # Production weight is 1.5x
    with patch("app.services.scoring.detect_environment", return_value="production"):
        assert _apply_environment_weight(60) == 90


def test_environment_weight_capped_at_100():
    with patch("app.services.scoring.detect_environment", return_value="production"):
        assert _apply_environment_weight(80) == 100
