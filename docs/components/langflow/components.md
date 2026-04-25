# Components

Components are the building blocks of a flow. Langflow ships with a wide catalog covering inputs, models, memory, retrieval, tools, and outputs.

## Categories

- **Inputs / Outputs** — Chat input, text input, file loaders, chat output, text output.
- **Models** — OpenAI, Anthropic, Mistral, Ollama, Hugging Face, and more.
- **Prompts** — Prompt templates with variable substitution.
- **Memory** — Conversation buffers, vector-backed memory stores.
- **Vector Stores** — Chroma, Pinecone, Weaviate, PGVector, FAISS.
- **Embeddings** — OpenAI, Cohere, Hugging Face, and local embeddings.
- **Agents** — Tool-calling agents with configurable tool sets.
- **Tools** — Web search, Python REPL, API request, custom tools.
- **Logic** — Conditional routers, loops, and parallel execution.

## Configuring a Component

1. Click a component on the canvas to open its side panel.
2. Fill in required fields (marked with `*`).
3. Toggle **Advanced** to reveal less-common options.
4. Use the **Code** tab to view or customize the underlying Python.

## Custom Components

You can create your own component by opening the **Custom Component** template, writing a Python class, and saving. See the internal developer guide for the full API.
