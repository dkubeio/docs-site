# Components

Components are the building blocks of a flow. Langflow ships with a wide catalog covering inputs, models, memory, retrieval, tools, and outputs. On DKubeX, additional **DKubeX Providers** components are available that connect directly to the cluster-local SecureLLM service.

## Categories

- **Input & Output** — Chat input, text input, file loaders, chat output, text output.
- **Models & Agents** — OpenAI, Anthropic, Mistral, Ollama, Hugging Face, and more.
- **LLM Operations** — Prompt templates, chains, and LLM utility components.
- **Files & Knowledge** — File loaders, document parsers, knowledge base connectors.
- **Data Sources** — Database connectors, API request components, web scrapers.
- **Processing** — Text splitters, parsers, transformers.
- **Flow Control** — Conditional routers, loops, and parallel execution.
- **Utilities** — Python REPL, custom tools, web search.
- **Prototypes** — Experimental components.
- **Tools** — Agents with tool-calling capabilities.
- **DKubeX Providers** — DKubeX-native LLM and embedding components backed by SecureLLM.

## DKubeX Providers

These components are built into every DKubeX Langflow instance and connect to the **SecureLLM** service running in the same cluster. They appear in the sidebar under **DKubeX Providers**.

### DKubeX LLM

Generates text using language models served by SecureLLM.

**Configuration:**

| Field | Description |
|-------|-------------|
| SecureLLM API Key | Your API key for the SecureLLM service (masked, saved once) |
| Model Name | Dropdown of available `TextGeneration` models — click the refresh button to populate |
| Max Tokens | Maximum tokens to generate (default 256) |
| Temperature | Sampling temperature 0–1 (default 0.1) |
| JSON Mode | Force JSON output format |
| Timeout | Request timeout in seconds (default 700) |
| Max Retries | Retries on failure (default 5) |

**Usage:**
1. Drop **DKubeX LLM** onto the canvas.
2. Enter your **SecureLLM API Key**.
3. Click the refresh icon next to **Model Name** to load available models.
4. Select a model and connect the component to your flow.

### DKubeX Embeddings

Generates vector embeddings using embedding models served by SecureLLM.

**Configuration:**

| Field | Description |
|-------|-------------|
| SecureLLM API Key | Your API key for the SecureLLM service (masked, saved once) |
| Model Name | Dropdown of available `TextEmbedding` models — click refresh to populate |
| Chunk Size | Texts per embedding batch (default 256) |
| Request Timeout | Timeout in seconds |
| Max Retries | Retries on failure (default 3) |

**Usage:**
1. Drop **DKubeX Embeddings** onto the canvas.
2. Enter your **SecureLLM API Key**.
3. Click refresh to load embedding models.
4. Connect to a Vector Store component to index documents.

> **Note:** The model dropdowns in DKubeX components show only models whose type matches the component — text generation models for **DKubeX LLM** and embedding models for **DKubeX Embeddings**. If the dropdown is empty after refreshing, verify your API key or contact your cluster administrator.

## Configuring Any Component

1. Click a component on the canvas to open its side panel.
2. Fill in required fields (marked with `*`).
3. Toggle **Advanced** to reveal less-common options.
4. Use the **Code** tab to view or customize the underlying Python.

## Global Variables

Use the **Global Variables** panel (gear icon in the sidebar) to store reusable values and API keys. Reference them from component fields with the variable picker. Global variables are encrypted at rest and resolved at deploy time for flow deployments.

## Custom Components

You can create your own component by opening the **Custom Component** template, writing a Python class that inherits from a Langflow base class, and saving. See the internal developer guide for the full component API.
