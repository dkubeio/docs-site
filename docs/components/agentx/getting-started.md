# Getting Started with AgentX

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Python | 3.12+ | Backend runtime |
| Node.js | 18+ | Frontend dev server |
| uv | latest | Python package manager (recommended) |
| Docker | any | Building container images |
| Kubernetes | 1.28+ | Production deployment only |
| kubectl + helm | any | Production deployment only |

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dkubeio/agentx.git
cd agentx
```

### 2. Install Dependencies

```bash
# Python backend
uv sync

# Node frontend
cd frontend && npm install
```

### 3. Configure Environment

Create `backend/.env`:

```env
# Database (SQLite for local dev)
DATABASE_URL=sqlite:///./agentx.db

# Auth mode: local-admin skips OAuth2, logs you in as a default admin
AUTHENTICATION_MODE=local-admin

# Security
SECRET_KEY=dev-secret-key-change-in-production
```

### 4. Initialize the Database

```bash
cd backend
uv run alembic upgrade head
```

### 5. Start Development Servers

**Option A — using Task (recommended):**
```bash
task dev
```

**Option B — manually:**
```bash
# Terminal 1: backend
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: frontend
cd frontend
npm run dev
```

### 6. Access the Application

| URL | Description |
|---|---|
| http://localhost:5173 | Web UI |
| http://localhost:8000/docs | Interactive API docs (Swagger UI) |
| http://localhost:8000/redoc | API docs (ReDoc) |
| http://localhost:8000/health | Health check |

In `local-admin` mode you are automatically signed in as an admin with username `default`.

---

## Creating Your First Assistant

1. Open the AgentX UI
2. Click **"Create Assistant"**
3. Fill in the form:
   - **Name** — unique name for this assistant (lowercase, hyphens allowed)
   - **Description** — what this assistant is for
   - **Provider / Model** — select DKubeX and enter your API key; pick a model from the dropdown
   - **Workspace source** *(optional)* — leave blank for an empty workspace, or provide a git repo URL to clone on startup
4. Click **"Create"**

The assistant moves through `starting` → `running` as Kubernetes provisions the pod. In development (no Kubernetes) the status stays `starting` unless a real cluster is reachable.

### Accessing the Assistant

Once `running`, click the assistant card to open it. You'll see tabs for:
- **OpenClaw** (`/agentx/<uuid>/webui/`) — the AI gateway web interface
- **Terminal** — plain bash in the workspace
- **Claude Code** — Anthropic Claude Code CLI
- **OpenCode** — OpenCode CLI
- **Gemini CLI**, **Codex CLI**, **Copilot CLI**, **Mistral Vibe** — additional coding agents

Each terminal tab lazy-starts its process on first click.

---

## Workspace Sources

When creating an assistant you can optionally configure a `workspace_sources` entry:

**Blank workspace** (default):
```json
{
  "workspace_sources": [
    { "type": "blank", "dir": "my-project", "git_init": true }
  ]
}
```

**Clone a git repository** (SSH):
```json
{
  "workspace_sources": [
    { "type": "git", "dir": "my-project", "url": "git@github.com:org/repo.git", "ref": "main" }
  ]
}
```

> **SSH key required** for git sources: configure a DKubeX SSH key in your account settings before creating the assistant.

---

## Kubernetes Deployment

### Using Helm

```bash
helm install agentx ./helm/agentx \
  --namespace dkubex-apps \
  --create-namespace \
  --set database.db_url=postgresql://user:password@postgres/agentx \
  --set hostname=your-domain.com
```

### Key Helm Values

```yaml
image:
  repository: ghcr.io/dkubeio/agentx
  tag: "latest"
  imagePullSecret: "dkubex-registry-secret"

database:
  db_url: postgresql://user:password@host/agentx

authentication:
  mode: ""   # auto-detected: oauth2-proxy in K8s, local-admin otherwise

hostname: ""   # your cluster hostname for HTTPRoute generation

resources:
  requests: { cpu: 250m, memory: 256Mi }
  limits:   { cpu: 500m, memory: 512Mi }
```

### Authentication in Kubernetes

AgentX integrates with OAuth2 Proxy. The proxy authenticates users and passes identity via HTTP headers:

| Header | Description |
|---|---|
| `X-Auth-Request-User` | Username |
| `X-Auth-Request-Email` | Email address |
| `X-Auth-Request-Groups` | Comma-separated group names |
| `X-Auth-Request-User-Namespace` | User's Kubernetes namespace |

Users are automatically provisioned in the database on first access. Group membership drives role assignment (`admins` group → admin role).

---

## Troubleshooting

**Database connection errors:**
```bash
# Check DATABASE_URL in backend/.env
# SQLite (dev): sqlite:///./agentx.db
# PostgreSQL: postgresql://user:pass@host/agentx
```

**Frontend can't reach backend:**
```bash
# Ensure backend is running on :8000
# Check vite.config.ts proxy settings
```

**Assistant stuck in `starting`:**
```bash
# Verify kubectl access and pod status
kubectl get pods -n dkubex-apps
kubectl logs -n dkubex-apps <pod-name>
```

**Invalid API key error on assistant creation:**
- The provider is validated before the pod is created; check that the DKubeX API key is correct and the base URL is reachable from the cluster.

---

## Next Steps

- [User Guide](./user-guide.md) — managing assistants, sharing, templates, admin features
- [API Reference](./api-reference.md) — full REST API documentation
- [Overview](./overview.md) — platform architecture and concepts
