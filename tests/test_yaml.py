import tempfile
from pathlib import Path

import pytest
import yaml

from gcop.utils import read_yaml


def test_read_yaml():
    test_data = {"key1": "value1", "key2": {"nested_key": "nested_value"}}

    with tempfile.NamedTemporaryFile(
        suffix=".yaml", mode="w", delete=False
    ) as temp_file:
        yaml.dump(test_data, temp_file)
        temp_path = Path(temp_file.name)

    try:
        # Test reading the YAML file
        result = read_yaml(temp_path)

        # Verify the contents match
        assert result == test_data
        assert result["key1"] == "value1"
        assert result["key2"]["nested_key"] == "nested_value"

    finally:
        # Clean up the temporary file
        temp_path.unlink()


def test_read_yaml_file_not_found():
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        read_yaml(Path("nonexistent.yaml"))
