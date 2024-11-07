import os
import subprocess
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Callable, Dict, List, Literal, Optional

import click
import pne
import questionary
import requests
import typer
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.console import Console

from gcop import prompt, version
from gcop.config import ModelConfig, gcop_config
from gcop.utils import check_version_update, migrate_config_if_needed

load_dotenv()

app = typer.Typer(
    name="gcop",
    help="gcop is your local git command copilot",
    add_completion=False,
)
console = Console()


class CommitMessage(BaseModel):
    thought: str = Field(
        ..., description="the reasoning of why output these commit messages"
    )  # noqa
    content: str = Field(
        ...,
        description="git commit messages based on guidelines",  # noqa
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


def generate_commit_message(
    diff: str,
    instruction: Optional[str] = None,
    previous_commit_message: Optional[str] = None,
) -> CommitMessage:
    """Generate a git commit message based on the given diff.

    Args:
        diff(str): git diff
        instruction(Optional[str]): additional instruction. Defaults to None.
        previous_commit_message(Optional[str]): previous commit message. Defaults to
            None.

    Returns:
        str: git commit message with ai generated.
    """
    instruction: str = prompt.get_commit_instrcution(
        diff=diff,
        commit_template=gcop_config.commit_template,
        instruction=instruction,
        previous_commit_message=previous_commit_message,
    )

    model_config: ModelConfig = gcop_config.model_config
    return pne.chat(
        messages=instruction,
        model=model_config.model_name,
        model_config={
            "api_key": model_config.api_key,
            "api_base": model_config.api_base,
            "temperature": 0.0,
        },
        output_schema=CommitMessage,
    )


def check_version_before_command(f: Callable) -> Callable:
    """Decorator to check version before executing any command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        check_version_update(console)
        return f(*args, **kwargs)

    return wrapper


@app.command(name="config")
@check_version_before_command
def config_command(from_init: bool = False):
    """Open the config file in the default editor."""
    initial_content = (
        "model:\n  model_name: provider/name,eg openai/gpt-4o"
        "\n  api_key: your_api_key\n"
    )
    if not os.path.exists(gcop_config._config_path):
        Path(gcop_config._config_path).write_text(initial_content)

    if from_init:
        with open(gcop_config._config_path) as f:
            if f.read() == initial_content:
                click.edit(filename=gcop_config._config_path)
    else:
        click.edit(filename=gcop_config._config_path)


@app.command(name="init")
@check_version_before_command
def init_command():
    """Add command into git config"""
    migrate_config_if_needed()

    try:
        subprocess.run(
            ["git", "config", "--global", "alias.p", "push"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.pf", "push --force"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.undo", "reset --soft HEAD^"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.gcommit", "!gcop commit"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.c", "!gcop commit"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.ac", "!git add . && gcop commit"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            [
                "git",
                "config",
                "--global",
                "alias.acp",
                "!git add . && gcop commit && git push",
            ],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.info", "!gcop info"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.gconfig", "!gcop config"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.ghelp", "!gcop help"],
            check=True,
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "config", "--global", "alias.amend", "commit --amend"],
            check=True,
            encoding="utf-8",
        )
        console.print("[green]git aliases added successfully[/]")

        config_command(from_init=True)
        console.print("[green]gcop initialized successfully[/]")
    except subprocess.CalledProcessError as error:
        print(f"Error adding git aliases: {error}")


@app.command(name="info")
@check_version_before_command
def info_command():
    """Display detailed information about the current git repository."""
    try:
        # Get project name (usually the directory name)
        project_name = os.path.basename(os.getcwd())

        # Get current branch
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()

        # Get latest commit info
        latest_commit = subprocess.check_output(
            ["git", "log", "-1", "--oneline"], text=True
        ).strip()

        # Get number of uncommitted changes
        uncommitted_changes = len(
            subprocess.check_output(
                ["git", "status", "--porcelain"], text=True
            ).splitlines()
        )

        # Get remote URL
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], text=True
        ).strip()

        # Get total number of commits
        total_commits = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"], text=True
        ).strip()

        # Get number of contributors
        contributors = len(
            set(
                subprocess.check_output(
                    ["git", "log", "--format='%ae'"], text=True
                ).splitlines()
            )
        )

        # Get repository creation time
        creation_time = subprocess.check_output(
            [
                "git",
                "log",
                "--reverse",
                "--date=iso",
                "--format=%ad",
                "|",
                "head",
                "-1",
            ],
            text=True,
            shell=True,
        ).strip()

        # Get last modified time
        last_modified = subprocess.check_output(
            ["git", "log", "-1", "--date=iso", "--format=%ad"], text=True
        ).strip()

        # Get repository size
        repo_size = (
            subprocess.check_output(["git", "count-objects", "-vH"], text=True)
            .split("\n")[2]
            .split(":")[1]
            .strip()
        )

        # Get most active contributor
        most_active = (
            subprocess.check_output(
                ["git", "shortlog", "-sn", "--no-merges", "|", "head", "-n", "1"],
                text=True,
                shell=True,
            )
            .strip()
            .split("\t")[1]
        )

        # Get most changed file
        most_changed = (
            subprocess.check_output(
                [
                    "git",
                    "log",
                    "--pretty=format:",
                    "--name-only",
                    "|",
                    "sort",
                    "|",
                    "uniq",
                    "-c",
                    "|",
                    "sort",
                    "-rg",
                    "|",
                    "head",
                    "-n",
                    "1",
                ],
                text=True,
                shell=True,
            )
            .strip()
            .split()[-1]
        )

        # Get line count by language (requires cloc to be installed)
        try:
            line_count = subprocess.check_output(
                ["cloc", ".", "--quiet", "--json"], text=True
            )
            # Parse JSON output and format it
            import json

            line_count_data = json.loads(line_count)
            formatted_line_count = "\n".join(
                [
                    f"{lang}: {data['code']} lines"
                    for lang, data in line_count_data.items()
                    if lang != "header" and lang != "SUM"
                ]
            )
            line_count = formatted_line_count
        except FileNotFoundError:
            line_count = (
                "cloc not found. Please ensure it's installed and in your system PATH."
            )
        except json.JSONDecodeError:
            line_count = (
                "Error parsing cloc output. Please check if cloc is working correctly."
            )
        except subprocess.CalledProcessError:
            line_count = "Error running cloc. Please check if it's installed correctly."

        # Get latest tag
        try:
            latest_tag = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"], text=True
            ).strip()
        except subprocess.CalledProcessError:
            latest_tag = "No tags found"

        # Get branch count
        branch_count = len(
            subprocess.check_output(["git", "branch", "-a"], text=True).splitlines()
        )

        # Get untracked files count
        untracked_count = len(
            subprocess.check_output(
                ["git", "ls-files", "--others", "--exclude-standard"], text=True
            ).splitlines()
        )

        # Get submodule info
        try:
            submodules = subprocess.check_output(
                ["git", "submodule", "status"], text=True
            ).strip()
            if not submodules:
                submodules = "No submodules"
        except subprocess.CalledProcessError:
            submodules = "No submodules"

        # Get latest merge commit
        try:
            latest_merge = subprocess.check_output(
                ["git", "log", "--merges", "-n", "1", "--pretty=format:%h - %s"],
                text=True,
            ).strip()
            if not latest_merge:
                latest_merge = "No merge commits found"
        except subprocess.CalledProcessError:
            latest_merge = "No merge commits found"

        # Get file type statistics
        file_types = subprocess.check_output(
            [
                "git",
                "ls-files",
                "|",
                "sed",
                "s/.*\\.//",
                "|",
                "sort",
                "|",
                "uniq",
                "-c",
                "|",
                "sort",
                "-rn",
            ],
            text=True,
            shell=True,
        ).strip()

        console.print(f"[bold]Project Name:[/] {project_name}")
        console.print(f"[bold]Current Branch:[/] {current_branch}")
        console.print(f"[bold]Latest Commit:[/] {latest_commit}")
        console.print(f"[bold]Uncommitted Changes:[/] {uncommitted_changes}")
        console.print(f"[bold]Remote URL:[/] {remote_url}")
        console.print(f"[bold]Total Commits:[/] {total_commits}")
        console.print(f"[bold]Contributors:[/] {contributors}")
        console.print(f"[bold]Repository Created:[/] {creation_time}")
        console.print(f"[bold]Last Modified:[/] {last_modified}")
        console.print(f"[bold]Repository Size:[/] {repo_size}")
        console.print(f"[bold]Most Active Contributor:[/] {most_active}")
        console.print(f"[bold]Most Changed File:[/] {most_changed}")
        console.print(f"[bold]Line Count by Language:[/]\n{line_count}")
        console.print(f"[bold]Latest Tag:[/] {latest_tag}")
        console.print(f"[bold]Branch Count:[/] {branch_count}")
        console.print(f"[bold]Untracked Files:[/] {untracked_count}")
        console.print(f"[bold]Submodules:[/]{submodules}")
        console.print(f"[bold]Latest Merge Commit:[/] {latest_merge}")
        console.print(f"[bold]File Type Statistics:[/]\n{file_types}")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error getting repository information: {e}[/]")


@app.command(name="commit")
@check_version_before_command
def commit_command(
    instruction: Optional[str] = typer.Option(
        None, help="Additional instruction for commit message generation"
    ),
    previous_commit_message: Optional[str] = typer.Option(
        None, help="Previous commit message to refine"
    ),
):
    """Generate a git commit message based on the staged changes and commit the
    changes.

    If you want to commit the changes with the generated commit message, please
    select "yes". If you want to retry the commit message generation, please
    select "retry". If you want to retry the commit message generation with new
    feedback, please select "retry by feedback". If you want to exit the commit
    process, please select "exit".
    """
    diff: str = get_git_diff("--staged")

    if not diff:
        console.print("[yellow]No staged changes[/]")
        return

    console.print(f"[yellow][Code diff] \n{diff}[/]")
    console.print("[bold][On Ready] Generating commit message... [/]")

    commit_messages: CommitMessage = generate_commit_message(
        diff, instruction, previous_commit_message
    )

    console.print(f"[bold][Thought] {commit_messages.thought}[/]")
    console.print(f"[green][Generated commit message]\n{commit_messages.content}[/]")

    actions: Dict[str, Callable] = {
        "yes": lambda: subprocess.run(["git", "commit", "-m", commit_messages.content]),
        "retry": lambda: commit_command(
            instruction=None, previous_commit_message=commit_messages.content
        ),
        "retry by feedback": lambda: commit_command(
            instruction=questionary.text("Please enter your feedback:").ask(),
            previous_commit_message=commit_messages.content,
        ),
        "exit": lambda: console.print("[yellow]Exiting commit process.[/]"),
    }

    response = questionary.select(
        "Do you want to commit the changes with this message?",
        choices=list(actions.keys()),
    ).ask()

    actions[response]()


@app.command(name="help")
@check_version_before_command
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
  git c          The same as `git gcommit` command
  git ac         The same as `git add . && git gcommit` command
  git acp        The same as `git add . && git gcommit && git push` command
  git amend      Amend the last commit, allowing you to modify the commit message or add changes to the previous commit
  git info       Display basic information about the current git repository
"""  # noqa

    console.print(help_message)


if __name__ == "__main__":
    app()
