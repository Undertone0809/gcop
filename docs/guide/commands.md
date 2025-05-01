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

### `git config`

Open the GCOP configuration file in the default editor. See [Configuration](/guide/configuration) for more details.

Option parameters:

- `l/--level`  [Optional]:Configuration levels, with the option of project/user. The default is `user`.

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

- `k/--key`  [Required]:Config key to set (dot notation).
- `v/--value`  [Required]:Value to set.
- `p/--project` [Optional]:Update project config instead of user config. The default is False.

## Usage Examples

1. Generate and apply an AI commit message:

   ```
   git c
   ```

2. Add all changes and commit with an AI message:

   ```
   git ac
   ```

3. Undo the last commit:

   ```
   git undo
   ```

4. Push to the current branch:

   ```
   git p
   ```

5. View detailed repository information:

   ```
   git info
   ```

   This command now provides an extensive summary of your repository, offering insights into its structure, history, and current state. It's particularly useful for project management and code review processes.

   Example output includes project name, current branch, latest commit, contributor statistics, file changes, language-specific line counts (if cloc is installed), tag information, and more.

::: info INFO
Some advanced features like line count by language require additional tools (e.g., cloc) to be installed.
:::

6. Amend the last commit:

   ```
   git amend
   ```

   This command opens your default text editor, allowing you to modify the last commit message. If you've staged changes, they will be added to the previous commit.

::: warning
The `git amend` command modifies Git history. Use it with caution, especially if you've already pushed the commit you're amending to a shared repository.
:::

7. View the current GCOP configuration

   ```
   gcop show-config
   ```

   This displays all currently active GCOP configuration items and is useful for debugging and validating configurations.

::: tip
The project level configuration (.gcop/config.yaml) overrides the global configuration. This allows you to set different configurations for different projects.
:::

For more detailed information on each command, refer to the [Quick Start](/guide/quick-start.md) section in the guide.
