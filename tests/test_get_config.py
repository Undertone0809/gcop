from pathlib import Path

import pytest

from gcop.config import config_manager
from gcop.schema import GcopConfig


@pytest.fixture
def mock_project_config(tmp_path):
    """Create a mock project configuration file"""
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
    """Test loading configuration from the project configuration file"""
    monkeypatch.chdir(mock_project_config)
    config = config_manager.load()
    assert isinstance(config, GcopConfig)
