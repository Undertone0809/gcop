import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import Literal

import click
import pne
import questionary
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
    content: str = Field(
        ...,
        description="git commit message, eg: feat: Add type annotation to generate_commit_message function",  # noqa
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


def generate_commit_message(diff: str) -> str:
    """Generate a git commit message based on the given diff.

    Args:
        diff(str): git diff

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

    \n{diff}
    """  # noqa
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


@app.command(name="init")
def init_command():
    """Add command into git config"""
    try:
        subprocess.run(
            ["git", "config", "--global", "alias.gcommit", "!gcop commit"],
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
        console.print("[green]gcop initialized successfully[/]")
    except subprocess.CalledProcessError as error:
        print(f"Error adding git aliases: {error}")


@app.command(name="config")
def config_command():
    """Open the config file in the default editor."""
    initial_content = (
        "model:\n  model_name: provider/name,eg openai/gpt-4o"
        "\n  api_key: your_api_key\n"
    )
    if not os.path.exists(gcop_config.config_path):
        Path(gcop_config.config_path).write_text(initial_content)

    click.edit(filename=gcop_config.config_path)


@app.command(name="commit")
def commit_command():
    """Generate a git commit message based on the staged changes and commit the
    changes."""
    diff: str = get_git_diff("--staged")

    if not diff:
        console.print("[yellow]No staged changes[/]")
        return

    console.print(f"[yellow]Staged: {diff}[/]")

    commit_message: str = generate_commit_message(diff)

    response = questionary.confirm(
        f"Ready to run command: git commit -m '{commit_message}', continue?"
    ).ask()
    if response:
        console.print(f"[green]Command: git commit -m '{commit_message}'[/]")
        subprocess.run(["git", "commit", "-m", f"{commit_message}"])
    else:
        console.print("[red]Canceled[/]")


@app.command(name="help")
def help_command():
    """Show help message"""
    console.print("[bold]gcop[/] is your local git command copilot")
    console.print(f"[bold]Version: [/]{version}")
    console.print("[bold]GitHub: https://github.com/Undertone0809/gcop[/]")
    console.print("\n\n[bold]Usage: gcop [OPTIONS] COMMAND[/]")
    console.print("[bold]Commands:")
    console.print("[bold]  git ghelp      Add command into git config")
    console.print("[bold]  git gconfig    Open the config file in the default editor")
    console.print(
        "[bold]  git gcommit    Generate a git commit message based on the staged changes and commit the changes"  # noqa
    )


if __name__ == "__main__":
    app()

    # response: str = pne.chat(messages="hello", model="deepseek/deepseek-chat")
    # print(response)
