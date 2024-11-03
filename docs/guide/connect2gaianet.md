---
title: Connect to GaiaNet
description: Connect to GaiaNet to use GCOP (Git Copilot).
head:
  - - meta
    - property: og:title
      content: Connect to GaiaNet
    - property: og:description
      content: Connect to GaiaNet to use GCOP (Git Copilot).
---

# Connect to GaiaNet

GaiaNet is a decentralized computing infrastructure that enables everyone to create, deploy, scale, and monetize their own AI agents. This guide will show you how to configure GCOP to use GaiaNet as your AI provider.

## Prerequisites

Before you begin, ensure you have:

- GCOP installed (see [Quick Start Guide](./quick-start.md) for installation instructions)
- A GaiaNet account and access to a GaiaNet node

For more information about GaiaNet, you can check out:

- [GaiaNet Node GitHub Repository](https://github.com/GaiaNet-AI/gaianet-node)
- [GaiaNet Documentation](https://docs.gaianet.ai/intro)

## Configuration Steps

1. Set up a GaiaNet node by following the instructions in the [GaiaNet Node User Guide](https://docs.gaianet.ai/user-guide/nodes).

2. Open the GCOP configuration file:

   ```
   git gconfig
   ```

3. Edit the `config.yaml` file to use GaiaNet as the provider， here we use GaiaNet llama model as an example:

   ```yaml
   model:
     model_name: openai/llama
     api_key: any-value
     api_base: https://llama.us.gaianet.network/v1
   ```

4. Save and close the configuration file.

## Verifying the Configuration

To ensure GCOP is correctly configured to use GaiaNet:

1. Stage some changes in your Git repository:

   ```
   git add .
   ```

2. Generate an AI commit message:

   ```
   git c
   ```

3. If configured correctly, you should see commit message suggestions generated using your GaiaNet node.

## Troubleshooting

If you encounter any issues:

- Double-check your GaiaNet node API key in the configuration file
- Ensure your GaiaNet node is running and accessible
- Verify your internet connection

For more help, refer to the [FAQ](../faq.md) or consult the [GaiaNet documentation](https://docs.gaianet.ai/intro).

By following these steps, you can harness the power of GaiaNet's decentralized AI infrastructure to enhance your Git workflow with GCOP.
