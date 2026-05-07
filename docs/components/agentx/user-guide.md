# User Guide

## Managing Assistants

### Creating an Assistant

1. Click **"Create Assistant"** in the top-right of the My Assistants tab
2. Fill in:
   - **Name** — unique per user, lowercase, hyphens allowed (e.g. `my-project`)
   - **Description** *(optional)* — free-form text
   - **Provider** — select DKubeX; enter your API key; choose a model from the dropdown (the dropdown validates the key live)
   - **Workspace source** *(optional)* — blank project or git clone (see below)
3. Click **"Create"**

The assistant card immediately shows `starting`; status updates in real time via Server-Sent Events and transitions to `running` once the pod's readiness probe passes.

### Workspace Sources

Set the workspace source when creating an assistant to control what lives in `/home/<user>/<dir>/`:

**Blank project:**
```json
{
  "workspace_sources": [
    { "type": "blank", "dir": "my-project", "git_init": true }
  ]
}
```
- `git_init: true` runs `git init` in the directory after creation.

**Clone from git (SSH):**
```json
{
  "workspace_sources": [
    { "type": "git", "dir": "my-project", "url": "git@github.com:org/repo.git", "ref": "main" }
  ]
}
```
- Requires a DKubeX SSH key configured in your account settings.
- `ref` defaults to `main` if omitted.

### Assistant Configuration

The `configuration` JSON object accepts:

| Field | Type | Default | Description |
|---|---|---|---|
| `model_provider` | string | — | Provider ID (e.g. `securellm`) |
| `model` | string | — | Model ID selected from the provider's list |
| `model_api_key` | string | — | API key (stored as a Kubernetes Secret; never returned in API responses) |
| `model_base_url` | string | provider default | Override the provider's base URL |
| `workspace_sources` | array | `[]` | Workspace initialization entries |
| `resources.cpu_request` | string | `100m` | Pod CPU request |
| `resources.cpu_limit` | string | `2000m` | Pod CPU limit |
| `resources.memory_request` | string | `256Mi` | Pod memory request |
| `resources.memory_limit` | string | `1Gi` | Pod memory limit |

### Assistant Lifecycle

| Action | From status | Result |
|---|---|---|
| **Start** | `stopped` | Creates Kubernetes resources; status → `starting` → `running` |
| **Stop** | `running` | Deletes Kubernetes resources; status → `stopping` → `stopped` |
| **Restart** | `running` | Deletes then recreates resources; status → `starting` → `running` |
| **Delete** | any | Deletes all Kubernetes resources and the database record |

> The workspace PVC is **not** deleted when an assistant is stopped — data persists. The PVC is removed only when the assistant is deleted.

### Coding-Agent Terminals

Once an assistant is `running`, click its card to open it. The toolbar shows links for each agent TUI:

| Tab | Path | Description |
|---|---|---|
| OpenClaw | `/agentx/<uuid>/webui/` | AI gateway web interface |
| Terminal | `/agentx/<uuid>/shell/` | Plain bash shell |
| Claude Code | `/agentx/<uuid>/claude/` | Anthropic Claude Code CLI |
| OpenCode | `/agentx/<uuid>/opencode/` | anomalyco/opencode CLI |
| Gemini CLI | `/agentx/<uuid>/gemini/` | Google Gemini CLI |
| Codex CLI | `/agentx/<uuid>/codex/` | OpenAI Codex CLI |
| Copilot CLI | `/agentx/<uuid>/copilot/` | GitHub Copilot CLI |
| Mistral Vibe | `/agentx/<uuid>/vibe/` | Mistral Vibe coding agent |

Each terminal is **lazily activated** — the process starts on your first click. If you close the browser tab, the session keeps running and reconnects when you return.

### Viewing Logs

1. Open an assistant card
2. Click **"View Logs"**
3. Live log lines stream from the pod via SSE
4. Stream automatically closes after 5 minutes of inactivity or when you close the panel

### Pinning Assistants

Click the pin icon on any assistant card (owned or shared) to add it to your pinned section at the top of the list. Pins persist across sessions and are personal to your account.

---

## Sharing Assistants

### Share with Users

1. Open an assistant card → click **"Share"**
2. Search by username or email
3. Select the permission level:

| Permission | What the recipient can do |
|---|---|
| **VIEW** | See assistant details and metadata |
| **USE** | Open terminals, view logs, interact with the assistant |
| **MANAGE** | Edit configuration, restart, start/stop, modify settings |

4. Click **"Share"**

The recipient sees the assistant immediately in their **"Shared with Me"** tab.

### Managing Shares

- **Update permission**: open the Shares panel on an assistant → click "Edit" next to a share → change level → Save
- **Revoke**: click "Remove" next to a share → confirm

### Accessing Shared Assistants

Navigate to the **"Shared with Me"** tab to see all assistants shared with you. The permission level is shown on each card and determines which actions are available.

**Shared assistant limitations:**
- Only the **owner** can delete, share with others, or publish as a template
- The owner retains full control regardless of what permission was granted to others

---

## Templates

Templates are saved assistant configurations that can be shared and redeployed.

### Publishing a Template

1. Open a working assistant → click **"Publish as Template"**
2. Provide:
   - **Name** — template name (unique)
   - **Description**
   - **Tags** — comma-separated, for filtering (e.g. `python,claude`)
   - **Version** — semantic version (e.g. `1.0.0`)
   - **Metadata** *(optional)* — JSON object with arbitrary extra info
3. Click **"Publish"**

### Deploying from a Template

1. Browse the Templates tab
2. Click **"Deploy"** on a template
3. Provide a unique assistant name
4. Click **"Create"**

### Template Versions

- Each published template can have multiple versions
- Versions can be marked as deprecated with a message
- When deploying, the latest non-deprecated version is used by default

---

## Admin Features

The **"Admin"** tab is visible only to users with the `admin` role.

### System Health

Displays:
- Total users, total assistants, running/stopped/error counts
- Database health status
- Kubernetes status (enabled / disabled)
- API uptime

### User Management

| Action | Steps |
|---|---|
| List users | Admin → Users tab |
| View user | Click a user row |
| View user's assistants | Admin → `GET /api/v1/admin/users/{id}/assistants` |
| Update role | Click user → Edit → change role → Save |
| Delete user | Click user → Delete → confirm |

Role changes are written to the audit log.

### Assistant Management

Admins can see, stop, and delete **any** assistant regardless of owner:

- **List**: Admin → Assistants tab; filter by status, owner, or search by name
- **Stop**: click Stop on any running assistant; action is logged
- **Delete**: click Delete; action is logged

### Pod Metrics

Admin → Metrics shows CPU (millicores) and memory (MiB) for every pod labeled `app=agentx`, mapped to their assistant name.

### Audit Logs

Admin → Audit Logs shows all recorded admin actions (newest first). Filter by action type or search by resource ID / username.

Current logged actions:
- `admin.assistant.stop`
- `admin.assistant.delete`

---

## Best Practices

### Naming

- Use lowercase with hyphens: `code-reviewer`, `data-pipeline`
- Be project-specific: `my-project-dev`, `my-project-prod`

### Resource Management

- **Stop** assistants when not actively used — the workspace PVC is preserved
- Monitor resource usage via the Admin metrics panel
- Set appropriate CPU/memory limits to avoid cluster resource starvation

### Security

- Never put raw secrets in the `configuration` JSON beyond `model_api_key` (which is stored as a Kubernetes Secret and filtered from API responses)
- Use the SSH key feature for git workspace sources rather than embedding credentials

### Sharing Strategy

- Grant **VIEW** to reviewers who just need to see the setup
- Grant **USE** to teammates who will interact with the assistant
- Grant **MANAGE** only when the recipient needs to modify configuration

---

## Troubleshooting

### Assistant stuck in `starting`

- Check the pod's events: `kubectl describe pod <name> -n <namespace>`
- Check logs: `kubectl logs <pod> -n <namespace>`
- Common causes: invalid API key (validated pre-flight but may fail at runtime), SSH key missing for git source, insufficient cluster resources

### Cannot share with a user

- Verify the username/email exists in AgentX (users are provisioned on first login)
- Check if already shared (re-sharing the same user raises a conflict)

### Agent terminal shows blank or error

- The agent process lazy-starts; wait a few seconds on first open
- If status is `error`, the startup self-test failed — check pod logs for the specific agent that failed

### Logs not streaming

- Confirm the assistant status is `running`
- Refresh the page
- Streams close after 5 minutes of inactivity; reopen via the Logs button

### Template deployment fails

- Check that the template's `model_api_key` is still valid (keys are stored in the template configuration)
- Ensure the workspace source (if any) is still accessible
- Check for naming conflicts with existing assistants
