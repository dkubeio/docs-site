# Getting Started with SecureLLM

SecureLLM is a self-hosted AI gateway that gives you a single, OpenAI-compatible endpoint for multiple LLM providers — with API key management, usage tracking, rate limiting, and safety guardrails built in.

---

## Prerequisites

- Docker and Docker Compose **or** Go 1.24+ (with CGO enabled)
- API key(s) for at least one LLM provider (OpenAI, Anthropic, or a custom OpenAI-compatible endpoint)

---

## Quick Start (Docker Compose)

1. **Clone the repository** and navigate to the root directory.

2. **Set the required environment variables:**

   ```bash
   export ADMIN_USERS="you@example.com"
   export OPENAI_API_KEY="sk-..."
   ```

3. **Start the gateway:**

   ```bash
   docker compose up
   ```

The gateway is now running at `http://localhost:8081`.
The admin UI is available at `http://localhost:8081/admin/`.

> **Note:** `ADMIN_USERS` is a comma-separated list of SSO usernames that have admin access. In a production setup, SecureLLM sits behind an SSO proxy (e.g., oauth2-proxy, Authelia, Authentik) that injects the `X-Forwarded-User` header.

---

## Quick Start (Without Docker)

Requires Go 1.24+ with CGO enabled.

```bash
# Build the binary
cd backend
CGO_ENABLED=1 go build -o ../securellm .
cd ..

# Set environment variables
export ADMIN_USERS="you@example.com"
export OPENAI_API_KEY="sk-..."
export DEV_MODE=true   # enables a local login page for development

# Run
./securellm
```

With `DEV_MODE=true` you can log in at `http://localhost:8081/admin/login` without an SSO proxy.

---

## Getting Your First API Key

1. Open the admin UI: `http://localhost:8081/admin/`
2. Log in (or use the dev login page if `DEV_MODE=true`).
3. Navigate to **Keys** in the sidebar.
4. Click **Create Key**, enter a name, and click **Create**.
5. Copy the key shown — it starts with `sk-` and is displayed **only once**.

---

## Making Your First Request

Replace `<your-key>` with the key you just created.

```bash
curl http://localhost:8081/v1/chat/completions \
  -H "Authorization: Bearer <your-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

---

## Using SecureLLM as a Drop-in OpenAI Replacement

Because SecureLLM exposes the same `/v1` interface as OpenAI, you can point any OpenAI-compatible client at it by changing the base URL.

**Python (openai SDK):**

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8081/v1",
    api_key="<your-key>",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

**JavaScript / TypeScript (openai SDK):**

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8081/v1",
  apiKey: "<your-key>",
});

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

---

## Streaming Responses

Streaming works the same way as with the OpenAI API — set `"stream": true` in your request body.

```bash
curl http://localhost:8081/v1/chat/completions \
  -H "Authorization: Bearer <your-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Count to 5."}],
    "stream": true
  }'
```

---

## Routing to a Specific Provider

By default, SecureLLM routes requests automatically based on the configured routing strategy. To force a specific provider for a single request, add the `x-provider` header:

```bash
curl http://localhost:8081/v1/chat/completions \
  -H "Authorization: Bearer <your-key>" \
  -H "Content-Type: application/json" \
  -H "x-provider: anthropic" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Next Steps

- [API Reference](./api-reference.md) — full endpoint reference with request/response schemas
- [Configuration](./configuration.md) — all environment variables and tuning options
