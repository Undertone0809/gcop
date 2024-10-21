import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from gcop.utils import get_default_storage_path, read_yaml
from gcop.utils.singleton import Singleton


@dataclass
class ModelConfig:
    model_name: str
    api_key: str
    api_base: Optional[str] = None
    include_git_history: bool = False  # 是否将过去的 git commit 信息作为参考的一部分
    enable_data_improvement: bool = False  # 是否愿意将数据用于改进 gcop 模型

class GcopConfig(metaclass=Singleton):
    def __init__(self):
        self.config_path: str = f"{get_default_storage_path()}/config.yaml"

        if not os.path.exists(self.config_path):
            initial_content = (
                "model:\n  model_name: provider/name,eg openai/gpt-4o"
                "\n  api_key: your_api_key\n"
            )
            Path(self.config_path).write_text(initial_content)

    @property
    def model_config(self) -> ModelConfig:
        try:
            _: dict = read_yaml(self.config_path)["model"]
            model_config = ModelConfig(**_)

            if model_config.model_name == "provider/name,eg openai/gpt-4o":
                msg: str = (
                    "Please run `git gconfig` to update or initialize your model "
                    "config.\nGo https://github.com/Undertone0809/gcop see how to config your model."  # noqa
                )
                raise ValueError(msg)

            return model_config
        except KeyError:
            msg: str = (
                "`model` field not found in ~/.gcop/config.yaml\n"
                "Please run `git gconfig` to initialize the config file by the "
                "following format:\nmodel:\n  model_name: 'xxx'\n  api_key: 'xxx'"
            )
            raise ValueError(msg)


gcop_config = GcopConfig()
