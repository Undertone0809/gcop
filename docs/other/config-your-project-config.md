# Project-Based Configuration Made Easy

GCOP makes it simple to customize settings for each of your projects! This guide walks you through setting up project-specific configurations that work perfectly for your team's needs.

## Why Use Project-Based Configuration?

Different projects often need different settings. With GCOP's project configuration, you can:

- Use different AI models for different projects
- Set unique commit message templates for each team
- Keep configurations separate and organized

## Real-World Example: Standardizing Commit Messages Across Your Team

Want your team to write consistent, informative commit messages? Project configuration makes it easy!

### How It Works in Practice: The FinTech Example

Imagine a financial technology team that needs detailed commit messages to streamline their review process. Here's how they configure GCOP:

```yaml
commit_template: |
  <good_example>
  <commit_message>
  feat(payment): implement cryptocurrency payment gateway
  
  - Add Bitcoin and Ethereum payment processing
  - Create transaction history component for crypto payments
  - Implement wallet address validation with checksum
  
  JIRA: FIN-423
  Security: Medium impact, wallet validation prevents transaction errors
  QA: Added unit tests for all validation logic
  </commit_message>
  <reason>
  Has required elements:
  - Type prefix with scope in parentheses
  - Descriptive bullet points
  - JIRA ticket reference
  - Security impact assessment
  - QA testing notes
  </reason>
  </good_example>
  
  <bad_example>
  <commit_message>added crypto payments</commit_message>
  <reason>
  Missing required elements:
  - No type/scope prefix
  - No bullet points for changes
  - No JIRA reference
  - No security or QA notes
  </reason>
  </bad_example>
  
  # TEAM REQUIREMENTS:
  # 1. Always include relevant ticket number (JIRA: XXX-###)
  # 2. For features affecting payment systems, include security impact
  # 3. Mention QA strategy for testable changes
  # 4. Use conventional commit types with scope (feat/fix/docs/etc)
  # 5. Include bullet points for multiple changes
```

With this setup, team members simply use GCOP as normal. The AI automatically generates properly formatted commit messages following all team standards—no more forgetting ticket numbers or skipping important details!

## Getting Started in 30 Seconds

Setting up project configuration is quick:

```bash
gcop init-project
```

That's it! This creates a `.gcop/config.yaml` file in your project's root directory. If the file already exists, you'll see a message letting you know.

## What's in the Configuration File?

Your `.gcop/config.yaml` file contains these key settings:

```yaml
commit_template: null # Your commit message template
enable_data_improvement: false # Whether to enable data improvement
include_git_history: false # Whether to include git history
model:
  api_base: eg:https://api.openai.com/v1
  api_key: sk-xxx
  model_name: provider/name,eg openai/gpt-4o
```

## How Configuration Priority Works

GCOP follows a simple priority system:

1. Project-level settings (`.gcop/config.yaml`) come first
2. Global settings (`~/.gcop/config.yaml`) are used as fallbacks

This means you can set different configurations for different projects, but keep common settings global.

## Quick Command: Check Your Current Settings

Want to see what settings are active? Just run:

```bash
gcop show-config
```

This shows you exactly which configuration options are currently in effect.

## Pro Tips for Smooth Setup

1. **Security first**: Add `.gcop/` to your `.gitignore` file to keep API keys private

2. **Use environment variables**: Store sensitive API keys as environment variables instead of in the config file

3. **Changes apply immediately**: No need to restart anything when you update your settings

## Troubleshooting Common Issues

Running into problems? Try these quick fixes:

1. Run `gcop show-config` to see what settings are active
2. Check that your config file has valid YAML formatting
3. Double-check your API key and model name
4. Verify file permissions are correct

Need more help? Check the [Configuration Guide](/guide/configuration) or open an issue on GitHub.
