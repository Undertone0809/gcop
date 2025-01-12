from pathlib import Path

import pytest

from gcop.config import GcopConfig


def test_get_config():
    """test get_config function"""
    config = GcopConfig.get_config()
    assert isinstance(config, GcopConfig)
