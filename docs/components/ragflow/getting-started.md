# RAGFlow on DKubeX — Getting Started

RAGFlow is an open-source RAG (Retrieval-Augmented Generation) engine with deep document understanding. It is available as a pre-integrated component on the DKubeX platform.

---

## What RAGFlow Does

- **Document ingestion**: Upload PDFs, Word, Excel, PowerPoint, Markdown, HTML, images, audio, and video. RAGFlow preserves layout, tables, figures, and headers during parsing.
- **Knowledge base management**: Create isolated knowledge bases with per-KB embedding models and chunking strategies.
- **Hybrid search**: Dense vector + BM25 keyword fusion with configurable similarity thresholds and re-ranking.
- **Conversational RAG**: Multi-turn chat grounded in your documents, with chunk-level source citations.
- **Agentic pipelines**: Visual flow editor to build multi-step agent workflows (retrieval, classification, code execution, web search, and more).
- **Multiple LLM/embedding backends**: OpenAI, Anthropic, Ollama (local), HuggingFace TEI, and 20+ providers.
- **REST API and MCP server**: Full programmatic access for all operations.

---

## Accessing RAGFlow

Once installed on your DKubeX cluster, RAGFlow is available at:

```
https://<platform-host>/ragflow/
```

Authentication is handled by the DKubeX platform — no separate login is required. Your platform identity is passed to RAGFlow automatically.

---

## Quick Start

### 1. Register a Model Provider

1. Click the avatar (top-right) and go to **Settings > Model Providers**
2. Select a provider (e.g., Ollama, OpenAI)
3. Enter the base URL and API key
4. Click **Add Model** and choose the model type (Chat, Embedding, Rerank)
5. Enter the model name as the provider expects it

### 2. Create a Knowledge Base

1. Go to **Knowledge Base** in the left sidebar
2. Click **+ Create knowledge base**
3. Set a name, select an embedding model, and choose a chunk method:
   - `General` — paragraph-level, works for most documents
   - `Q&A` — extracts question-answer pairs
   - `Manual` — preserves heading hierarchy (technical docs)
   - `Table` — optimized for spreadsheets
   - `Paper` — academic paper structure
4. Click **Save**

### 3. Upload and Parse Documents

1. Open your knowledge base and click **+ Add file** (or drag-and-drop)
2. Supported formats: PDF, DOCX, XLSX, PPTX, MD, TXT, HTML, PNG, JPG, MP3, MP4
3. Select files and click **Parse** — watch status go from `UNSTART` to `SUCCESS`
4. Click a file row and go to **Chunks** to inspect extracted content

### 4. Test Retrieval

1. Inside your knowledge base, go to the **Testing** tab
2. Enter a query and adjust sliders (similarity threshold, top-k, vector weight)
3. Click **Test** to see ranked chunks with similarity scores
4. Tune parameters before connecting to a chat assistant

### 5. Create a Chat Assistant

1. Go to **Chat** in the left sidebar and click **+ Create assistant**
2. Select an LLM and configure generation parameters (temperature, top-p, max tokens)
3. Customize the system prompt — use `{knowledge}` where retrieved chunks should be injected
4. Attach one or more knowledge bases
5. Click **Save**, then **Start chat** to begin a conversation

### 6. Build an Agent (Optional)

1. Go to **Agent** in the left sidebar and click **+ Create agent**
2. Drag nodes onto the visual canvas: Retrieval, Generate, Categorize, Code, HTTP Request, etc.
3. Connect nodes and configure each one
4. Click **Run** to test with sample input

---

## Architecture on DKubeX

RAGFlow is deployed as a Helm chart with the following components:

| Component | Purpose |
|-----------|---------|
| **RAGFlow app** | Main application (web UI, API server, MCP server) |
| **MySQL** | Relational store for users, knowledge bases, and metadata |
| **Redis** | Cache and session storage |
| **MinIO** | S3-compatible object storage for uploaded documents |
| **Infinity** | Vector database and document engine (default) |

Alternative document engines (Elasticsearch, OpenSearch) are available via Helm configuration.

---

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/ragflow/` | Web UI |
| `/ragflow/v1/` | REST API |
| Port 9382 (internal) | MCP server |

### API Examples

```bash
# List chat assistants
curl -H "Authorization: Bearer <api-key>" \
  https://<platform-host>/ragflow/v1/chat/list

# Chat with an assistant
curl -X POST -H "Authorization: Bearer <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the refund policy?"}' \
  https://<platform-host>/ragflow/v1/chat/<assistant-id>/completions
```

API keys are created in **Settings > API Key** within the RAGFlow UI.

---

## Configuration

RAGFlow is configured through Helm values. Key settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `ragflow.proxyAuth.enabled` | Enable platform SSO authentication | `true` |
| `ragflow.basePath` | URL base path | `/ragflow` |
| `env.DOC_ENGINE` | Document engine selection | `infinity` |
| `mysql.enabled` | Deploy MySQL in-chart | `true` |
| `redis.enabled` | Deploy Redis in-chart | `true` |
| `minio.enabled` | Deploy MinIO in-chart | `true` |

Each dependency (MySQL, Redis, MinIO) can point to an external service by setting `<component>.enabled: false` and populating the corresponding external host/port environment variables.

---

## Further Reading

- [RAGFlow GitHub](https://github.com/infiniflow/ragflow)
- [RAGFlow API Documentation](https://github.com/infiniflow/ragflow/blob/main/docs/references/http_api_reference.md)
- [DKubeX Integration Details](../dkubex-integration.md)
