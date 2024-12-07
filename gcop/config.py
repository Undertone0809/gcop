import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from zeeland import Singleton

from gcop.utils import get_default_storage_path, read_yaml


@dataclass
class ModelConfig:
    """Model config.

    Args:
        model_name (str): The name of the model to use.
        api_key (str): The API key to use.
        api_base (Optional[str]): The API base URL to use.
        include_git_history (bool): Whether to include the git history in the prompt.
        enable_data_improvement (bool): Whether to enable data improvement.
        commit_template (Optional[str]): The commit template to use.

    Examples:
        model_name: openai/gpt-4o
        api_key: sk-xxx
        api_base: https://api.openai.com/v1
    """

    model_name: str
    api_key: str
    api_base: Optional[str] = None


@dataclass
class GcopConfig(metaclass=Singleton):
    """Gcop config.

    Args:
        model (ModelConfig): The model config.
        commit_template (Optional[str]): The commit template. If not provided,
            default template _DEFAULT_COMMIT_TEMPLATE will be used.
        include_git_history (bool): Whether to include the git history in the prompt.
        enable_data_improvement (bool): Whether to enable data improvement.
            Defaults to False.

    Examples:
        The following is an example of the config yaml file:

        model:
            model_name: openai/gpt-4o
            api_key: sk-xxx
            api_base: https://api.openai.com/v1
        commit_template: |
            - Good Example

            ```
            feat: implement user registration

            - Add registration form component
            - Create API endpoint for user creation
            - Implement email verification process

            This feature allows new users to create accounts and verifies
            their email addresses before activation. It includes proper
            input validation and error handling.
            ```
            reason: contain relevant detail of the changes, no just one line

            - Bad Example

            ```
            feat: add user registration
            ```
            reason: only one line, need more detail based on guidelines

    """

    model: ModelConfig
    commit_template: Optional[str] = None
    include_git_history: bool = False
    enable_data_improvement: bool = False

    _config_path: str = f"{get_default_storage_path()}/config.yaml"

    @classmethod
    def from_yaml(cls, config_path: Optional[str] = None) -> "GcopConfig":
        """Load config from YAML file.

        Args:
            config_path: Optional path to config file. If not provided, uses
            default path.

        Returns:
            GcopConfig instance initialized from YAML data

        Raises:
            ValueError: If model name is not properly configured
        """
        config: dict = read_yaml(config_path or cls._config_path)

        try:
            config["model"] = ModelConfig(**config.get("model", {}))
        except KeyError:
            raise ValueError(
                "`model` field error in ~/.zeeland/gcop/config.yaml\n"
                "Go https://gcop.zeeland.top/guide/configuration see how to config model."  # noqa
            )

        if (
            not config["model"].model_name
            or config["model"].model_name == "provider/name,eg openai/gpt-4o"
        ):
            raise ValueError(
                "Please run `gcop config` to custom your language model "
                "config.\nGo https://gcop.zeeland.top/how-to-config-model see how to config model."  # noqa
            )

        # Set commit_template to None if it's empty or only contains whitespace
        if config.get("commit_template") and not config.get("commit_template").strip():
            config["commit_template"] = None

        return cls(**config)

    @property
    def model_config(self) -> ModelConfig:
        return self.model

    @staticmethod
    def get_example_config() -> dict:
        return {
            "model": {
                "model_name": "provider/name,eg openai/gpt-4o",
                "api_key": "sk-xxx",
                "api_base": "https://api.openai.com/v1",
            },
            "commit_template": None,
            "include_git_history": False,
            "enable_data_improvement": False,
        }


EXAMPLE_CONFIG = GcopConfig.get_example_config()


def get_config() -> GcopConfig:
    """Get the  config instance, loading it if necessary.
    If an attribute is defined in the local configuration,
    the original value will be overwritten.
    """
    if not hasattr(get_config, "_instance"):
        get_config._instance = GcopConfig.from_yaml()
    project_config_path = Path.cwd() / ".gcop" / "config.yaml"
    if project_config_path.exists():
        project_config = read_yaml(project_config_path)
        for k, v in project_config.items():
            if not v.strip():
                pass
            if hasattr(get_config._instance, k):
                setattr(get_config._instance, k, v)
    return get_config._instance
