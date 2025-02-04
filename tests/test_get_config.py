from pathlib import Path

import pytest

from gcop.config import GcopConfig


@pytest.fixture
def mock_project_config(tmp_path):
    """创建一个模拟的项目配置文件"""
    config_dir: Path = tmp_path / ".gcop"
    config_dir.mkdir()
    project_config_file = config_dir / "config.yaml"
    project_config_file.write_text(
        """
commit_template: null
enable_data_improvement: false
historyLearing: True
learning_limit: 10
include_git_history: false
model:
  api_base: test-https://api.openai.com/v1
  api_key: test-api-key
  model_name: test-openai/gpt-4o
    """.strip()
    )
    return tmp_path


def test_get_project_config(mock_project_config, monkeypatch):
    """测试从项目配置文件加载配置"""
    monkeypatch.chdir(mock_project_config)
    config = GcopConfig.get_config()
    assert isinstance(config, GcopConfig)
    assert config.enable_data_improvement is False
    assert config.include_git_history is False
    assert config.model.api_base == "test-https://api.openai.com/v1"
    assert config.model.api_key == "test-api-key"
    assert config.model.model_name == "test-openai/gpt-4o"
