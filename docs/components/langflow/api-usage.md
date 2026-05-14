# API Usage

There are two ways to call a flow over HTTP: via the **main Langflow instance** (useful during development), or via a **deployed flow pod** (for production use).

---

## Option 1 — Call via the Main Langflow Instance

The main Langflow backend exposes a run endpoint for any saved flow. This is useful for testing during development but shares resources with all other users.

### Endpoint

```
POST /langflow/api/v1/run/{flow_id}
```

`flow_id` is the UUID visible in the URL when the flow is open in the canvas.

### Request body

```json
{
  "input_value": "Hello, Langflow!",
  "output_type": "chat",
  "input_type": "chat",
  "tweaks": {}
}
```

| Field | Description |
|-------|-------------|
| `input_value` | Text sent to the flow's chat/text input |
| `output_type` | `"chat"` or `"text"` depending on your flow's output component |
| `input_type` | `"chat"` or `"text"` depending on your flow's input component |
| `tweaks` | Per-run overrides keyed by component ID (optional) |

### Authentication

Generate a Langflow API key from **Settings → API Keys** and send it as the `x-api-key` header.

### cURL example

```bash
curl -X POST \
  "https://<platform-host>/langflow/api/v1/run/<flow_id>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LANGFLOW_API_KEY" \
  -d '{"input_value": "Hello", "output_type": "chat", "input_type": "chat"}'
```

### Python example

```python
import requests, os

response = requests.post(
    f"https://<platform-host>/langflow/api/v1/run/{flow_id}",
    headers={"x-api-key": os.environ["LANGFLOW_API_KEY"]},
    json={"input_value": "Hello", "output_type": "chat", "input_type": "chat"},
)
print(response.json())
```

---

## Option 2 — Call a Deployed Flow Pod

When you [deploy a flow](./deploying-flows.md), it runs as a standalone pod with its own internal endpoint. This is the recommended approach for production workloads.

### Getting the cURL command

1. Go to **Deployment Mode** in the header.
2. Click the deployment row to open the detail panel.
3. Click the **cURL** tab.

The cURL command is pre-built with the correct endpoint, headers, and request body for your specific flow. It looks like:

```bash
curl -X POST \
  "http://langflow-deployment-<name>.dkubex-apps.svc.cluster.local:7860/api/v1/run/<flow_id>?stream=false" \
  -H "Content-Type: application/json" \
  -d '{"input_value": "...", "input_type": "chat", "output_type": "chat"}'
```

### Endpoint structure

```
http://langflow-deployment-<slug>.dkubex-apps.svc.cluster.local:7860/api/v1/run/<flow_id>
```

| Part | Value |
|------|-------|
| `<slug>` | The deployment name you chose, lowercased with spaces replaced by hyphens |
| `<flow_id>` | UUID of the source flow |
| Port | Always `7860` |

> **Cluster-internal only:** This address is only reachable from within the `dkubex-apps` namespace (or other namespaces with cross-namespace access). It is not exposed externally. Contact your cluster administrator if you need external access via an ingress or gateway route.

### No authentication required

Deployed flow pods do not require an API key by default — they are secured at the network level by being cluster-internal only.

---

## Response Format

Both endpoints return the same Langflow response structure:

```json
{
  "session_id": "...",
  "outputs": [
    {
      "inputs": { "input_value": "Hello" },
      "outputs": [
        {
          "results": {
            "message": {
              "text": "Hello! How can I help you?",
              ...
            }
          },
          "component_display_name": "Chat Output",
          ...
        }
      ]
    }
  ]
}
```

The assistant's reply is at `outputs[0].outputs[0].results.message.text` for chat flows.

---

## Streaming

Add `?stream=true` to the endpoint URL to receive a server-sent events (SSE) stream instead of a single JSON response. Each event contains a partial token.

```bash
curl -X POST \
  ".../api/v1/run/<flow_id>?stream=true" \
  -H "Content-Type: application/json" \
  -d '{"input_value": "Hello", "input_type": "chat", "output_type": "chat"}'
```
