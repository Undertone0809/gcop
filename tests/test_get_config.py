import pytest

from gcop.config import GcopConfig, get_config


def test_get_config():
    '''test get_config function'''
    config = get_config()
    assert isinstance(config, GcopConfig)
