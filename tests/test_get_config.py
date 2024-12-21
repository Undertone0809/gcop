from pathlib import Path

import pytest

from gcop.config import GcopConfig, get_config


def test_get_config():
    """test get_config function"""
    project_config_path = Path.cwd() / ".gcop" / "config.yaml"
    if not project_config_path.exists():
        pytest.skip("Configuration file does not exist. Skip the test")
    config = get_config()
    assert isinstance(config, GcopConfig)
