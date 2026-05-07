# API Reference

AgentX provides a RESTful API for managing assistants, templates, users, sharing, and system administration.

## Base URL

| Environment | Base URL |
|---|---|
| Development | `http://localhost:8000` |
| Production | `https://<hostname>/agentx` |

Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## Authentication

**Development (`local-admin` mode):** No credentials required. All requests run as the default admin user.

**Production (`oauth2-proxy` mode):** OAuth2 Proxy authenticates requests and injects headers:

```
X-Auth-Request-User: username
X-Auth-Request-Email: user@example.com
X-Auth-Request-Groups: group1,group2
X-Auth-Request-User-Namespace: user-namespace
```

Users are automatically created in the database on first access.

---

## Common Response Fields

Every `AssistantRead` response includes these computed fields in addition to database fields:

| Field | Type | Description |
|---|---|---|
| `url` | string | WebUI URL: `/agentx/<uuid>/webui/` |
| `tuis` | array of `TuiLink` | Browser links for each coding-agent terminal |

**`TuiLink` object:**
```json
{ "id": "claude", "label": "Claude Code", "url": "/agentx/<uuid>/claude/" }
```

**`tuis` array** (always returned, 7 entries):
```json
[
  { "id": "shell",    "label": "Terminal",     "url": "/agentx/<uuid>/shell/" },
  { "id": "claude",   "label": "Claude Code",  "url": "/agentx/<uuid>/claude/" },
  { "id": "opencode", "label": "OpenCode",     "url": "/agentx/<uuid>/opencode/" },
  { "id": "gemini",   "label": "Gemini CLI",   "url": "/agentx/<uuid>/gemini/" },
  { "id": "codex",    "label": "Codex CLI",    "url": "/agentx/<uuid>/codex/" },
  { "id": "copilot",  "label": "Copilot CLI",  "url": "/agentx/<uuid>/copilot/" },
  { "id": "vibe",     "label": "Mistral Vibe", "url": "/agentx/<uuid>/vibe/" }
]
```

**Assistant statuses:** `pending` | `starting` | `running` | `stopping` | `stopped` | `error`

> **Note:** `model_api_key` is filtered from all API responses — it is stored as a Kubernetes Secret and never returned.

---

## Assistants API

### Subscribe to Events

Subscribe to real-time assistant status events via Server-Sent Events. Subscribe once per session to receive all `assistant.*` events for the current user.

```
GET /api/assistants/events
```

**Response:** SSE stream

```
: connected

event: assistant.created
data: {"id": 1, "name": "my-assistant", "status": "starting", ...}

event: assistant.updated
data: {"id": 1, "status": "running", ...}

event: assistant.deleted
data: {"id": 1}
```

The watcher also pushes `assistant.updated` events to shared-assistant recipients so their cards stay in sync.

---

### Create Assistant

```
POST /api/assistants/
```

**Request body:**
```json
{
  "name": "my-assistant",
  "description": "My coding assistant",
  "configuration": {
    "model_provider": "securellm",
    "model": "claude-3-5-sonnet",
    "model_api_key": "sk-...",
    "model_base_url": "http://securellm.dkubex-apps/securellm/v1",
    "workspace_sources": [
      { "type": "git", "dir": "my-project", "url": "git@github.com:org/repo.git", "ref": "main" }
    ],
    "resources": {
      "cpu_request": "100m",
      "cpu_limit": "2000m",
      "memory_request": "256Mi",
      "memory_limit": "1Gi"
    }
  }
}
```

**Validation rules:**
- `model_provider` must be set if `model` is set (and vice versa)
- `model_provider` must be an enabled provider (currently `securellm`)
- `workspace_sources[].dir` must match `[a-z0-9][a-z0-9._-]{0,63}` (no slashes, no `..`)
- git sources require `url`; `ref` defaults to `main`
- The API key is validated against the provider before the pod is created

**Response:** `201 Created`
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "my-assistant",
  "description": "My coding assistant",
  "configuration": { "model_provider": "securellm", "model": "claude-3-5-sonnet", ... },
  "status": "starting",
  "owner_id": 1,
  "template_source_id": null,
  "token": "secure-token",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z",
  "url": "/agentx/550e8400-e29b-41d4-a716-446655440000/webui/",
  "tuis": [ ... ]
}
```

**Error responses:**
- `409` — assistant with this name already owned by the user
- `400` — invalid configuration (missing model, disabled provider, etc.)
- `502` — Kubernetes resource creation failed

---

### List Assistants

```
GET /api/assistants/
```

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 100 | Max records (max 100) |
| `include_metadata` | bool | false | Wrap response in pagination envelope |

**Response without metadata** (`include_metadata=false`): `200 OK`
```json
[ { "id": 1, "name": "my-assistant", "status": "running", ... } ]
```

**Response with metadata** (`include_metadata=true`): `200 OK`
```json
{
  "items": [ { "id": 1, ... } ],
  "total": 42,
  "page": 1,
  "page_size": 100,
  "total_pages": 1
}
```

---

### Get Assistant

```
GET /api/assistants/{assistant_id}
```

**Response:** `200 OK` — `AssistantRead` object

---

### Update Assistant

```
PUT /api/assistants/{assistant_id}
```

**Request body** (all fields optional):
```json
{
  "name": "new-name",
  "description": "Updated description",
  "configuration": { ... },
  "status": "stopped"
}
```

**Response:** `200 OK` — updated `AssistantRead`

Publishes an `assistant.updated` SSE event.

---

### Delete Assistant

```
DELETE /api/assistants/{assistant_id}
```

Deletes all Kubernetes resources (StatefulSet, Service, HTTPRoute, Secrets, ConfigMap) if the assistant is not already stopped, then removes the database record.

**Response:** `204 No Content`

Publishes an `assistant.deleted` SSE event.

---

### Start Assistant

Start a `stopped` assistant by recreating its Kubernetes resources.

```
POST /api/assistants/{assistant_id}/start
```

**Response:** `200 OK` — `AssistantRead` with `status: "starting"`

Status transitions to `running` once the pod readiness probe passes (detected by the StatefulSet watcher).

---

### Stop Assistant

Stop a `running` assistant by deleting its Kubernetes resources (workspace PVC is preserved).

```
POST /api/assistants/{assistant_id}/stop
```

**Response:** `200 OK` — `AssistantRead` with `status: "stopping"`

---

### Restart Assistant

Restart a `running` assistant (delete + recreate resources).

```
POST /api/assistants/{assistant_id}/restart
```

**Response:** `200 OK` — `AssistantRead` with `status: "starting"`

---

### Stream Logs

Stream live log lines from the assistant's pod.

```
GET /api/assistants/{assistant_id}/logs
```

**Response:** SSE stream (`text/event-stream`)
```
event: log
data: {"line": "Starting openclaw...", "timestamp": "..."}
```

The stream closes automatically after 5 minutes of inactivity. A legacy equivalent endpoint exists at `/temp/assistants/{assistant_id}/logs`.

---

### Publish as Template

Publish the assistant's configuration as a reusable template.

```
POST /api/assistants/{assistant_id}/publish
```

**Request body:**
```json
{
  "name": "My Template",
  "description": "Template description",
  "tags": ["claude", "python"],
  "version": "1.0.0",
  "template_metadata": { "author": "Jane" }
}
```

**Response:** `201 Created` — `TemplateRead` object

---

### Pin / Unpin

```
POST   /api/assistants/{assistant_id}/pin     → 201 { "pinned": true }
DELETE /api/assistants/{assistant_id}/pin     → 204
GET    /api/assistants/pinned                 → 200 [ AssistantRead, ... ]
```

Pins work for both owned and shared assistants (requires at least VIEW access).

---

## Sharing API

### Share Assistant

```
POST /api/assistants/{assistant_id}/shares
```

**Request body:**
```json
{
  "shares": [
    { "shared_with_user_id": 2, "permission": "use" },
    { "shared_with_user_id": 3, "permission": "manage" }
  ]
}
```

**Permission values:** `view` | `use` | `manage`

**Response:** `201 Created` — array of `AssistantShareRead`
```json
[
  {
    "id": 1,
    "assistant_id": 1,
    "shared_with_user_id": 2,
    "permission": "use",
    "shared_with_username": "user2",
    "created_at": "...",
    "updated_at": "..."
  }
]
```

---

### List Shares

```
GET /api/assistants/{assistant_id}/shares
```

**Response:** `200 OK` — array of shares for this assistant

---

### Update Share Permission

```
PUT /api/assistants/{assistant_id}/shares/{share_id}
```

**Request body:**
```json
{ "permission": "manage" }
```

**Response:** `200 OK` — updated share

---

### Revoke Share

```
DELETE /api/assistants/{assistant_id}/shares/{share_id}
```

**Response:** `204 No Content`

---

### List Shared with Me

```
GET /api/assistants/shared-with-me
```

**Response:** `200 OK` — array of `SharedAssistantRead`
```json
[
  {
    "id": 1,
    "name": "teammates-assistant",
    "status": "running",
    "share_id": 5,
    "permission": "use",
    "shared_by_owner_id": 3,
    "shared_by_owner_username": "teammate",
    "url": "/agentx/.../webui/",
    "tuis": [ ... ],
    ...
  }
]
```

---

## Providers API

### List Enabled Providers

```
GET /api/providers/
```

Returns the list of providers currently enabled in the system.

**Response:** `200 OK`
```json
[
  {
    "id": "securellm",
    "label": "DKubeX",
    "default_base_url": "http://securellm.dkubex-apps/securellm/v1",
    "requires_base_url": false,
    "requires_api_key": true
  }
]
```

---

### List Models

Fetch available models for a provider and validate the API key. Used by the Create-Assistant form to populate the model dropdown.

```
POST /api/providers/models
```

**Request body:**
```json
{
  "provider": "securellm",
  "api_key": "sk-...",
  "base_url": null
}
```

`base_url` is optional — omit to use the provider's default.

**Response:** `200 OK`
```json
{
  "models": [
    { "id": "claude-3-5-sonnet-20241022", "name": "claude-3-5-sonnet-20241022" },
    { "id": "claude-3-haiku-20240307",    "name": "claude-3-haiku-20240307" }
  ]
}
```

**Error responses:**
- `400` — unknown or disabled provider, missing required field
- `401` — invalid API key
- `502` — upstream provider returned an error
- `504` — could not reach the upstream endpoint

---

## Templates API

### List Templates

```
GET /api/templates/
```

**Query parameters:** `skip`, `limit`, `tags` (comma-separated), `q` (search)

**Response:** `200 OK` — array of `TemplateRead`

---

### Get Template

```
GET /api/templates/{template_id}
```

**Response:** `200 OK` — `TemplateRead`

---

### Deploy from Template

```
POST /api/templates/{template_id}/deploy
```

**Request body:**
```json
{
  "name": "my-new-assistant",
  "description": "Created from template",
  "version_id": null
}
```

`version_id` is optional — omit to use the latest version.

**Response:** `201 Created` — `AssistantRead`

---

### Create Template Version

```
POST /api/templates/{template_id}/versions
```

**Request body:**
```json
{
  "version": "1.1.0",
  "configuration": { ... },
  "changelog": "Added workspace source support"
}
```

**Response:** `201 Created`

---

### List Template Versions

```
GET /api/templates/{template_id}/versions
```

**Response:** `200 OK`

---

### Deprecate Template Version

```
POST /api/templates/{template_id}/versions/{version_id}/deprecate
```

**Request body:**
```json
{ "deprecation_message": "Use v2.0.0 instead" }
```

**Response:** `200 OK`

---

## Users API

### Get Current User

```
GET /api/v1/users/me
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "role": "user",
  "namespace": "user-alice",
  "group": "engineers",
  "created_at": "...",
  "updated_at": "...",
  "last_accessed_at": "..."
}
```

---

### Search Users

Search by username or email (used when sharing an assistant).

```
GET /api/v1/users/search?q=alice&limit=10
```

**Query parameters:** `q` (required), `limit` (default 10, max 50)

**Response:** `200 OK` — array of user summaries

---

### List All Users *(admin only)*

```
GET /api/v1/users/?skip=0&limit=100
```

**Response:** `200 OK`

---

### Get User *(admin only)*

```
GET /api/v1/users/{user_id}
```

---

### Create User *(admin only)*

```
POST /api/v1/users/
```

**Request body:**
```json
{
  "username": "bob",
  "email": "bob@example.com",
  "role": "user",
  "namespace": "user-bob"
}
```

---

### Update User *(admin only)*

```
PUT /api/v1/users/{user_id}
```

**Request body:** any subset of `username`, `email`, `role`, `namespace`, `group`

---

### Delete User *(admin only)*

```
DELETE /api/v1/users/{user_id}
```

**Response:** `200 OK`

---

## Admin API

All endpoints require the `admin` role.

### List All Assistants

```
GET /api/v1/admin/assistants
```

**Query parameters:** `skip`, `limit` (max 200), `status`, `owner_id`, `q`

**Response:** `200 OK` — array of `AdminAssistantRead` (includes `owner_username`)

---

### Stop Any Assistant

```
POST /api/v1/admin/assistants/{assistant_id}/stop
```

Action is recorded in the audit log.

**Response:** `200 OK` — `AdminAssistantRead`

---

### Delete Any Assistant

```
DELETE /api/v1/admin/assistants/{assistant_id}
```

Action is recorded in the audit log.

**Response:** `204 No Content`

---

### Get User's Assistants

```
GET /api/v1/admin/users/{user_id}/assistants
```

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "total": 3,
  "assistants": [
    { "id": 1, "name": "my-assistant", "status": "running" }
  ]
}
```

---

### Get Pod Metrics

```
GET /api/v1/admin/metrics/pods
```

**Response:** `200 OK`
```json
{
  "k8s_enabled": true,
  "pods": [
    {
      "assistant_id": 1,
      "assistant_name": "my-assistant",
      "pod_name": "assistant-my-assistant-1-0",
      "cpu_millicores": 250,
      "memory_mib": 512,
      "status": "Running"
    }
  ]
}
```

When `k8s_enabled` is `false` (local dev), `pods` is empty.

---

### Get System Health

```
GET /api/v1/admin/health
```

**Response:** `200 OK`
```json
{
  "counters": {
    "total_users": 10,
    "total_assistants": 25,
    "running_assistants": 15,
    "stopped_assistants": 8,
    "error_assistants": 2
  },
  "services": {
    "database":   { "status": "healthy" },
    "kubernetes": { "status": "enabled" },
    "api":        { "status": "healthy", "uptime_seconds": 86400 }
  }
}
```

---

### Get Audit Logs

```
GET /api/v1/admin/audit-logs
```

**Query parameters:** `skip`, `limit` (max 200), `action`, `q`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "timestamp": "2026-01-01T00:00:00Z",
    "admin_username": "admin",
    "action": "admin.assistant.stop",
    "resource_type": "assistant",
    "resource_id": "5",
    "details": { "name": "old-assistant", "owner_id": 2 }
  }
]
```

---

## Health Endpoints

```
GET /health        → { "status": "healthy" }
GET /users/me      → current user (same as /api/v1/users/me)
```

---

## Error Responses

| Status | When |
|---|---|
| `400` | Invalid request parameters or business rule violation |
| `401` | Not authenticated |
| `403` | Insufficient permissions |
| `404` | Resource not found |
| `409` | Conflict (duplicate name, already shared, etc.) |
| `422` | Validation error (request body schema violation) |
| `500` | Internal server error |
| `502` | Kubernetes operation failed |
| `504` | Could not reach upstream provider |

All error responses use the shape:
```json
{ "detail": "Human-readable error message" }
```

---

## Pagination

List endpoints accept `skip` (offset) and `limit` parameters. Use `include_metadata=true` on `GET /api/assistants/` to get the full pagination envelope.
