---
title: Commands
description: GCOP (Git Copilot) commands.
head:
  - - meta
    - property: og:title
      content: GCOP Commands
    - property: og:description
      content: GCOP (Git Copilot) commands.
---

# GCOP Commands

GCOP enhances your Git workflow with several powerful commands. Here's a comprehensive list of available commands and their usage:

## Basic Commands

### `git ghelp`

Show the help message with a list of available GCOP commands.

### `git gcommit` or `git c`

Generate an AI-powered commit message based on staged changes and commit them.

### `git ac`

Add all changes and commit with an AI-generated message.

The same as `git add . && git gcommit`.

### `git p`

Push changes to the remote repository.

The same as `git push`.

### `git acp`

Add all changes, commit with an AI-generated message, and push to the remote repository.

The same as `git add . && git gcommit && git p`.

### `git cp`

Commit with an AI-generated message and push to the remote repository.

The same as `git gcommit && git p`.

### `git pf`

Force push changes to the remote repository (use with caution).

The same as `git push --force`.

### `git undo`

Undo the last commit while keeping changes staged.

The same as `git reset HEAD~`.

### `git amend`

Amend the last commit, allowing you to modify the commit message or add changes to the previous commit.

The same as `git commit --amend`.

::: warning
The `git amend` command modifies Git history. Use it with caution, especially if you've already pushed the commit you're amending to a shared repository.
:::

### `git gconfig`

Open the GCOP configuration file in the default editor. See [Configuration](/guide/configuration) for more details.

Option parameters:

- `l/--level` [Optional]:Configuration levels, with the option of project/user. The default is `user`.

### `git info`

Display detailed information about the current git repository. This command provides a comprehensive overview, including:

- Basic repository details (name, branch, latest commit)
- Contribution statistics (total commits, contributors, most active contributor)
- File and code statistics (repository size, most changed file, line count by language)
- Version control information (latest tag, branch count, untracked files)
- Advanced details (submodules, latest merge commit, file type statistics)

### `gcop init-project`

Initialize the GCOP configuration in the current project. This command creates the `.gcop/config.yaml` file in the project root directory, which contains the default GCOP configuration.

### `gcop show-config`

The current GCOP configuration is displayed. This command outputs all GCOP configuration items currently in effect, including model configuration, submit templates, and so on.

### `gcop set-config`

Set a configuration value.
Option parameters:

- `k/--key` [Required]:Config key to set (dot notation).
- `v/--value` [Required]:Value to set.
- `p/--project` [Optional]:Update project config instead of user config. The default is False.
