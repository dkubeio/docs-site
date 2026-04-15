# Configuration

SecureLLM is configured entirely through environment variables. There are no config files required.

---

## Server

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8081` | Port the HTTP server listens on |
| `BASE_PATH` | _(empty)_ | URL path prefix, e.g. `/securellm`. Useful when running behind a reverse proxy at a sub-path |
| `READ_TIMEOUT_SEC` | `30` | HTTP read timeout in seconds |
| `WRITE_TIMEOUT_SEC` | `60` | HTTP write timeout in seconds |
| `IDLE_TIMEOUT_SEC` | `120` | HTTP keep-alive (idle) timeout in seconds |
| `LOG_LEVEL` | `info` | Log verbosity: `debug`, `info`, `warn`, `error` |
| `LOG_FORMAT` | `json` | Log format: `json` or `text` |

---

## Database

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_DRIVER` | `sqlite3` | Database driver: `sqlite3` or `postgres` |
| `DB_DSN` | `./securellm.db` | SQLite file path **or** PostgreSQL connection string (e.g. `postgres://user:pass@host:5432/db?sslmode=disable`) |

Database migrations run automatically on startup. No manual migration steps are needed.

---

## Authentication & Admin

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_USERS` | _(empty)_ | Comma-separated list of SSO usernames that have admin access, e.g. `alice@example.com,bob@example.com` |
| `DEV_MODE` | `false` | Set to `true` to enable a local dev login page at `/admin/login`. **Do not enable in production.** In production, use an SSO proxy that injects `X-Forwarded-User` |

---

## LLM Providers

Configure one or more providers. Any provider whose required variables are set will be automatically registered on first boot.

### OpenAI

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | _(required)_ | Your OpenAI API key |
| `OPENAI_BASE_URL` | _(empty)_ | Override the OpenAI base URL. Useful for Azure OpenAI or proxy setups |

### Anthropic

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | _(required)_ | Your Anthropic API key |
| `ANTHROPIC_BASE_URL` | _(empty)_ | Override the Anthropic base URL |

### Custom (OpenAI-compatible)

Use this to connect Ollama, vLLM, LM Studio, or any other OpenAI-compatible endpoint.

| Variable | Default | Description |
|----------|---------|-------------|
| `CUSTOM_PROVIDER_NAME` | _(required)_ | A unique name for this provider, e.g. `ollama` |
| `CUSTOM_PROVIDER_BASE_URL` | _(required)_ | Base URL of the custom endpoint, e.g. `http://localhost:11434/v1` |
| `CUSTOM_PROVIDER_API_KEY` | _(empty)_ | Optional API key for the custom endpoint |

Additional custom providers can be added at any time through the admin UI (**Providers** page) without restarting.

### OpenAI Compatible

Use this type for any named service that speaks the OpenAI API format — Azure OpenAI, LiteLLM proxies, Anyscale, Together AI, or similar hosted endpoints.

Unlike **Custom / local** (designed for Ollama, vLLM, LM Studio on private networks), **OpenAI Compatible** is for reachable named services that implement the OpenAI API.

| Field | Requirement | Notes |
|-------|-------------|-------|
| Name | Required | Unique identifier, e.g. `azure-openai`, `litellm-proxy` |
| Base URL | Required | Endpoint root, e.g. `https://my-resource.openai.azure.com` |
| API Key | Optional | Leave blank if the endpoint does not require authentication |

Providers of this type are added through the admin UI (**Providers** page). There is no environment variable equivalent.

---

## Routing

| Variable | Default | Description |
|----------|---------|-------------|
| `ROUTING_STRATEGY` | `simple-shuffle` | How to select a provider when multiple are available. Options: `simple-shuffle`, `weighted-random`, `weighted-fallback`, `usage-based`, `latency-based` |
| `ROUTING_WEIGHTS` | `{}` | JSON object of provider weights for weighted strategies, e.g. `{"openai": 3, "anthropic": 1}` (75% OpenAI, 25% Anthropic) |
| `ROUTING_LATENCY_BUFFER_MS` | `0` | Buffer in milliseconds for `latency-based` routing — a provider is preferred only if it is this many ms faster than the alternatives |
| `NUM_RETRIES` | `2` | Number of fallback attempts before returning an error |
| `FALLBACKS` | `{}` | Explicit per-model fallback chains as JSON, e.g. `{"gpt-4": ["claude-3-5-sonnet-20241022"]}` |
| `COOLDOWN_TIME_SEC` | `30` | Seconds to put a provider in cooldown after a `429` or `404` error |
| `DISABLE_COOLDOWNS` | `false` | Set to `true` to disable automatic provider cooldowns |

**Routing strategies explained:**

| Strategy | Behavior |
|----------|----------|
| `simple-shuffle` | Randomly selects among available providers for the model |
| `weighted-random` | Probability-based selection using `ROUTING_WEIGHTS` |
| `weighted-fallback` | Like `weighted-random` but falls back to other providers on failure |
| `usage-based` | Prefers the provider with the lowest cumulative token usage |
| `latency-based` | Prefers the provider with the lowest observed response time |

---

## Rate Limiting

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_ENABLED` | `false` | Enable per-key request rate limiting |
| `RATE_LIMIT_RPM` | `60` | Maximum requests per minute per API key |

---

## Guardrails

### PII Masking (requires Microsoft Presidio)

| Variable | Default | Description |
|----------|---------|-------------|
| `PRESIDIO_ENABLED` | `false` | Enable PII detection and masking via Presidio |
| `PRESIDIO_ANALYZER_URL` | `http://localhost:5001` | URL of the Presidio Analyzer service |
| `PRESIDIO_ANONYMIZER_URL` | `http://localhost:5002` | URL of the Presidio Anonymizer service |

### Prompt Injection Detection

| Variable | Default | Description |
|----------|---------|-------------|
| `PROMPT_INJECTION_ENABLED` | `true` | Enable prompt injection detection |
| `PROMPT_INJECTION_ACTION` | `block` | What to do when injection is detected: `block` (return 400) or `log` (allow but record) |
| `PROMPT_INJECTION_THRESHOLD` | `0.7` | Detection confidence threshold (0.0–1.0). Lower values are more sensitive |

### Content Filtering

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTENT_FILTER_ENABLED` | `true` | Enable content filtering |
| `CONTENT_FILTER_ACTION` | `block` | What to do when a pattern matches: `block` or `log` |
| `CONTENT_FILTER_BLOCK_PATTERNS` | _(empty)_ | Comma-separated list of regex patterns to block |
| `CONTENT_FILTER_WARN_PATTERNS` | _(empty)_ | Comma-separated list of regex patterns to warn on (request is allowed) |
| `CONTENT_FILTER_BUILTIN_PII` | `true` | Enable built-in PII regex patterns (email addresses, phone numbers, SSNs, etc.) |

---

## Example `.env` File

```bash
# Server
PORT=8081
LOG_LEVEL=info
LOG_FORMAT=json

# Admin
ADMIN_USERS=alice@example.com,bob@example.com

# Database (SQLite for dev, Postgres for prod)
DB_DRIVER=sqlite3
DB_DSN=./securellm.db
# DB_DRIVER=postgres
# DB_DSN=postgres://securellm:secret@db:5432/securellm?sslmode=disable

# Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Custom provider (e.g. Ollama)
# CUSTOM_PROVIDER_NAME=ollama
# CUSTOM_PROVIDER_BASE_URL=http://ollama:11434/v1

# Routing
ROUTING_STRATEGY=weighted-random
ROUTING_WEIGHTS={"openai": 3, "anthropic": 1}
NUM_RETRIES=2

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_RPM=120

# Guardrails
PROMPT_INJECTION_ENABLED=true
PROMPT_INJECTION_ACTION=block
CONTENT_FILTER_ENABLED=true
CONTENT_FILTER_BUILTIN_PII=true
```

---

## Production Deployment Notes

- **SSO:** In production, deploy SecureLLM behind an SSO proxy (oauth2-proxy, Authelia, Authentik, etc.) configured to inject `X-Forwarded-User` on every request. Never set `DEV_MODE=true` in production.
- **Database:** Use PostgreSQL for multi-instance or production deployments. SQLite works well for single-node setups.
- **TLS:** Terminate TLS at your reverse proxy or load balancer, not at SecureLLM itself.
- **Secrets:** Avoid passing `API_KEY` values directly in shell history. Use a secrets manager or a `.env` file with restricted permissions (`chmod 600`).
