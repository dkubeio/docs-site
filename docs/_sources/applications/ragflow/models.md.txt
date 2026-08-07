# Using Models on DKubeX

RAGFlow needs models to power your knowledge bases and chats: a **chat** model to generate answers, an **embedding** model to index and retrieve your documents, and optionally a **rerank** model to sharpen retrieval.

On DKubeX you get all of these from the built-in **DKubeX** model provider, which connects to the cluster's **SecureLLM** service. You do **not** bring your own OpenAI or Anthropic keys — you provide a single **SecureLLM API key**, and RAGFlow registers the models that key is allowed to use.

## Add the DKubeX provider

1. Click your avatar in the top-right of the page and open the **Model providers** page.
2. Find the **DKubeX** provider and start its setup.
3. Paste your **SecureLLM API key** and confirm.
4. RAGFlow contacts SecureLLM and registers the chat, embedding, and rerank models your key permits. They appear under your added models.

> If setup fails with a **"Failed to reach SecureLLM"** message, verify your API key with your cluster administrator.

## Refresh models

Use **Refresh models** to re-sync with SecureLLM. The list is scoped to your current key: any models your key no longer permits are removed, so you only ever see the models the active key can use.

## Set your default models

Registering models does not choose defaults for you. Open **Set Default Models** and pick your default **chat**, **embedding**, and **rerank** models. Until you choose, the model dropdowns show a **Select Model** placeholder.

Once your defaults are set, you can [create a knowledge base](./knowledge-bases.md) and [start a chat](./chat.md).
