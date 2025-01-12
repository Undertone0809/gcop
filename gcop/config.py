import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional

from zeeland import Singleton

from gcop.utils import Color, get_default_storage_path, logger, read_yaml


class YamlFile:
    def __init__(self, path: str) -> None:
        self._path: Path | str = path

    def read(self) -> Dict[str, Any]:
        return read_yaml(self._path)

    def exists(self) -> bool:
        return os.path.exists(self._path)

    @property
    def path(self) -> str:
        return str(self._path)

    def __repr__(self) -> str:
        return self.path


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

    def check_model_config(self) -> bool:
        if (
            self.model_name == "provider/name,eg openai/gpt-4o"
            or self.api_base == "eg:https://api.openai.com/v1"
            or self.api_key == "eg:sk-xxx"
        ):
            return False
        return True


_gcop_config: "GcopConfig" = None


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

    default_config: ClassVar[Dict[str, Any]] = {
        "model": {
            "model_name": "provider/name,eg openai/gpt-4o",
            "api_key": "sk-xxx",
            "api_base": "eg:https://api.openai.com/v1",
        },
        "commit_template": None,
        "include_git_history": False,
        "enable_data_improvement": False,
    }
    model: ModelConfig
    commit_template: Optional[str] = None
    include_git_history: bool = False
    enable_data_improvement: bool = False

    _config_path: str = f"{get_default_storage_path()}/config.yaml"
    _config: Optional[Dict[str, Any]] = None
    user_config: Optional[YamlFile] = None
    project_config: Optional[YamlFile] = None

    def __post_init__(self):
        self._config = self.default_config

    @property
    def dict(self) -> Dict[str, Any]:
        return deepcopy(self._config)

    def merge(self, config: Dict[str, Any]) -> None:
        """Merge config with provided config.

        Args:
            config: The config to merge.
        """
        from gcop.utils import merge_dicts

        merge_dicts(self._config, config)

    @property
    def model_config(self) -> ModelConfig:
        return self.model

    def init_model_config(self) -> None:
        self._config["model"] = ModelConfig(**self._config.get("model", {}))
        if not self._config["model"].check_model_config():
            logger.color_info(
                "Warning:You are using the example configuration for the model."
                "Please replace the example values with "
                "your actual model_name ,api_key and api_base to ensure the project "  # noqa
                "runs correctly",
                color=Color.YELLOW,
            )

    @classmethod
    def get_config(cls, reload: bool = False) -> "GcopConfig":
        """Get the GcopConfig instance.

        This method follows the singleton pattern and loads configurations in the following priority:
        1. Project config (.gcop/config.yaml)
        2. User config (~/.zeeland/gcop/config.yaml)
        3. Default config

        Args:
            reload (bool, optional): Whether to force reload the configuration.
                When True, ignores existing instance and creates a new one. Defaults to False.

        Returns:
            GcopConfig: Configuration instance containing merged configuration data.

        Example:
            >>> config = GcopConfig.get_config()  # Get config instance
            >>> config = GcopConfig.get_config(reload=True)  # Force reload config
        """  # noqa: E501
        global _gcop_config
        if _gcop_config is None or reload:
            _gcop_config = cls(cls.default_config)
            # Load user_config
            user_config = YamlFile(cls._config_path)
            if user_config.exists():
                logger.info("Loading user config from %s", user_config.path)
                _gcop_config.user_config = user_config
                _gcop_config.merge(user_config.read())
            # Load project_config
            project_config_path = Path.cwd() / ".gcop" / "config.yaml"
            project_config = YamlFile(project_config_path)
            if project_config.exists():
                logger.info("Loading project config from %s", project_config.path)
                _gcop_config.merge(project_config.read())
                _gcop_config.project_config = project_config
            _gcop_config.init_model_config()
        return _gcop_config


EXAMPLE_CONFIG = GcopConfig.default_config
