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
include_git_history: false
# Optional, default is false. Attention: This feature is not supported yet.
enable_data_improvement: false
# Optional, if you want to customize the commit template. 
commit_template: |
  <good_example>
  <commit_message>
  feat: implement user registration

  - Add registration form component
  - Create API endpoint for user creation
  - Implement email verification process

  This feature allows new users to create accounts and verifies
  their email addresses before activation. It includes proper
  input validation and error handling.
  </commit_message>
  <reason>contain relevant detail of the changes, not just one line</reason>
  </good_example>

  <bad_example>
  <commit_message>feat: add user registration</commit_message>
  <reason>only one line, need more detail based on guidelines</reason>
  </bad_example>
```

### Commit Message Template

gcop provides a default `commit template` to guide language model how to generate commit message. Default template is as follows:

```yaml
... # other configurations
commit_template: |
  <good_example>
  <commit_message>
  feat: implement user registration

  - Add registration form component
  - Create API endpoint for user creation
  - Implement email verification process

  This feature allows new users to create accounts and verifies
  their email addresses before activation. It includes proper
  input validation and error handling.
  </commit_message>
  <reason>contain relevant detail of the changes, not just one line</reason>
  </good_example>

  <bad_example>
  <commit_message>feat: add user registration</commit_message>
  <reason>only one line, need more detail based on guidelines</reason>
  </bad_example>
```

You can customize the commit message template to guide language model how to generate commit message.

The following example how to generate a commit message in Chinese:


```yaml
... # other configurations
commit_template: |
  <good_example>
  <commit_message>
  功能：实现用户注册

  - 添加注册表单组件
  - 创建用户创建的API端点
  - 实现邮箱验证流程

  此功能允许新用户创建账号，并在激活前验证其邮箱地址。
  包含适当的输入验证和错误处理。
  </commit_message>
  <reason>包含了相关更改的详细信息，不仅仅是一行描述</reason>
  </good_example>

  <bad_example>
  <commit_message>功能：添加用户注册</commit_message>
  <reason>只有一行描述，不符合规范，需要更多细节</reason>
  </bad_example>
  <bad_example>
  <commit_message>feat: add user registration</commit_message>
  <reason>不能使用英文输出 commit message</reason>
  </bad_example>

  请使用中文输出 commit message。
```

Example output:

```
docs: 更新文档结构和内容

- 删除过时的API示例文档
- 更新配置指南，修改默认配置选项
- 重命名FAQ文档为How to guide，并更新内容
- 更新快速开始指南中的模型配置链接
- 移动changelog和connect2gaianet文档到other目录
- 更新贡献指南，包括开发工作流程和代码标准
- 更新模型配置指南，添加配置语言模型的说明
- 更新gcop/prompt.py中的默认提交模板
- 修复utils/__init__.py中的文件读取编码问题
```

:::info TIP
We recommend you fork the default commit template and customize it to your own needs.
:::
