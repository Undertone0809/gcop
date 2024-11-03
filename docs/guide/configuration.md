---
title: Configuration
description: Configure GCOP (Git Copilot).
head:
  - - meta
    - property: og:title
      content: Configuration
    - property: og:description
      content: Configure GCOP (Git Copilot).
---

# Configuration

This tutorial will guide you through the process of configuring GCOP. Before you start, please make sure you have installed GCOP. See [Quick Start](/guide/quick-start) for more details.

## Storage Location

Gcop will store all configurations in the `config.yaml` file. The `config.yaml` file will be stored in:

- Windows: `%USERPROFILE%\.gcop\config.yaml`
- Linux: `~/.gcop/config.yaml`
- MacOS: `~/.gcop/config.yaml`

## All Configurations

There are all configurations you can set in the `config.yaml` file.

```yaml
model:
  # Required, the model name.
  model_name: 'provider/name,eg openai/gpt-4o '
  # Required, the API key.
  api_key: 'your_api_key'
  # Optional, the API base.
  api_base: 'your_api_base,eg https://api.openai.com/v1'
  # Optional, default is false. If true, the git history will be included in the prompt.
  include_git_history: true
  # Optional, default is false. Attention: This feature is not supported yet.
  enable_data_improvement: true
  # Optional, if you want to customize the commit template. 
  commit_template: |
    - Good Example

    ```
    feat: implement user registration

    - Add registration form component
    - Create API endpoint for user creation
    - Implement email verification process

    This feature allows new users to create accounts and verifies
    their email addresses before activation. It includes proper
    input validation and error handling.
    ```
    reason: contain relevant detail of the changes, not just one line

    - Bad Example

    ```
    feat: add user registration
    ```
    reason: only one line, need more detail based on guidelines
```

