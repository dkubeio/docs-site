# API Reference

AgentX provides a comprehensive RESTful API for managing AI assistants, templates, users, and system administration.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com/agentx`

## Authentication

All API requests require authentication via OAuth2 Proxy headers in production or use the default admin user in development mode.

### Headers (Production)

```
X-Auth-Request-User: username
X-Auth-Request-Email: user@example.com
X-Auth-Request-Groups: group1,group2
X-Auth-Request-User-Namespace: user-namespace
```

## Assistants API

### Create Assistant

Create a new AI assistant.

**Endpoint**: `POST /api/assistants`

**Request Body**:
```json
{
  "name": "my-assistant",
  "description": "My AI assistant",
  "configuration": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "my-assistant",
  "description": "My AI assistant",
  "configuration": {...},
  "status": "running",
  "owner_id": 1,
  "token": "secure-token-here",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Assistants

Get all assistants owned by the current user.

**Endpoint**: `GET /api/assistants`

**Query Parameters**:
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 100, max: 100): Maximum records to return
- `include_metadata` (bool, default: false): Include pagination metadata

**Response (without metadata)**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "my-assistant",
    "status": "running",
    ...
  }
]
```

**Response (with metadata)**: `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "name": "my-assistant",
      "status": "running",
      ...
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 100,
  "total_pages": 1
}
```

### Get Assistant

Get details of a specific assistant.

**Endpoint**: `GET /api/assistants/{assistant_id}`

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "my-assistant",
  "status": "running",
  ...
}
```

### Update Assistant

Update an existing assistant.

**Endpoint**: `PUT /api/assistants/{assistant_id}`

**Request Body**:
```json
{
  "name": "updated-name",
  "description": "Updated description",
  "configuration": {...}
}
```

**Response**: `200 OK`

### Delete Assistant

Delete an assistant and its resources.

**Endpoint**: `DELETE /api/assistants/{assistant_id}`

**Response**: `204 No Content`

### Start Assistant

Start a stopped assistant.

**Endpoint**: `POST /api/assistants/{assistant_id}/start`

**Response**: `200 OK`
```json
{
  "id": 1,
  "status": "running",
  ...
}
```

### Stop Assistant

Stop a running assistant.

**Endpoint**: `POST /api/assistants/{assistant_id}/stop`

**Response**: `200 OK`
```json
{
  "id": 1,
  "status": "stopped",
  ...
}
```

### Restart Assistant

Restart a running assistant.

**Endpoint**: `POST /api/assistants/{assistant_id}/restart`

**Response**: `200 OK`

### Stream Logs

Stream real-time logs from an assistant's pod.

**Endpoint**: `GET /api/assistants/{assistant_id}/logs`

**Response**: Server-Sent Events (SSE) stream
```
event: log
data: {"line": "Assistant started", "timestamp": "2024-01-15T10:30:00Z"}

event: log
data: {"line": "Processing request...", "timestamp": "2024-01-15T10:30:01Z"}
```

### Publish as Template

Publish an assistant's configuration as a reusable template.

**Endpoint**: `POST /api/assistants/{assistant_id}/publish`

**Request Body**:
```json
{
  "name": "My Template",
  "description": "Template description",
  "tags": ["ai", "gpt-4"],
  "version": "1.0.0",
  "template_metadata": {
    "author": "John Doe",
    "category": "AI"
  }
}
```

**Response**: `201 Created`

## Sharing API

### Share Assistant

Share an assistant with one or more users.

**Endpoint**: `POST /api/assistants/{assistant_id}/shares`

**Request Body**:
```json
{
  "shares": [
    {
      "shared_with_user_id": 2,
      "permission": "read"
    },
    {
      "shared_with_user_id": 3,
      "permission": "write"
    }
  ]
}
```

**Permissions**:
- `read`: View-only access
- `write`: Can modify the assistant

**Response**: `201 Created`
```json
[
  {
    "id": 1,
    "assistant_id": 1,
    "shared_with_user_id": 2,
    "permission": "read",
    "shared_with_username": "user2"
  }
]
```

### List Shares

List all sharing relationships for an assistant.

**Endpoint**: `GET /api/assistants/{assistant_id}/shares`

**Response**: `200 OK`

### Update Share Permission

Update the permission level of an existing share.

**Endpoint**: `PUT /api/assistants/{assistant_id}/shares/{share_id}`

**Request Body**:
```json
{
  "permission": "write"
}
```

**Response**: `200 OK`

### Revoke Share

Remove a sharing relationship.

**Endpoint**: `DELETE /api/assistants/{assistant_id}/shares/{share_id}`

**Response**: `204 No Content`

### List Shared with Me

Get all assistants shared with the current user.

**Endpoint**: `GET /api/assistants/shared-with-me`

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "shared-assistant",
    "share_id": 1,
    "permission": "read",
    "shared_by_owner_id": 2,
    "shared_by_owner_username": "owner"
  }
]
```

## Pin API

### Pin Assistant

Pin an assistant for quick access.

**Endpoint**: `POST /api/assistants/{assistant_id}/pin`

**Response**: `201 Created`
```json
{
  "pinned": true
}
```

### Unpin Assistant

Remove a pin from an assistant.

**Endpoint**: `DELETE /api/assistants/{assistant_id}/pin`

**Response**: `204 No Content`

### List Pinned Assistants

Get all assistants pinned by the current user.

**Endpoint**: `GET /api/assistants/pinned`

**Response**: `200 OK`

## Templates API

### List Templates

Get all available templates.

**Endpoint**: `GET /api/templates`

**Query Parameters**:
- `skip` (int): Pagination offset
- `limit` (int): Maximum records
- `tags` (string): Filter by tags (comma-separated)
- `q` (string): Search query

**Response**: `200 OK`

### Get Template

Get details of a specific template.

**Endpoint**: `GET /api/templates/{template_id}`

**Response**: `200 OK`

### Deploy from Template

Create a new assistant from a template.

**Endpoint**: `POST /api/templates/{template_id}/deploy`

**Request Body**:
```json
{
  "name": "my-new-assistant",
  "description": "Created from template",
  "version_id": null
}
```

**Response**: `201 Created`

### Create Template Version

Create a versioned snapshot of a template.

**Endpoint**: `POST /api/templates/{template_id}/versions`

**Request Body**:
```json
{
  "version": "1.1.0",
  "configuration": {...},
  "changelog": "Added new features"
}
```

**Response**: `201 Created`

### List Template Versions

Get all versions of a template.

**Endpoint**: `GET /api/templates/{template_id}/versions`

**Response**: `200 OK`

### Deprecate Template Version

Mark a template version as deprecated.

**Endpoint**: `POST /api/templates/{template_id}/versions/{version_id}/deprecate`

**Request Body**:
```json
{
  "deprecation_message": "Use version 2.0.0 instead"
}
```

**Response**: `200 OK`

## Users API

### Get Current User

Get information about the authenticated user.

**Endpoint**: `GET /api/v1/users/me`

**Response**: `200 OK`
```json
{
  "id": 1,
  "username": "john.doe",
  "email": "john@example.com",
  "role": "user",
  "namespace": "user-john-doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Search Users

Search for users by username or email.

**Endpoint**: `GET /api/v1/users/search`

**Query Parameters**:
- `q` (string, required): Search query
- `limit` (int, default: 10, max: 50): Maximum results

**Response**: `200 OK`
```json
[
  {
    "id": 2,
    "username": "jane.doe",
    "email": "jane@example.com"
  }
]
```

### List Users (Admin Only)

Get all users in the system.

**Endpoint**: `GET /api/v1/users`

**Query Parameters**:
- `skip` (int): Pagination offset
- `limit` (int): Maximum records

**Response**: `200 OK`

### Get User (Admin Only)

Get details of a specific user.

**Endpoint**: `GET /api/v1/users/{user_id}`

**Response**: `200 OK`

### Create User (Admin Only)

Create a new user.

**Endpoint**: `POST /api/v1/users`

**Request Body**:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "role": "user",
  "namespace": "user-newuser"
}
```

**Response**: `200 OK`

### Update User (Admin Only)

Update user information.

**Endpoint**: `PUT /api/v1/users/{user_id}`

**Request Body**:
```json
{
  "role": "admin"
}
```

**Response**: `200 OK`

### Delete User (Admin Only)

Delete a user.

**Endpoint**: `DELETE /api/v1/users/{user_id}`

**Response**: `200 OK`

## Admin API

### List All Assistants (Admin Only)

Get all assistants across all users.

**Endpoint**: `GET /api/v1/admin/assistants`

**Query Parameters**:
- `skip` (int): Pagination offset
- `limit` (int, max: 200): Maximum records
- `status` (string): Filter by status
- `owner_id` (int): Filter by owner
- `q` (string): Search query

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "assistant-1",
    "owner_id": 1,
    "owner_username": "john.doe",
    "status": "running"
  }
]
```

### Stop Assistant (Admin Only)

Stop any assistant regardless of owner.

**Endpoint**: `POST /api/v1/admin/assistants/{assistant_id}/stop`

**Response**: `200 OK`

### Delete Assistant (Admin Only)

Delete any assistant regardless of owner.

**Endpoint**: `DELETE /api/v1/admin/assistants/{assistant_id}`

**Response**: `204 No Content`

### Get User Assistants (Admin Only)

Get summary of assistants owned by a user.

**Endpoint**: `GET /api/v1/admin/users/{user_id}/assistants`

**Response**: `200 OK`
```json
{
  "user_id": 1,
  "total": 5,
  "assistants": [
    {"id": 1, "name": "assistant-1", "status": "running"}
  ]
}
```

### Get Pod Metrics (Admin Only)

Get CPU and memory metrics for all pods.

**Endpoint**: `GET /api/v1/admin/metrics/pods`

**Response**: `200 OK`
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

### Get System Health (Admin Only)

Get system health overview.

**Endpoint**: `GET /api/v1/admin/health`

**Response**: `200 OK`
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
    "database": {"status": "healthy"},
    "kubernetes": {"status": "enabled"},
    "api": {"status": "healthy", "uptime_seconds": 86400}
  }
}
```

### Get Audit Logs (Admin Only)

Get audit log entries.

**Endpoint**: `GET /api/v1/admin/audit-logs`

**Query Parameters**:
- `skip` (int): Pagination offset
- `limit` (int, max: 200): Maximum records
- `action` (string): Filter by action
- `q` (string): Search query

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T10:30:00Z",
    "admin_username": "admin",
    "action": "admin.assistant.stop",
    "resource_type": "assistant",
    "resource_id": "1",
    "details": {"name": "assistant-1", "owner_id": 2}
  }
]
```

## Events API

### Subscribe to Events

Subscribe to real-time assistant events via Server-Sent Events.

**Endpoint**: `GET /api/assistants/events`

**Response**: SSE stream
```
event: assistant.created
data: {"id": 1, "name": "new-assistant", ...}

event: assistant.updated
data: {"id": 1, "status": "running", ...}

event: assistant.deleted
data: {"id": 1}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Resource already exists"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

### 502 Bad Gateway
```json
{
  "detail": "Kubernetes operation failed"
}
```

## Rate Limiting

Currently, there are no rate limits enforced. This may change in future versions.

## Pagination

List endpoints support pagination via `skip` and `limit` query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (varies by endpoint)

## OpenAPI Documentation

Interactive API documentation is available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
