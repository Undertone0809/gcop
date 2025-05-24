import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelConfig:
    """Configuration for the AI model.

    Attributes:
        model_name: The name of the model to use
        api_key: The API key for authentication
        api_base: Optional base URL for the API
    """

    model_name: str = "provider/name,eg openai/gpt-4o"
    api_key: str = "eg:sk-xxx"
    api_base: Optional[str] = "eg:https://api.openai.com/v1"

    def is_valid(self) -> bool:
        """Check if the model configuration is valid (not using example values)."""
        return not (
            self.model_name == "provider/name,eg openai/gpt-4o"
            or self.api_base == "eg:https://api.openai.com/v1"
            or self.api_key == "eg:sk-xxx"
        )


@dataclass
class GcopConfig:
    """Configuration class for Gcop.

    Attributes:
        model_config (ModelConfig): The configuration for the model.
        commit_template (str): The template for commit messages.
        include_git_history (bool): Flag to include git history in processing.
        enable_data_improvement (bool): Flag to enable data improvement features.
        history_learning_limit (int): The limit on the number of learning iterations.
    """

    model: ModelConfig = field(default_factory=ModelConfig)
    commit_template: str = None
    include_git_history: bool = False
    enable_data_improvement: bool = False
    history_learning_limit: int = 10
