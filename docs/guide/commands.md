# GCOP Commands

GCOP enhances your Git workflow with several powerful commands. Here's a comprehensive list of available commands and their usage:

## Basic Commands

### `git gcommit` or `git c`

Generate an AI-powered commit message based on staged changes and commit them.

### `git ac`

Add all changes and commit with an AI-generated message.

### `git p`

Push changes to the remote repository.

### `git pf`

Force push changes to the remote repository (use with caution).

### `git undo`

Undo the last commit while keeping changes staged.

### `git ghelp`

Show the help message with a list of available GCOP commands.

### `git gconfig`

Open the GCOP configuration file in the default editor.

### `git info`

Display basic information about the current git repository.

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

5. View repository information:
   ```
   git info
   ```
   This command provides a summary of your repository, including:

- Project name
- Current branch
- Latest commit
- Number of uncommitted changes
- Remote URL
- Total number of commits
- Number of contributors
- Repository creation time
- Last modified time
- Repository size
- Most active contributor
- Most changed file
- Line count by language (if cloc is installed)
- Latest tag
- Branch count
- Untracked files count
- Submodule information
- Latest merge commit
- File type statistics

For more detailed information on each command, refer to the [Quick Start](/guide/quick-start.md) section in the guide.
