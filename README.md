<p align="center">
   <img src="./docs/public/banner.png" alt="GCOP Banner" style="border-radius: 15px;">
</p>

<div align="center">

[![Python Version](https://img.shields.io/pypi/pyversions/gcop.svg)](https://pypi.org/project/gcop/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/Undertone0809/gcop/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/Undertone0809/gcop/releases)
[![License](https://img.shields.io/github/license/Undertone0809/gcop)](https://github.com/Undertone0809/gcop/blob/main/LICENSE)

<a href="https://t.me/zeeland0809" target="_blank">
    <img src="https://img.shields.io/badge/Telegram-join%20chat-2CA5E0?logo=telegram&logoColor=white" alt="chat on Telegram">
</a>

</div>

# GCOP - Your Complete Git Workflow Assistant

GCOP (Git Copilot) enhances your Git experience with AI-powered commit messages, smart commands, and workflow optimization tools. It streamlines your development workflow, improves team collaboration, and makes complex Git operations simple.

## 🚀 Key Features

1. **🤖 Intelligent Commit Messages**
   - Generate meaningful, structured commit messages automatically
   - Save time while improving your repository's documentation quality
   - Learn from your project's commit history to match your team's style

2. **⚡ 20+ Powerful Git Commands**
   - Streamline complex Git operations with intuitive shortcuts
   - Simplify your daily workflow with smarter, more efficient commands
   - Reduce common Git operations to single commands

3. **📊 Repository Insights**
   - Get detailed information about your project with a single command
   - Visualize activity, contributors, and codebase statistics easily
   - Monitor repository health and team contributions

4. **🔄 Workflow Automation**
   - Combine multiple Git operations into single commands
   - Automate common patterns like "add, commit and push" to save time
   - Create consistent workflows across your team

5. **🎨 Highly Customizable**
   - Configure to match your team's conventions with templates
   - Project-specific settings for consistent standards
   - Custom AI model selection for your specific needs

6. **🤝 Team Collaboration Tools**
   - Maintain consistent commit styles and clear history across your team
   - Improve code review processes with better commit documentation
   - Enhance team communication through standardized practices

## Video Demo

This video shows how to use gcop to generate a commit message. See the [documentation](https://gcop.zeeland.top/)

[![Gcop is your git AI copilot](https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20240624003422.png)](https://www.youtube.com/watch?v=j7qKI_TdhXs "Gcop is your git AI copilot")

## 🛠️ Getting Started

We recommend you to read the [Quick Start Guide](https://gcop.zeeland.top/) in detail.

### What You'll Need

- Python 3.8 or newer
- Git installed on your system
- An API key for your preferred LLM (e.g., OpenAI, Anthropic)

### Installation

1. Install GCOP with pip:

   ```
   pip install gcop
   ```

2. Initialize GCOP:

   ```
   gcop init
   ```

> This command sets up GCOP and adds its aliases to your Git configuration.

3. Configure your AI model:

   ```
   git gconfig
   ```

   This opens the configuration file. Edit it to include your AI provider details:

   ```yaml
   model:
     model_name: provider/name, eg openai/gpt-4o
     api_key: your_api_key
   ```

Then gcop will generate a `config.yaml`, then gcop will open the `config.yaml`
file in the default editor, and you can config your language model. See how to
config your model [here](https://gcop.zeeland.top/other/how-to-config-model.html):

> `config.yaml` store path:
>
> - Windows: `%USERPROFILE%\.zeeland\gcop\config.yaml`
> - Linux: `~/.zeeland/gcop/config.yaml`
> - MacOS: `~/.zeeland/gcop/config.yaml`

1. Verify the installation:

   ```
   git ghelp
   ```

   You should see output similar to:

   ```
   gcop is your local git command copilot
   Version: 1.0.0
   GitHub: https://github.com/Undertone0809/gcop

   Usage: git [OPTIONS] COMMAND

   Commands:
     git p          Push changes to remote repository
     git pf         Force push changes to remote repository
     git undo       Undo last commit, keep changes
     git ghelp      Show this help message
     git gconfig    Open config file in default editor
     git gcommit    Generate AI commit message and commit changes
     git ac         Add all changes and commit with AI message
     git c          Shorthand for 'git gcommit'
   ```

## 💡 Basic Usage

### Generating AI Commit Messages

After making changes to your project:

1. Stage your changes:

   ```
   git add .
   ```

2. Generate and apply an AI commit message:

   ```
   git c
   ```

   Example output:

```
[On Ready] Generating commit message...

[Thought] The changes include adding a new file for VSCode settings and updating the .gitignore to include the new settings file. These changes are related to
development environment configuration and do not affect the application's functionality.

[Generated commit message]
chore: update vscode settings and gitignore

- Add .vscode/settings.json with YAML schema configuration
- Update .gitignore to include .vscode/settings.json
- Add .vscode/extensions.json with recommended extensions

These changes improve the development environment by ensuring proper YAML schema validation and managing VSCode settings and extensions.

? Do you want to commit the changes with this message? (Use arrow keys)
 » yes
   retry
   retry by feedback
   exit
```

3. Choose the most appropriate message using arrow keys and press Enter.

### Customizing Commit Messages with Project Configuration

GCOP uses a two-level configuration system:

- **User config**: Global settings stored in `~/.zeeland/gcop/config.yaml` (includes your API keys)
- **Project config**: Repository-specific settings in `.gcop/config.yaml` (overrides user config)

This approach lets you keep sensitive information in your user config while customizing project-specific elements like commit templates.

You can customize how GCOP generates commit messages for specific projects:

1. Initialize a project-level configuration:

   ```
   gcop init-project
   ```

   This creates a `.gcop/config.yaml` file in your project root.

2. Edit the configuration to customize commit message templates:

   ```yaml
   commit_template: |
     <good_example>
     <commit_message>
     feat(backend): add user authentication API
     
     - Implement JWT token generation and validation
     - Add rate limiting for login attempts
     - Create user session management endpoints
     
     Related: #123
     Testing: Added unit tests for auth flows
     </commit_message>
     </good_example>
     
     <bad_example>
     <commit_message>added login stuff</commit_message>
     </bad_example>
     
     # PROJECT GUIDELINES:
     # 1. Use conventional commits format (feat/fix/docs)
     # 2. Include ticket number for tracked issues
     # 3. Mention testing strategy for new features
   ```

3. Use GCOP normally with `git c` or `git ac` - the AI will now follow your custom template!

This approach helps teams maintain consistent commit messages and follow project-specific conventions. Project configurations take priority over global settings, so each repository can have its own standards.

> **Important:** Keep your API keys in user config (`~/.zeeland/gcop/config.yaml`), not in project config. This keeps sensitive information secure and separate from your codebase.

For more advanced configuration options, see [Project-Based Configuration](https://gcop.zeeland.top/other/config-your-project-config).


### Repository Insights

Get detailed information about your repository:

```
git info
```

This command displays comprehensive repository statistics including:

- Project name and branch information
- Commit history and contributor metrics
- File type distribution and repository size
- Most active contributors and frequently changed files

### Workflow Automation Commands

GCOP provides several time-saving command combinations:

- `git ac`: Add all changes and commit with an AI-generated message
- `git acp`: Add all changes, commit with AI message, and push to remote
- `git cp`: Commit with AI message and push to remote
- `git undo`: Undo the last commit while keeping changes staged
- `git p`: Push to the current branch
- `git pf`: Force push to the current branch (use with caution)

## 🔧 Configuration

To modify your settings:

1. Open the config file:

   ```
   git gconfig
   ```

2. Edit the `config.yaml` file to customize:
   - AI model settings
   - Commit message templates
   - Git history learning preferences
   - Project-specific configurations

3. Save and close the file.

## 📚 Learn More

- [Detailed Documentation](https://gcop.zeeland.top/)
- [Contribution Guidelines](CONTRIBUTING.md)
- [Changelog](https://github.com/Undertone0809/gcop/releases)

### Makefile usage

[`Makefile`](https://github.com/Undertone0809/gcop/blob/main/Makefile)
contains a lot of
functions for faster development.

<details>
<summary>Install all dependencies and pre-commit hooks</summary>
<p>

```bash
make install
```

</p>
</details>

<details>
<summary>Codestyle and type checks</summary>
<p>

Automatic formatting uses `ruff`.

```bash
make polish-codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `ruff` and `darglint` library

</p>
</details>

<details>
<summary>Code security</summary>
<p>

> If this command is not selected during installation, it cannnot be used.

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues
with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>All linters</summary>
<p>

Of course there is a command to run all linters in one:

```bash
make lint
```

the same as:

```bash
make check-codestyle && make test && make check-safety
```

</p>
</details>

<details>
<summary>Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More
information [about docker](https://github.com/Undertone0809/python-package-template/tree/main/%7B%7B%20cookiecutter.project_name%20%7D%7D/docker).

</p>
</details>

<details>
<summary>Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📦 Techs

- [Promptulate: Large language model automation and Autonomous Language Agents development framework](https://github.com/Undertone0809/promptulate)
- [P3G: Python Packages Project Generator](https://github.com/Undertone0809/P3G)

## 🛡 License

[![License](https://img.shields.io/github/license/Undertone0809/gcop)](https://github.com/Undertone0809/gcop/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license.
See [LICENSE](https://github.com/Undertone0809/gcop/blob/main/LICENSE) for more details.

## 🤝 Support

For more information, please
contact: [zeeland4work@gmail.com](mailto:zeeland4work@gmail.com)

See anything changelog, describe the [telegram channel](https://t.me/zeeland0809)

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/P3G-%F0%9F%9A%80-brightgreen)](https://github.com/Undertone0809/python-package-template)

This project was generated with [P3G](https://github.com/Undertone0809/P3G)
