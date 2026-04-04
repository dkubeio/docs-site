# RAGFlow API Reference

RAGFlow exposes a REST API at `/ragflow/v1/` when deployed on DKubeX. All API calls require an API key.

---

## Authentication

Generate an API key in the RAGFlow UI: **Settings > API Key > + Create API Key**.

Include it in every request:

```
Authorization: Bearer <api-key>
```

---

## Knowledge Base

### Create a Knowledge Base

```
POST /ragflow/v1/kb/create
```

**Body:**

```json
{
  "name": "Product Docs",
  "description": "Product documentation knowledge base",
  "embedding_model": "BAAI/bge-small-en-v1.5",
  "chunk_method": "General"
}
```

### List Knowledge Bases

```
GET /ragflow/v1/kb/list
```

### Delete a Knowledge Base

```
DELETE /ragflow/v1/kb/<kb-id>
```

---

## Documents

### Upload a Document

```
POST /ragflow/v1/document/upload
Content-Type: multipart/form-data
```

**Form fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `kb_id` | string | Yes | Target knowledge base ID |
| `file` | file | Yes | Document file (PDF, DOCX, etc.) |

### Trigger Parsing

```
POST /ragflow/v1/document/run
```

**Body:**

```json
{
  "doc_ids": ["<document-id>"]
}
```

### Get Document Status

```
GET /ragflow/v1/document/<doc-id>
```

---

## Retrieval

### Test Retrieval

```
POST /ragflow/v1/chunk/retrieval_test
```

**Body:**

```json
{
  "kb_id": "<kb-id>",
  "question": "What is the return policy?",
  "top_k": 5,
  "similarity_threshold": 0.2
}
```

**Response:** Ranked list of chunks with similarity scores and source metadata.

---

## Chat

### List Assistants

```
GET /ragflow/v1/chat/list
```

### Create a Chat Session

```
POST /ragflow/v1/chat/<assistant-id>/session/create
```

### Chat Completion

```
POST /ragflow/v1/chat/<assistant-id>/completions
```

**Body:**

```json
{
  "question": "How do I reset my password?",
  "session_id": "<session-id>",
  "stream": false
}
```

**Response:** LLM-generated answer with source citations referencing specific document chunks.

### Streaming

Set `"stream": true` to receive Server-Sent Events (SSE) for real-time token streaming.

---

## Common Response Format

All API responses follow this structure:

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

| Code | Meaning |
|------|---------|
| `0` | Success |
| Non-zero | Error (check `message` for details) |

---

## Rate Limits and Notes

- API keys are scoped to the user who created them
- File upload size limits depend on the cluster's ingress configuration
- Parsing is asynchronous — poll document status after triggering a parse
- The MCP server (port 9382, internal) provides Model Context Protocol access for compatible AI tools
