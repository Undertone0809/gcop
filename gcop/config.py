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
        include_git_history: true
        enable_data_improvement: true
        commit_template: `
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
        `
    """

    model_name: str
    api_key: str
    api_base: Optional[str] = None
    include_git_history: bool = False
    enable_data_improvement: bool = False
    commit_template: Optional[str] = None


class GcopConfig(metaclass=Singleton):
    def __init__(self):
        self.config_path: str = f"{get_default_storage_path()}/config.yaml"

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

            # Set commit_template to None if it's empty or only contains whitespace
            if (
                model_config.commit_template
                and not model_config.commit_template.strip()
            ):
                model_config.commit_template = None

            return model_config
        except KeyError:
            msg: str = (
                "`model` field not found in ~/.gcop/config.yaml\n"
                "Please run `gcop init` to initialize the config file by the "
                "following format:\nmodel:\n  model_name: 'xxx'\n  api_key: 'xxx'"
            )
            raise ValueError(msg)


gcop_config = GcopConfig()
