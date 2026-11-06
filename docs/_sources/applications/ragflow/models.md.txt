# Using Models on DKubeX

RAGFlow needs models to power your knowledge bases and chats: a **chat** model to generate answers, an **embedding** model to index and retrieve your documents, and optionally a **rerank** model to sharpen retrieval.

On DKubeX you get all of these from the built-in **DKubeX** model provider, which connects to the cluster's **SecureLLM** service. The DKubeX provider is preconfigured with your DKubeX user key, so RAGFlow automatically registers the models you have access to.

## Add the DKubeX provider

1. Click your avatar in the top-right of the page and open the **Model providers** page.
2. In the **Available models** column on the right, find the built-in **DKubeX** provider and click **Add**.
3. RAGFlow registers the chat, embedding, and rerank models you have access to (the ones deployed in Model Studio). They appear under **Added models**.

## Refresh models

Use **Refresh models** to re-sync with SecureLLM. The list is scoped to the models your DKubeX user is permitted to use, so any models you can no longer access are removed and you only ever see the ones currently available to you.

## Set your default models

Registering models does not choose defaults for you. In the **Set default models** column, pick your default **LLM** (chat), **embedding**, and — optionally — **rerank** models. Until you choose, the model dropdowns show a **Select model** placeholder.

Once your defaults are set, you can [create a knowledge base](./knowledge-bases.md) and [start a chat](./chat.md).
