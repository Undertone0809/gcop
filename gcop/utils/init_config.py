from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from gcop.utils import Color, logger, read_yaml

INIT_CONFIG_COMMAND = "init_project"


@dataclass
class LocalConfig:
    gcoprule: str

    @classmethod
    def from_yaml(cls) -> "LocalConfig":
        config: dict = read_yaml(InitConfigCommand().config_file_path)
        return cls(**config)


class ConfigFileHandleMixin:
    def __init__(self) -> None:
        self.project_path = Path.cwd()
        self.config_folder_path = self.project_path / ".gcop"
        self.config_file_path = self.config_folder_path / "config.yaml"

    def _init_project(self):
        try:
            self.config_folder_path.mkdir(parents=True, exist_ok=True)
            self.config_file_path.touch(exist_ok=True)
        except (OSError, FileNotFoundError) as e:
            logger.color_info(f"File create error: {e}", color=Color.RED)

    def _check_config_exist(self):
        return self.config_file_path.exists()


class InitConfigCommand(ConfigFileHandleMixin):
    def __init__(self) -> None:
        super().__init__()

    def handle(self):
        if self._check_config_exist():
            logger.color_info(
                """The configuration file already exists, so there is no need to \
initialize again.""",
                color=Color.DEFAULT,
            )
            return False
        self._init_project()
        return True


def check_config_exist(func):
    def wrapper(*args, **kwargs):
        command = InitConfigCommand()
        if command._check_config_exist:
            func(*args, **kwargs)
        else:
            logger.color_info(
                f"""The configuration file does not exist.\
Please first initialize the project using\
the command '{INIT_CONFIG_COMMAND}'.""",
                color=Color.RED,
            )

    return wrapper


def get_local_config() -> "LocalConfig":
    config = LocalConfig.from_yaml()
    return config


if __name__ == "__main__":
    print(get_local_config())
