import pytest

from gcop.utils.init_config import InitConfigCommand, get_local_config

local_conifig_file_path = InitConfigCommand().config_file_path
local_config_exits = local_conifig_file_path.exists()


@pytest.mark.skipif(not local_config_exits, reason="local config file not exits")
def test_get_local_config():
    local_config = get_local_config()
    assert local_config is not None
