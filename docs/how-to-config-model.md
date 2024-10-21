# How to config model?

gcop use - [Promptulate: Large language model automation and Autonomous Language Agents development framework](https://github.com/Undertone0809/promptulate) to drive the model. Promptulate allows you to create any language model and build LLM application. 

## Model template

Here is the basic template for configuring the model:

```shell
model:
  model_name: provider/name,eg openai/gpt-4o
  api_key: your_api_key
```

## OpenAI

If you want to initialize the model, you can use the following command:

```shell
model:
  model_name: openai/gpt-4o
  api_key: your_api_key
```

## Claude

```shell
model:
  model_name: claude-2
  api_key: your_api_key
```

## Deepseek

```shell
model:
  model_name: deepseek/deepseek-chat
  api_key: your_api_key
```

## Ollama

```shell
model:
  model_name: ollama/llama2
  api_key: your_api_key
  api_base: http://localhost:11434
```

## OpenAI Proxy

If you want to use Zhipu GLM4 by OpenAI proxy, you can use the following configuration:

```shell
model:
  model_name: openai/glm-4
  api_key: your_api_key
  api_base: https://open.bigmodel.cn/api/paas/v4/
```

Use `openai/model_name` provider means you are using OpenAI SDK to call the model.

## OpenRouter

```shell
model:
  model_name: openrouter/google/palm-2-chat-bison
  api_key: your_api_key
```

## HuggingFace

```shell
model:
  model_name: huggingface/gpt2
  api_key: your_api_key
```

## More models

gcop use [promptulate](https://github.com/Undertone0809/promptulate) standard to name the model. You can see how to write your model name in [here](https://www.promptulate.cn/other/how_to_write_model_name.html).

promptulate integrates litellm's capabilities and model name standards, so if you want to use any model, you can go directly to the [litellm](https://docs.litellm.ai/docs/) website to view the model name and then use it in promptulate.
