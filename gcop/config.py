import os
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, Dict, Optional

from zeeland import Singleton

from gcop.utils import Color, get_default_storage_path, logger, merge_dicts, read_yaml

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


class ConfigFile:
    """Represents a YAML configuration file."""

    def __init__(self, path: str | Path) -> None:
        self._path: Path = Path(path)

    def read(self) -> Dict[str, Any]:
        """Read and parse the YAML file."""
        return read_yaml(self._path)

    def exists(self) -> bool:
        """Check if the config file exists."""
        return self._path.exists()

    @property
    def path(self) -> str:
        """Get the string representation of the file path."""
        return str(self._path)

    def __repr__(self) -> str:
        return f"ConfigFile(path='{self.path}')"


@dataclass
class ModelConfig:
    """Configuration for the AI model.

    Attributes:
        model_name: The name of the model to use
        api_key: The API key for authentication
        api_base: Optional base URL for the API
    """

    model_name: str
    api_key: str
    api_base: Optional[str] = None

    def is_valid(self) -> bool:
        """Check if the model configuration is valid (not using example values)."""
        return not (
            self.model_name == "provider/name,eg openai/gpt-4o"
            or self.api_base == "eg:https://api.openai.com/v1"
            or self.api_key == "eg:sk-xxx"
        )


class GcopConfig(metaclass=Singleton):
    """Global configuration manager for GCOP. This class follows the singleton pattern
    and manages configuration from multiple sources:

    1. Project config (.gcop/config.yaml)
    2. User config (~/.zeeland/gcop/config.yaml)
    3. Default config
    """

    _instance: ClassVar[Optional["GcopConfig"]] = None
    _DEFAULT_USER_CONFIG_PATH: ClassVar[str] = (
        f"{get_default_storage_path()}/config.yaml"
    )
    _DEFAULT_PROJECT_CONFIG_PATH: ClassVar[str] = ".gcop/config.yaml"

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        self._config: Dict[str, Any] = deepcopy(DEFAULT_CONFIG)
        self.model: ModelConfig = ModelConfig(**self._config.get("model", {}))
        self.commit_template: Optional[str] = None
        self.include_git_history: bool = False
        self.enable_data_improvement: bool = False

        self.user_config: Optional[ConfigFile] = None
        self.project_config: Optional[ConfigFile] = None

        self._load_configurations()

    def _load_configurations(self) -> None:
        """Load and merge configurations from all sources."""
        # Load user config
        user_config = ConfigFile(self._DEFAULT_USER_CONFIG_PATH)
        if user_config.exists():
            logger.info("Loading user config from %s", user_config.path)
            self.user_config = user_config
            self._merge_config(user_config.read())

        # Load project config
        project_config = ConfigFile(Path.cwd() / self._DEFAULT_PROJECT_CONFIG_PATH)
        if project_config.exists():
            logger.info("Loading project config from %s", project_config.path)
            self.project_config = project_config
            self._merge_config(project_config.read())

        self._initialize_model_config()

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Merge new configuration with existing configuration."""
        merge_dicts(self._config, new_config)
        self._update_instance_attributes()

    def _update_instance_attributes(self) -> None:
        """Update instance attributes from the current configuration."""
        self.commit_template = self._config.get("commit_template")
        self.include_git_history = self._config.get("include_git_history", False)
        self.enable_data_improvement = self._config.get(
            "enable_data_improvement", False
        )

    def _initialize_model_config(self) -> None:
        """Initialize and validate model configuration."""
        self.model = ModelConfig(**self._config.get("model", {}))
        if not self.model.is_valid():
            logger.color_info(
                "Warning: You are using example configuration values for the model. "
                "Please replace them with your actual model_name, api_key, and api_base. "  # noqa
                "Visit https://gcop.zeeland.top/other/how-to-config-model.html for help.",  # noqa
                color=Color.YELLOW,
            )

    @property
    def dict(self) -> Dict[str, Any]:
        """Get a deep copy of the current configuration dictionary."""
        return deepcopy(self._config)

    @classmethod
    def get_instance(cls, reload: bool = False) -> "GcopConfig":
        """Get the singleton instance of GcopConfig.

        Args:
            reload: If True, force reload the configuration

        Returns:
            The singleton instance of GcopConfig
        """
        if cls._instance is None or reload:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_config(cls, reload: bool = False) -> "GcopConfig":
        """Alias for get_instance to maintain backward compatibility."""
        return cls.get_instance(reload)

    @property
    def model_config(self) -> ModelConfig:
        """Get the current model configuration."""
        return self.model

    @property
    def _config_path(self) -> str:
        """Legacy property for backward compatibility."""
        return self._DEFAULT_USER_CONFIG_PATH
