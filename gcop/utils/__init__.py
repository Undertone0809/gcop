import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple

import questionary
import requests
import yaml
from rich.console import Console

from gcop import version


@dataclass
class VersionMetadata:
    """Version metadata for caching version information."""

    last_check: Optional[datetime] = None
    latest_version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "VersionMetadata":
        """Create VersionMetadata from dictionary."""
        last_check = None
        if data.get("last_check"):
            try:
                last_check = datetime.fromisoformat(data["last_check"])
            except (ValueError, TypeError):
                last_check = None

        return cls(last_check=last_check, latest_version=data.get("latest_version"))

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "latest_version": self.latest_version,
        }


def convert_backslashes(path: str) -> str:
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


def check_version_update(console: Console) -> None:
    """Check for new version of gcop using cached data.
    Only checks PyPI once per day and caches the result.

    Args:
        console: Rich console instance for output
    """
    metadata_path = os.path.join(get_default_storage_path(), "metadata.json")
    current_time = datetime.now()

    metadata = _load_metadata(metadata_path)

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
                    console.print("[yellow]Updating gcop...[/]")
                    subprocess.run(["pip", "install", "-U", "gcop"], check=True)
                    console.print("[green]Update successful![/]")
                    subprocess.run(["gcop", "init"], check=True)
                    console.print("[green]GCOP reinitialized successfully![/]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]Failed to update gcop: {e}[/]")

    except Exception:
        pass
