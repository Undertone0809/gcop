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

GCOP (Git Copilot) is an intelligent assistant that enhances your Git workflow by automating commit message generation using AI. It's designed to make your development process smoother and more efficient.

## 🚀 Key Features

- **Smart Commit Messages**: Let AI generate meaningful commit messages based on your changes.
- **Flexible AI Integration**: Works with various large language models (LLMs) of your choice.
- **Simplified Git Commands**: Powerful aliases for common Git operations to speed up your workflow.

## 📦 Techs

- [Promptulate: Large language model automation and Autonomous Language Agents development framework](https://github.com/Undertone0809/promptulate)
- [P3G: Python Packages Project Generator](https://github.com/Undertone0809/P3G)
- [Gamma: Generate gcop Banner here](https://gamma.app/)
- [gpt-4o: Generate project code](https://openai.com/)

## Video Demo

This video shows how to use gcop to generate a commit message.

[![Gcop is your git AI copilot](https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20240624003422.png)](https://www.youtube.com/watch?v=j7qKI_TdhXs "Gcop is your git AI copilot")

## 🛠️ Getting Started

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
config your model [here](./docs/guide/how-to-config-model.md):

> `config.yaml` store path:
>
> - Windows: `%USERPROFILE%\.gcop\config.yaml`
> - Linux: `~/.gcop/config.yaml`
> - MacOS: `~/.gcop/config.yaml`

4. Verify the installation:

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
   ? Select a commit message to commit (Use arrow keys)
    » feat: Implement user authentication system
      docs: Update installation instructions in README
      fix: Resolve database connection timeout issue
      style: Improve code formatting in src/main.py
      retry
   ```

3. Choose the most appropriate message using arrow keys and press Enter.

### Other Useful Commands

- `git ac`: Add all changes and commit with an AI-generated message

   ```
   git ac
   ```

   Output:

   ```
   Changes added. Generating commit message...
   ? Select a commit message to commit (Use arrow keys)
    » feat: Add new user profile page
      fix: Correct CSS styling issues on mobile devices
      docs: Update API documentation for v2.0
      refactor: Optimize database queries for better performance
      retry
   ```

- `git undo`: Undo the last commit while keeping changes staged

   ```
   git undo
   ```

   Output:

   ```
   HEAD is now at a1b2c3d Previous commit message
   Changes from the last commit are now staged.
   ```

- `git p`: Push to the current branch

   ```
   git p
   ```

   Output:

   ```
   Enumerating objects: 5, done.
   Counting objects: 100% (5/5), done.
   Delta compression using up to 8 threads
   Compressing objects: 100% (3/3), done.
   Writing objects: 100% (3/3), 328 bytes | 328.00 KiB/s, done.
   Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
   To https://github.com/username/repo.git
      a1b2c3d..e4f5g6h  main -> main
   ```

- `git pf`: Force push to the current branch (use with caution)
- `git gconfig`: Open the GCOP configuration file for adjustments

## 🔧 Configuration

To modify your AI model settings:

1. Open the config file:

   ```
   git gconfig
   ```

2. Edit the `config.yaml` file:

   ```yaml
   model:
     model_name: provider/name, eg openai/gpt-4o
     api_key: your_api_key
   ```

3. Save and close the file.

## 📚 Learn More

- [Detailed Documentation](https://github.com/Undertone0809/gcop/wiki)
- [Contribution Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

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
