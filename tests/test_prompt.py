import pytest

from gcop.prompt import get_commit_instrcution


def test_get_commit_instruction_basic():
    """Test basic commit instruction generation."""
    diff = "test diff content"
    result = get_commit_instrcution(diff)
    assert isinstance(result, str)
    assert "test diff content" in result


def test_get_commit_instruction_with_template():
    """Test commit instruction with custom template."""
    diff = "test diff"
    template = """
    <example>
    feat: custom template
    </example>
    """
    result = get_commit_instrcution(diff, commit_template=template)
    assert isinstance(result, str)
    assert "custom template" in result
    assert "test diff" in result


def test_get_commit_instruction_with_previous():
    """Test commit instruction with previous commit message."""
    diff = "test diff"
    prev_msg = "fix: previous commit"
    result = get_commit_instrcution(diff, previous_commit_message=prev_msg)
    assert isinstance(result, str)
    assert "previous commit" in result
    assert "test diff" in result


def test_get_commit_instruction_with_instruction():
    """Test commit instruction with additional instruction."""
    diff = "test diff"
    instruction = "Please make it more detailed"
    result = get_commit_instrcution(diff, instruction=instruction)
    assert isinstance(result, str)
    assert "Please make it more detailed" in result
    assert "test diff" in result


def test_get_commit_instruction_with_history():
    """Test commit instruction with commit message history."""
    diff = "test diff"
    history = "commit message history"
    result = get_commit_instrcution(diff, commmit_message_history=history)
    assert isinstance(result, str)
    assert "commit message history" in result
    assert "test diff" in result


def test_get_commit_instruction_all_params():
    """Test commit instruction with all parameters."""
    diff = "test diff"
    template = "<example>template</example>"
    prev_msg = "previous message"
    instruction = "make it better"
    commit_message_history = "commit message history"

    result = get_commit_instrcution(
        diff,
        commmit_message_history=commit_message_history,
        commit_template=template,
        previous_commit_message=prev_msg,
        instruction=instruction,
    )

    assert isinstance(result, str)
    assert "test diff" in result
    assert "commit message history"
    assert "template" in result
    assert "previous message" in result
    assert "make it better" in result
