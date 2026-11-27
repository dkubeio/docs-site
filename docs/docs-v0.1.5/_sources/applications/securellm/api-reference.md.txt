# API Reference

SecureLLM exposes two groups of endpoints:

- **`/v1/*`** — OpenAI-compatible inference endpoints. Authenticated with an API key.
- **`/admin/api/*`** — Admin and self-service management endpoints. Authenticated via SSO (the `X-Forwarded-User` header injected by your SSO proxy).

---

## Authentication

### API Key (`/v1/*` and `/api/*`)

Pass your API key in the `Authorization` header:

```
Authorization: Bearer sk-<your-key>
```

Keys are created in the admin UI under **Keys**. Each key is shown only once at creation.

### SSO (`/admin/api/*`)

Admin endpoints rely on an upstream SSO proxy that injects `X-Forwarded-User: username@example.com`. In `DEV_MODE` this header is set by the dev login page.

Admin-only endpoints additionally require the user to be listed in `ADMIN_USERS` or for the proxy to set `X-Auth-Request-Role: admin`.

---

## Base URL

All paths below are relative to the gateway base URL, e.g. `http://localhost:8081`.

If you deployed with a path prefix (via `BASE_PATH`), prepend it. For example, with `BASE_PATH=/securellm` the chat endpoint becomes `/securellm/v1/chat/completions`.

---

## Inference Endpoints

### `GET /health`

Returns gateway health status. No authentication required.

**Response:**

```json
{
  "status": "ok",
  "version": "0.1.0",
  "db": "ok"
}
```

---

### `GET /v1/models`

Lists models available to the caller, respecting key-level and user-level restrictions.

**Auth:** API key

**Response:**

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1715367049,
      "owned_by": "openai"
    }
  ]
}
```

---

### `POST /v1/chat/completions`

OpenAI-compatible chat completions. Supports streaming via Server-Sent Events.

**Auth:** API key

**Request body:**

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false,
  "temperature": 0.7,
  "max_tokens": 1024
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | Yes | Model ID as returned by `/v1/models` |
| `messages` | array | Yes | Conversation history |
| `stream` | boolean | No | Stream response as SSE (default: `false`) |
| `temperature` | number | No | Sampling temperature (0–2) |
| `max_tokens` | integer | No | Maximum tokens to generate |

All additional OpenAI-compatible parameters are forwarded to the upstream provider unchanged.

**Headers:**

| Header | Description |
|--------|-------------|
| `x-provider` | Override automatic routing and target a specific provider by name (e.g., `openai`, `anthropic`) |

**Non-streaming response:**

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1715367049,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Hello! How can I help?"},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  }
}
```

**Streaming response:** Each SSE event is a `data:` line containing a JSON delta, terminated by `data: [DONE]`. The format matches the OpenAI streaming protocol exactly.

---

### `POST /v1/embeddings`

OpenAI-compatible embeddings endpoint.

**Auth:** API key

**Request body:**

```json
{
  "model": "text-embedding-3-small",
  "input": "The quick brown fox"
}
```

**Response:**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [0.0023064255, -0.009327292, ...]
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
```

---

### `GET /api/usage/me`

Returns usage logs for the API key used in the request.

**Auth:** API key

**Response:**

```json
[
  {
    "id": "uuid",
    "key_id": "uuid",
    "model": "gpt-4o",
    "provider": "openai",
    "input_tokens": 20,
    "output_tokens": 10,
    "cost_usd": 0.000150,
    "latency_ms": 842,
    "status_code": 200,
    "created_at": "2024-05-10T12:34:56Z"
  }
]
```

---

## Admin Self-Service Endpoints

These endpoints are available to any authenticated SSO user.

### `GET /admin/api/me`

Returns information about the currently logged-in user.

**Response:**

```json
{
  "username": "you@example.com",
  "is_admin": false,
  "created_at": "2024-05-01T09:00:00Z"
}
```

---

### `GET /admin/api/me/restrictions`

Returns the provider and model restrictions applied to your account by an admin.

**Response:**

```json
{
  "username": "you@example.com",
  "allowed_providers": "openai,anthropic",
  "allowed_models": ""
}
```

An empty string means no restriction (all allowed).

---

### `GET /admin/api/keys`

Lists all API keys belonging to the current user.

**Response:**

```json
[
  {
    "id": "uuid",
    "name": "my-app",
    "prefix": "sk-a1b2c3d4",
    "allowed_providers": "",
    "allowed_models": "",
    "last_used_at": "2024-05-10T12:00:00Z",
    "created_at": "2024-05-01T09:00:00Z"
  }
]
```

---

### `POST /admin/api/keys`

Creates a new API key for the current user.

**Request body:**

```json
{
  "name": "my-app"
}
```

**Response:**

```json
{
  "id": "uuid",
  "name": "my-app",
  "key": "sk-a1b2c3d4e5f6...",
  "prefix": "sk-a1b2c3d4",
  "created_at": "2024-05-01T09:00:00Z"
}
```

> The `key` field contains the plaintext key and is returned **only once**. Store it immediately.

---

### `DELETE /admin/api/keys/{id}`

Revokes one of your own API keys by ID.

**Response:** `204 No Content`

---

### `GET /admin/api/models`

Lists all models available across all enabled providers.

**Response:**

```json
[
  {"id": "gpt-4o", "provider": "openai"},
  {"id": "claude-3-5-sonnet-20241022", "provider": "anthropic"}
]
```

---

### `GET /admin/api/usage/mine`

Returns all usage logs across all your keys.

---

### `GET /admin/api/usage/mine/summary`

Returns aggregated usage statistics for all your keys.

**Response:**

```json
{
  "total_requests": 1024,
  "total_input_tokens": 500000,
  "total_output_tokens": 200000,
  "total_cost_usd": 3.75,
  "by_model": {
    "gpt-4o": {"requests": 512, "cost_usd": 2.50}
  }
}
```

---

## Admin-Only Endpoints

These endpoints require admin privileges.

### Providers

#### `GET /admin/api/providers`

Lists all configured providers with their health status.

**Response:**

```json
[
  {
    "id": "uuid",
    "name": "openai",
    "type": "openai",
    "base_url": "",
    "allowed_models": "",
    "enabled": true,
    "healthy": true
  }
]
```

> API keys are never returned.

---

#### `POST /admin/api/providers`

Creates a new provider.

**Request body:**

```json
{
  "name": "my-ollama",
  "type": "custom",
  "api_key": "",
  "base_url": "http://localhost:11434/v1",
  "allowed_models": "llama3,mistral"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique identifier for this provider |
| `type` | string | `openai`, `anthropic`, `custom`, or `dkubex` |
| `api_key` | string | Provider API key (optional for some types) |
| `base_url` | string | Override base URL (required for `custom`) |
| `allowed_models` | string | Comma-separated list of allowed models (empty = all) |

---

#### `PUT /admin/api/providers/{name}`

Updates an existing provider's configuration. Accepts the same fields as `POST`.

---

#### `PUT /admin/api/providers/{name}/toggle`

Enables or disables a provider without deleting it.

**Response:**

```json
{"enabled": false}
```

---

#### `DELETE /admin/api/providers/{name}`

Permanently deletes a provider.

---

### Model Routes

Model routes define which provider handles a given model name, with an explicit priority order for fallbacks.

#### `GET /admin/api/model-routes`

Lists all model routes.

**Response:**

```json
[
  {
    "id": "uuid",
    "model_name": "gpt-4o",
    "provider_name": "openai",
    "priority": 1
  }
]
```

---

#### `POST /admin/api/model-routes`

Creates a new model route.

**Request body:**

```json
{
  "model_name": "gpt-4o",
  "provider_name": "openai",
  "priority": 1
}
```

Lower priority values are tried first. Create multiple routes for the same `model_name` with different providers to set up a fallback chain.

---

#### `PUT /admin/api/model-routes/{id}`

Updates the priority of an existing route.

**Request body:**

```json
{"priority": 2}
```

---

#### `DELETE /admin/api/model-routes/{id}`

Deletes a model route.

---

#### `GET /admin/api/model-routes/events`

SSE stream of real-time model route change notifications. Used by the admin UI.

---

### Users & Restrictions

#### `GET /admin/api/users`

Lists all SSO users who have logged into the gateway.

---

#### `GET /admin/api/users/restrictions`

Lists all per-user restrictions.

---

#### `GET /admin/api/users/restrictions/{username}`

Returns restrictions for a specific user.

**Response:**

```json
{
  "username": "dev@example.com",
  "allowed_providers": "openai",
  "allowed_models": "gpt-4o-mini,gpt-3.5-turbo"
}
```

---

#### `PUT /admin/api/users/restrictions/{username}`

Sets or updates restrictions for a user.

**Request body:**

```json
{
  "allowed_providers": "openai",
  "allowed_models": "gpt-4o-mini"
}
```

Pass an empty string to remove a restriction.

---

#### `DELETE /admin/api/users/restrictions/{username}`

Removes all restrictions for a user (grants unrestricted access).

---

#### `PATCH /admin/api/keys/{id}`

Updates the restrictions on any API key (admin can modify keys belonging to any user).

**Request body:**

```json
{
  "allowed_providers": "anthropic",
  "allowed_models": "claude-3-haiku-20240307"
}
```

---

### Guardrails

#### `GET /admin/api/guardrails`

Lists all guardrails (built-in and custom) with their current status.

**Response:**

```json
[
  {
    "name": "pii-masking",
    "type": "pii",
    "enabled": true,
    "action": "block",
    "builtin": true
  },
  {
    "name": "no-profanity",
    "type": "content_filter",
    "enabled": true,
    "action": "block",
    "builtin": false,
    "block_patterns": ["badword1", "badword2"]
  }
]
```

---

#### `POST /admin/api/guardrails`

Creates a custom guardrail.

**Request body:**

```json
{
  "name": "no-profanity",
  "type": "content_filter",
  "action": "block",
  "block_patterns": ["pattern1", "pattern2"],
  "warn_patterns": ["pattern3"]
}
```

| Field | Values | Description |
|-------|--------|-------------|
| `type` | `content_filter`, `injection`, `pii` | Guardrail type |
| `action` | `block`, `log` | What to do when triggered |
| `block_patterns` | array of regex strings | Patterns that block the request |
| `warn_patterns` | array of regex strings | Patterns that log a warning but allow the request |

---

#### `PUT /admin/api/guardrails/{name}`

Updates an existing guardrail configuration.

---

#### `PUT /admin/api/guardrails/{name}/toggle`

Enables or disables a guardrail.

---

#### `DELETE /admin/api/guardrails/{name}`

Deletes a custom guardrail. Built-in guardrails cannot be deleted (only toggled).

---

#### `POST /admin/api/guardrails/test`

Tests a guardrail with sample input without making an LLM call.

**Request body:**

```json
{
  "guardrail_name": "no-profanity",
  "input": "This is a test message."
}
```

**Response:**

```json
{
  "triggered": false,
  "action": "none",
  "matched_patterns": []
}
```

---

#### `GET /admin/api/guardrail-logs`

Returns guardrail execution logs showing which requests were blocked, warned, or passed.

---

### Usage & Audit (Admin)

#### `GET /admin/api/usage`

Returns paginated usage logs across all keys and users.

**Query params:** `page`, `page_size`, `provider`, `model`, `key_id`

---

#### `GET /admin/api/usage/summary`

Returns aggregated usage statistics across all keys.

---

#### `GET /admin/api/audit`

Returns the audit log of admin actions (provider changes, key revocations, etc.).

**Query params:** `actor`, `action`, `resource_type`, `from`, `to`

---

### Metrics & Cooldowns

#### `GET /admin/api/metrics`

Returns gateway performance metrics (request counts, error rates, p50/p95/p99 latency, throughput) broken down by provider and model.

---

#### `GET /admin/api/cooldowns`

Lists providers currently in cooldown (temporarily skipped due to errors).

**Response:**

```json
[
  {
    "provider": "openai",
    "until": "2024-05-10T12:35:30Z",
    "reason": "429 rate limited"
  }
]
```

---

#### `DELETE /admin/api/cooldowns/{provider}`

Manually clears a provider's cooldown so it is used immediately on the next request.

---

## Error Responses

All errors follow a consistent JSON envelope:

```json
{
  "error": {
    "message": "API key not found or revoked",
    "type": "authentication_error",
    "code": 401
  }
}
```

| HTTP Status | Meaning |
|-------------|---------|
| `400` | Bad request — invalid input or blocked by a guardrail |
| `401` | Missing or invalid API key |
| `403` | Key or user lacks permission for the requested model/provider |
| `429` | Rate limit exceeded for your API key |
| `500` | Gateway error or all upstream providers failed |
| `502` | Upstream provider returned an unexpected response |
| `503` | No healthy providers available for the requested model |

---

## Rate Limiting

When rate limiting is enabled, the gateway returns standard rate limit headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1715367090
Retry-After: 15
```

Rate limits are applied per API key. The limit is set globally via the `RATE_LIMIT_RPM` environment variable.
