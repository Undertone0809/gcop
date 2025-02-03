import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Mapping, Optional

import questionary
import requests
import yaml
from rich.console import Console
from zeeland import get_default_storage_path as _get_default_storage_path

from gcop import version
from gcop.utils.logger import Color, logger


@dataclass
class VersionMetadata:
    """Version metadata for caching version information."""

    last_check: Optional[datetime] = None
    latest_version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VersionMetadata":
        """Create VersionMetadata from dictionary."""
        last_check = None
        if data.get("last_check"):
            try:
                last_check = datetime.fromisoformat(data["last_check"])
            except (ValueError, TypeError):
                last_check = None

        return cls(last_check=last_check, latest_version=data.get("latest_version"))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "latest_version": self.latest_version,
        }


def convert_backslashes(path: str) -> str:
    """Convert all \\ to / of file path."""
    return path.replace("\\", "/")


def get_old_default_storage_path(module_name: str = "") -> str:
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


def get_default_storage_path(module_name: str = "") -> str:
    return _get_default_storage_path("gcop", module_name)


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
    with open(file_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        return config


def _load_metadata(metadata_path: str) -> VersionMetadata:
    """Load version metadata from file or create new if not exists.

    Args:
        metadata_path(str): Path to metadata file

    Returns:
        VersionMetadata: Loaded or new metadata object
    """
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                return VersionMetadata.from_dict(json.load(f))
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, create new metadata
            pass

    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

    metadata = VersionMetadata()

    with open(metadata_path, "w") as f:
        json.dump(metadata.to_dict(), f)

    return metadata


def check_version_update() -> None:
    """Check for new version of gcop using cached data.
    Only checks PyPI once per day and caches the result.
    """
    metadata_path: str = os.path.join(get_default_storage_path(), "metadata.json")
    current_time: datetime = datetime.now()

    metadata: VersionMetadata = _load_metadata(metadata_path)

    if metadata.last_check and current_time - metadata.last_check <= timedelta(days=1):
        return

    try:
        response = requests.get("https://pypi.org/pypi/gcop/json", timeout=1)
        latest_version = response.json()["info"]["version"]

        metadata = VersionMetadata(
            last_check=current_time, latest_version=latest_version
        )
        with open(metadata_path, "w") as f:
            json.dump(metadata.to_dict(), f)

        if latest_version != version:
            should_update = questionary.confirm(
                f"A new version of gcop is available: {latest_version} "
                f"(current: {version}). Would you like to update now?"
            ).ask()

            if should_update:
                try:
                    logger.color_info("Updating gcop...", color=Color.YELLOW)
                    subprocess.run(["pip", "install", "-U", "gcop"], check=True)
                    logger.color_info("Update successful!", color=Color.GREEN)
                    subprocess.run(["gcop", "init"], check=True)
                    logger.color_info(
                        "GCOP reinitialized successfully!", color=Color.GREEN
                    )
                except subprocess.CalledProcessError as e:
                    logger.color_info(f"Failed to update gcop: {e}", color=Color.RED)

    except Exception:
        pass


def migrate_config_if_needed() -> None:
    """Migrate old config to new location if needed.

    After v1.6.0, the config file location has been changed to
    `~/.zeeland/gcop/config.yaml`. Original config file location is
    `~/.gcop/config.yaml`.
    """
    old_config_path: str = os.path.join(get_old_default_storage_path(), "config.yaml")
    new_config_path: str = os.path.join(get_default_storage_path(), "config.yaml")

    if not os.path.exists(old_config_path):
        return

    try:
        if not os.path.exists(new_config_path):
            logger.color_info("No new config file found, migrating old config...")
            shutil.copy2(old_config_path, new_config_path)
            logger.color_info(
                f"Config migrated from {old_config_path} to {new_config_path}"
            )
        else:
            logger.color_info("New config file already exists, skipping migration")

        backup_path: str = old_config_path + ".backup"
        shutil.copy2(old_config_path, backup_path)
        os.remove(old_config_path)
        logger.color_info(f"Old config backup created at {backup_path}")

    except Exception as e:
        logger.color_info(f"Error migrating config: {e}", color=Color.RED)
        logger.color_info(
            "Please manually move your config file to the new location", color=Color.RED
        )


def merge_dicts(d1: Dict[str, Any], d2: Dict[str, Any]) -> None:
    for k in d2:
        if k in d1 and isinstance(d1[k], Dict) and isinstance(d2[k], Mapping):
            merge_dicts(d1[k], d2[k])
        else:
            d1[k] = d2[k]
