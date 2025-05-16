from dataclasses import fields, is_dataclass

from conftier import ConfigManager

from gcop.schema import GcopConfig


def is_key_in_config(config: GcopConfig, key: str) -> bool:
    """Check if a key (including nested keys) exists in the config.

    Args:
        config: The configuration object (GcopConfig instance).
        key: The key to check, can be nested (e.g. 'model_config.base_url').

    Returns:
        bool: True if the key exists, False otherwise.
    """
    keys = key.split(".")
    current = config

    for k in keys:
        if is_dataclass(current):
            field_names = [f.name for f in fields(current)]
            if k not in field_names:
                return False
            current = getattr(current, k)
        elif isinstance(current, dict):
            if k not in current:
                return False
            current = current[k]
        else:
            try:
                current = getattr(current, k)
            except AttributeError:
                return False

    return True


config_manager = ConfigManager(
    config_name="gcop",
    config_schema=GcopConfig,
    version="1.0.0",
    auto_create_user=True,
)
print(config_manager.get_user_config())
print(config_manager.get_project_config())