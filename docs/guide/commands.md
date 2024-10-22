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

Display detailed information about the current git repository. This command provides a comprehensive overview, including:

- Basic repository details (name, branch, latest commit)
- Contribution statistics (total commits, contributors, most active contributor)
- File and code statistics (repository size, most changed file, line count by language)
- Version control information (latest tag, branch count, untracked files)
- Advanced details (submodules, latest merge commit, file type statistics)

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

> Note: Some advanced features like line count by language require additional tools (e.g., cloc) to be installed.

For more detailed information on each command, refer to the [Quick Start](/guide/quick-start.md) section in the guide.

