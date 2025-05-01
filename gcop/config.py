from conftier import ConfigManager

from gcop.schema import GcopConfig

DEFAULT_CONFIG = {
    "model": {
        "model_name": "provider/name,eg openai/gpt-4o",
        "api_key": "eg:sk-xxx",
        "api_base": "eg:https://api.openai.com/v1",
    },
    "commit_template": None,
    "include_git_history": False,
    "enable_data_improvement": False,
}


config_manager = ConfigManager(
    config_name="gcop",
    config_schema=GcopConfig,
    version="1.0.0",
    auto_create_user=True,
)
