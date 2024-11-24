from pathlib import Path

from gcop.utils import Color, logger, read_yaml


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

    def check_config_exist(self, func):
        def wrapper(*args, **kwargs):
            if self._check_config_exist:
                func(*args, **kwargs)
            else:
                logger.color_info("配置文件不存在，请先初始化项目", color=Color.RED)

        return wrapper

    def _check_config_exist(self):
        return self.config_file_path.exists()

    def get_local_config(self) -> dict:
        return read_yaml(self.config_file_path)


class InitConfigCommand(ConfigFileHandleMixin):
    def __init__(self) -> None:
        super().__init__()

    def handle(self):
        if self._check_config_exist():
            logger.color_info("配置文件已存在，无需再次初始化", color=Color.DEFAULT)
            return False
        self._init_project()
        return True


if __name__ == "__main__":
    command = InitConfigCommand()
    command.handle()
