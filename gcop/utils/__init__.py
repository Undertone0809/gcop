import os
import tempfile

import yaml


def convert_backslashes(path: str):
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def get_default_storage_path(module_name: str = "") -> str:
    """Get the default storage path for the current module. The storage path is
    created in the user's home directory, or in a temporary directory if permission
    is denied.

    Args:
        module_name(str): The name of the module to create a storage path for.

    Returns:
        str: The default storage path for the current module.
    """
    storage_path = os.path.expanduser("~/.gcop")

    if module_name:
        storage_path = os.path.join(storage_path, module_name)

    # Try to create the storage path (with module subdirectory if specified)
    # Use a temporary directory instead if permission is denied,
    try:
        os.makedirs(storage_path, exist_ok=True)
    except PermissionError:
        storage_path = os.path.join(tempfile.gettempdir(), "gcop", module_name)
        os.makedirs(storage_path, exist_ok=True)

    return convert_backslashes(storage_path)


def read_yaml(file_path: str) -> dict:
    """Read yaml config file.

    Args:
        file_path(str): file path

    Returns:
        dict: model config, format is as follows
            {
                "model": {
                    "model_name": "xxx",
                    "api_key": "xxx"
                }
            }
    """
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
        return config
