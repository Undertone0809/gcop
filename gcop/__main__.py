import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional

import click
import pne
import questionary
import requests
import typer
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.console import Console

from gcop import version
from gcop.config import ModelConfig, gcop_config

load_dotenv()

app = typer.Typer(
    name="gcop",
    help="gcop is your local git command copilot",
    add_completion=False,
)
console = Console()


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


class LLMResponse(BaseModel):
    content: List[str] = Field(
        ...,
        description="three of alternative git commit messages, eg: feat: Add type annotation to generate_commit_message function",  # noqa
    )


def get_git_diff(diff_type: Literal["--staged", "--cached"]) -> str:
    """Get git diff

    Args:
        diff_type(str): diff type, --staged or --cached

    Returns:
        str: git diff
    """
    try:
        result = subprocess.check_output(
            ["git", "diff", diff_type], text=True, encoding="utf-8"
        )
        return result
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error getting git diff: {e}")


def generate_commit_message(diff: str, feedback: Optional[str] = None) -> List[str]:
    """Generate a git commit message based on the given diff.

    Args:
        diff(str): git diff
        feedback(Optional[str]): feedback from the previous commit message.

    Returns:
        str: git commit message
    """
    prompt = f"""You need to generate a git commit message based on the following diff:
    ## Good git messages examples
    - feat: Add type annotation to generate_commit_message function
    - fix: Fix bug in generate_commit_message function
    - docs: Update README.md
    - feat: first commit
    - style: Format code using black
    - refactor: Refactor generate_commit_message function
    - ci: Add GitHub Actions workflow for Python package release
    - build: Update setup.py and add tests folder

    \n{diff}
    """  # noqa

    if not feedback:
        # TODO optimize feedback logic
        prompt += f"""
    This is original git commit message, it's not good enough, please reflect the
    feedback and generate the better git messages.
    {feedback}
    """

    model_config: ModelConfig = gcop_config.model_config
    response: LLMResponse = pne.chat(
        messages=prompt,
        model=model_config.model_name,
        model_config={
            "api_key": model_config.api_key,
            "api_base": model_config.api_base,
        },
        output_schema=LLMResponse,
    )
    return response.content


@app.command(name="config")
def config_command(from_init: bool = False):
    """Open the config file in the default editor."""
    initial_content = (
        "model:\n  model_name: provider/name,eg openai/gpt-4o"
        "\n  api_key: your_api_key\n"
    )
    if not os.path.exists(gcop_config.config_path):
        Path(gcop_config.config_path).write_text(initial_content)

    if not from_init:
        click.edit(filename=gcop_config.config_path)
        return

    with open(gcop_config.config_path) as f:
        content = f.read()

        if content == initial_content:
            click.edit(filename=gcop_config.config_path)


@app.command(name="init")
def init_command():
    """Add command into git config"""
    try:
        subprocess.run(
            ["git", "config", "--global", "alias.p", "push"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.pf", "push --force"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.undo", "reset --soft HEAD^"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.gcommit", "!gcop commit"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.c", "!gcop commit"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.ac", "!git add . && gcop commit"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.gconfig", "!gcop config"],
            check=True,
            encoding="utf-8",  # noqa
        )
        subprocess.run(
            ["git", "config", "--global", "alias.ghelp", "!gcop help"],
            check=True,
            encoding="utf-8",  # noqa
        )
        console.print("[green]git aliases added successfully[/]")

        config_command(from_init=True)
        console.print("[green]gcop initialized successfully[/]")
    except subprocess.CalledProcessError as error:
        print(f"Error adding git aliases: {error}")


@app.command(name="commit")
def commit_command(feedback: Optional[str] = None):
    """Generate a git commit message based on the staged changes and commit the
    changes."""
    diff: str = get_git_diff("--staged")

    if not diff:
        console.print("[yellow]No staged changes[/]")
        return

    console.print(f"[yellow]Staged: {diff}[/]")

    commit_messages: List[str] = generate_commit_message(diff, feedback)

    response = questionary.select(
        "Select a commit message to commit", choices=[*commit_messages, "retry"]
    ).ask()

    if response == "retry":
        commit_command(feedback=str(commit_messages))
        return

    if response:
        console.print(f"[green]Command: git commit -m '{response}'[/]")
        subprocess.run(["git", "commit", "-m", f"{response}"])
    else:
        console.print("[red]Canceled[/]")

    # # request pypi to get the latest version
    # # TODO optimize logic, everyday check the latest version one time
    # response = requests.get("https://pypi.org/pypi/gcop/json")
    # latest_version = response.json()["info"]["version"]
    # if version != latest_version:
    #     console.print(f"[bold]A new version of gcop is available: {latest_version}[/]") # noqa
    #     console.print(f"[bold]Your current version: {version}[/]")
    #     console.print(
    #         "[bold]Please consider upgrading by running: pip install -U gcop[/]"
    #     )


@app.command(name="help")
def help_command():
    """Show help message"""
    help_message = """
[bold]gcop[/] is your local git command copilot
[bold]Version: [/]{version}
[bold]GitHub: https://github.com/Undertone0809/gcop[/]

[bold]Usage: gcop [OPTIONS] COMMAND[/]

[bold]Commands:
  git p          Push the changes to the remote repository
  git pf         Push the changes to the remote repository with force
  git undo       Undo the last commit but keep the file changes
  git ghelp      Add command into git config
  git gconfig    Open the config file in the default editor
  git gcommit    Generate a git commit message based on the staged changes and commit the changes
  git ac         The same as `git add . && git gcommit` command
  git c          The same as `git gcommit` command
"""  # noqa

    console.print(help_message)


if __name__ == "__main__":
    app()
