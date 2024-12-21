# Configure Your Project

GCOP supports project-level configuration, allowing you to set different configuration options for different projects. This guide will help you understand how to configure your project.

## Initialize Project Configuration

To initialize GCOP configuration in your project, simply run in the project root directory:

```bash
gcop init-project
```

This command creates a `.gcop/config.yaml` file in your project root directory. If the configuration file already exists, the command will indicate that it has been initialized.

## Configuration File Structure

The default content of the project configuration file `.gcop/config.yaml` is as follows:

```yaml
commit_template: null # Commit message template
enable_data_improvement: false # Whether to enable data improvement
include_git_history: false # Whether to include git history in the prompt
model:
  api_base: eg:https://api.openai.com/v1
  api_key: sk-xxx
  model_name: provider/name,eg openai/gpt-4o
```

## Configuration Priority

GCOP's configuration priority is as follows (from highest to lowest):

1. Project-level configuration (`.gcop/config.yaml`)
2. Global configuration (`~/.gcop/config.yaml`)

This means that project-level configuration will override global configuration, allowing you to set different configurations for different projects.

## View Current Configuration

To view the current effective configuration, use:

```bash
gcop show-config
```

This command displays all currently effective GCOP configuration items, including model configuration, commit templates, etc.

## Important Notes

1. Make sure to add `.gcop/` to your `.gitignore` file to avoid committing sensitive information like API keys to version control.

2. It's recommended to use environment variables for storing API keys rather than writing them directly in the configuration file.

3. Changes to the project configuration file take effect immediately, no need to restart GCOP.

## Troubleshooting

If you encounter configuration-related issues, you can:

1. Use `gcop show-config` to check the current configuration
2. Ensure the configuration file format is correct (valid YAML format)
3. Verify that the API key and model name are correct
4. Check file permissions

For more help, refer to the [Configuration Guide](/guide/configuration) or submit a GitHub issue.
