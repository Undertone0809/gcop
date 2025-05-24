import os
import pprint
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
import yaml
from conftier import (
    ConfigManager,
    find_project_root,
    get_project_config_path,
    get_user_config_path,
)
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from gcop import prompt, version
from gcop.config import config_manager, is_key_in_config
from gcop.schema import GcopConfig, ModelConfig
from gcop.utils import check_version_update, migrate_config_if_needed
from gcop.utils.logger import Color, logger

load_dotenv()

app = typer.Typer(
    name="gcop",
    help="gcop is your local git command copilot",
    add_completion=False,
)


class CommitMessage(BaseModel):
    thought: str = Field(
        ..., description="the reasoning of why output these commit messages"
    )  # noqa
    content: str = Field(
        ...,
        description="git commit messages based on guidelines",  # noqa
    )


def get_git_diff(diff_type: Literal["--staged", "--cached"]) -> str:
    """Get git diff.

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


def get_git_history(log_type: Literal["--oneline", "--stat"], limit: int) -> str:
    """Get git history

    Args:
        log_type(str): log type, --oneline or --stat
        limit(int): Limit the output quantity

    Returns:
        str: git history
    """
    try:
        result = subprocess.check_output(
            ["git", "log", log_type, "-n", limit], text=True, encoding="utf-8"
        )
        return result
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error getting git history: {e}")


def generate_commit_message(
    diff: str,
    commit_message_history: Optional[str] = None,
    instruction: Optional[str] = None,
    previous_commit_message: Optional[str] = None,
) -> CommitMessage:
    """Generate a git commit message based on the given diff.

    Args:
        diff(str): git diff
        instruction(Optional[str]): additional instruction. Defaults to None.
        previous_commit_message(Optional[str]): previous commit message. At the first
            time, it's usually empty. It always uses when you are improving the
            commit message or providing feedback. Defaults to None.

    Returns:
        str: git commit message with ai generated.
    """
    gcop_config = config_manager.load()
    commit_template = gcop_config.commit_template
    instruction: str = prompt.get_commit_instrcution(
        diff=diff,
        commmit_message_history=commit_message_history,
        commit_template=commit_template,
        instruction=instruction,
        previous_commit_message=previous_commit_message,
    )
    model_config: ModelConfig = gcop_config.model
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
        check_version_update()
        return f(*args, **kwargs)

    return wrapper


@app.command(name="config")
@check_version_before_command
def config_command(
    level: str = typer.Option(
        "project",
        "--level",
        "-l",
        help="Configuration levels, with the option of project/user",
        case_sensitive=False,
    ),
):
    """Open the config file in the default editor."""
    if level == "project":
        click.edit(filename=config_manager.project_config_path)
    elif level == "user":
        click.edit(filename=config_manager.user_config_path)
    else:
        typer.echo("The current parameter is illegal. The option is project/user.")


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
            ["git", "config", "--global", "alias.cp", "!gcop commit && git push"],
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
        logger.color_info("git aliases added successfully", color=Color.GREEN)
        config_manager.load()
        logger.color_info("gcop initialized successfully", color=Color.GREEN)
    except subprocess.CalledProcessError as error:
        logger.color_info(f"Error adding git aliases: {error}", color=Color.RED)


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

        logger.color_info(f"Project Name: {project_name}")
        logger.color_info(f"Current Branch: {current_branch}")
        logger.color_info(f"Latest Commit: {latest_commit}")
        logger.color_info(f"Uncommitted Changes: {uncommitted_changes}")
        logger.color_info(f"Remote URL: {remote_url}")
        logger.color_info(f"Total Commits: {total_commits}")
        logger.color_info(f"Contributors: {contributors}")
        logger.color_info(f"Repository Created: {creation_time}")
        logger.color_info(f"Last Modified: {last_modified}")
        logger.color_info(f"Repository Size: {repo_size}")
        logger.color_info(f"Most Active Contributor: {most_active}")
        logger.color_info(f"Most Changed File: {most_changed}")
        logger.color_info(f"Line Count by Language:\n{line_count}")
        logger.color_info(f"Latest Tag: {latest_tag}")
        logger.color_info(f"Branch Count: {branch_count}")
        logger.color_info(f"Untracked Files: {untracked_count}")
        logger.color_info(f"Submodules: {submodules}")
        logger.color_info(f"Latest Merge Commit: {latest_merge}")
        logger.color_info(f"File Type Statistics:\n{file_types}")

    except subprocess.CalledProcessError as e:
        logger.color_info(f"Error getting repository information: {e}", color=Color.RED)


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
    gcop_config = config_manager.load()

    diff: str = get_git_diff("--staged")
    commit_message_history: Optional[str] = None

    if not diff:
        logger.color_info("No staged changes", color=Color.YELLOW)
        return

    if gcop_config.include_git_history:
        commit_message_history: str = get_git_history(
            "--online", gcop_config.history_learning_limit
        )

    logger.color_info(f"[Code diff] \n{diff}", color=Color.YELLOW)
    logger.color_info("[On Ready] Generating commit message...")

    commit_messages: CommitMessage = generate_commit_message(
        diff, commit_message_history, instruction, previous_commit_message
    )

    logger.color_info(f"[Thought] {commit_messages.thought}")
    logger.color_info(
        f"[Generated commit message]\n{commit_messages.content}", color=Color.GREEN
    )

    actions: Dict[str, Callable] = {
        "yes": lambda: subprocess.run(["git", "commit", "-m", commit_messages.content]),
        "retry": lambda: commit_command(
            instruction=None, previous_commit_message=commit_messages.content
        ),
        "retry by feedback": lambda: commit_command(
            instruction=questionary.text("Please enter your feedback:").ask(),
            previous_commit_message=commit_messages.content,
        ),
        "exit": lambda: logger.color_info(
            "Exiting commit process.", color=Color.YELLOW
        ),
    }

    response = questionary.select(
        "Do you want to commit the changes with this message?",
        choices=list(actions.keys()),
    ).ask()

    actions[response]()


@app.command(name="init-project")
@check_version_before_command
def init_project(
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Project path"),
):
    """Initialize project configuration template"""
    config_name = config_manager.config_name
    project_path = Path(path) if path else Path.cwd()
    config_dir = project_path / f".{config_name}"
    config_file = config_dir / "config.yaml"

    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created directory: {config_dir}")

    if not config_file.exists():
        with open(config_file, "w") as f:
            yaml.dump(config_manager._get_default_dict(), f, default_flow_style=False)
        typer.echo(f"Created project config template: {config_file}")
    else:
        typer.echo(f"Project config already exists: {config_file}")


@app.command(name="show-config")
@check_version_before_command
def show_config():
    """Show current effective configuration and its sources"""
    config_name = config_manager.config_name

    # Get configs directly from config_manager
    merged_config = config_manager.load()
    user_config = config_manager.get_user_config()
    project_config = config_manager.get_project_config()

    if not user_config and not project_config:
        typer.echo(
            typer.style(
                f"No configuration files found for framework '{config_name}'",
                fg="yellow",
            )
        )
        return

    # Display user config
    if user_config:
        typer.echo(
            typer.style(f"User config ({config_manager.user_config_path}):", fg="blue")
        )
        typer.echo(
            typer.style(yaml.dump(user_config, default_flow_style=False), fg="cyan")
        )
    else:
        typer.echo(
            typer.style(
                f"No user config found at {config_manager.user_config_path}",
                fg="yellow",
            )
        )

    # Display project config
    if project_config:
        typer.echo(
            typer.style(
                f"Project config ({config_manager.project_config_path}):", fg="blue"
            )
        )
        typer.echo(
            typer.style(yaml.dump(project_config, default_flow_style=False), fg="cyan")
        )
    else:
        typer.echo(typer.style("No project config found", fg="yellow"))

    # Display merged config (effective configuration)
    typer.echo(typer.style("Merged config (effective configuration):", fg="green"))
    typer.echo(
        typer.style(yaml.dump(merged_config, default_flow_style=False), fg="green")
    )


@app.command(name="set-config")
@check_version_before_command
def set_config(
    key: str = typer.Option(
        ..., "--key", "-k", help="Config key to set (dot notation)"
    ),
    value: str = typer.Option(..., "--value", "-v", help="Value to set"),
    project: bool = typer.Option(
        False,
        "--project",
        "-p",
        is_flag=True,
        help="Update project config instead of user config",
    ),
):
    """Set a configuration value"""
    gcop_config: GcopConfig = config_manager.load()
    if not is_key_in_config(gcop_config, key):
        typer.echo(f"Invalid key(s): {key}")
        raise typer.Abort()

    config_name: str = config_manager.config_name
    if project:
        project_root = find_project_root()
        if not project_root:
            typer.echo("No project root found. Cannot update project configuration.")
            raise typer.Abort()
        config_path = get_project_config_path(config_name, str(project_root))
        if not config_path:
            typer.echo("No project configuration path could be determined.")
            raise typer.Abort()
    else:
        config_path = get_user_config_path(config_name)

    config_path.parent.mkdir(parents=True, exist_ok=True)

    existing_config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            existing_config = yaml.safe_load(f) or {}

    key_parts = key.split(".")
    current = existing_config

    for part in key_parts[:-1]:
        current = current.setdefault(part, {})
        if not isinstance(current, dict):
            current = {}

    try:
        if value.lower() == "true":
            parsed_value = True
        elif value.lower() == "false":
            parsed_value = False
        elif value.isdigit():
            parsed_value = int(value)
        else:
            try:
                parsed_value = float(value)
            except ValueError:
                parsed_value = value
    except Exception:
        parsed_value = value

    current[key_parts[-1]] = parsed_value

    with open(config_path, "w") as f:
        yaml.dump(existing_config, f, default_flow_style=False, sort_keys=False)

    config_type = "project" if project else "user"
    typer.echo(f"Updated {config_type} config: {key} = {value}")


@app.command(name="help")
@check_version_before_command
def help_command():
    """Show help message"""
    help_message = f"""
gcop is your local git command copilot
Version: {version}
GitHub: https://github.com/Undertone0809/gcop

Usage: gcop [OPTIONS] COMMAND

Commands:
  git p          Push the changes to the remote repository
  git pf         Push the changes to the remote repository with force
  git undo       Undo the last commit but keep the file changes
  git ghelp      Add command into git config
  git gconfig    Open the config file in the default editor
  git gcommit    Generate a git commit message based on the staged changes and commit the changes
  git c          The same as `git gcommit` command
  git ac         The same as `git add . && git gcommit` command
  git acp        The same as `git add . && git gcommit && git push` command
  git cp         The same as `git gcommit && git push` command
  git amend      Amend the last commit, allowing you to modify the commit message or add changes to the previous commit
  git info       Display basic information about the current git repository
  gcop init-project Initialize gcop config in the current project
  gcop show-config Show the current gcop config
"""  # noqa

    logger.color_info(help_message)


if __name__ == "__main__":
    app()
