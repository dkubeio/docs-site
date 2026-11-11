# Testing a Model in the Playground

The **Playground** is Model Studio's inference workbench for testing your deployed models — chat,
document-grounded chat (RAG), embeddings, reranking, and text-to-speech.

## Prerequisites

- A deployed model in the **Running** state (see
  [Deploying a Model on CPU](deploying-a-model-on-cpu.md) or [on GPU](deploying-a-model-on-gpu.md)).
- For **RAG**, a deployed **embedding** model as well.

## Select a model

1. In Model Studio, open **Playground**.
2. In the left panel, pick a model from the **Model** dropdown (use the **Type** filter to narrow it).
   The dropdown only lists models that support the current tab's capability.
3. Optionally set the parameters: **System Prompt**, **Temperature**, **Max Tokens**, **Context
   Length**.

## Run inference

Choose the tab for what you want to test:

- **Chat** — type a message and press **Enter** (or **Send**). Responses stream in; token usage is
  shown after each response. Use **Copy** or **Clear** as needed.
- **RAG** — upload documents (PDF, DOCX, TXT). The Playground chunks and embeds them with a deployed
  embedding model, retrieves the relevant passages, and grounds the answer — responses include source
  attribution.
- **Embeddings** — enter text and generate its embedding vector.
- **Reranking** — enter a query plus one passage per line; results are sorted by relevance score.
- **Text to Speech** — enter text and synthesize audio.

:::{note}
Vision, image generation, and speech-to-text are coming in a future KubeAI release for self-hosted LLM
models.
:::
