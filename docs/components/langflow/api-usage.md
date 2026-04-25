# API Usage

Once a flow is deployed, you can invoke it over HTTP from any client.

## Endpoint

```
POST /api/v1/run/{flow_id}
```

Replace `{flow_id}` with the ID of your deployed flow (visible in the URL when the flow is open).

## Request

```json
{
  "input_value": "Hello, Langflow!",
  "output_type": "chat",
  "input_type": "chat",
  "tweaks": {}
}
```

- `input_value` — Text sent to the flow's chat input.
- `tweaks` — Per-run overrides keyed by component ID.

## Example: cURL

```bash
curl -X POST \
  "https://your-host/api/v1/run/<flow_id>" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LANGFLOW_API_KEY" \
  -d '{"input_value":"Hello","output_type":"chat","input_type":"chat"}'
```

## Example: Python

```python
import requests, os

r = requests.post(
    f"https://your-host/api/v1/run/{flow_id}",
    headers={"x-api-key": os.environ["LANGFLOW_API_KEY"]},
    json={"input_value": "Hello", "output_type": "chat", "input_type": "chat"},
)
print(r.json())
```

## Authentication

Generate an API key from **Settings → API Keys** and send it as the `x-api-key` header.
