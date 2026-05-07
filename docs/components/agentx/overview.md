# AgentX Overview

AgentX is an AI Assistant Management Platform for Kubernetes. It provides a web UI and REST API for creating, running, sharing, and administering AI coding assistants — each deployed as an isolated Kubernetes pod with a persistent workspace.

## What is an Assistant?

An assistant is a Kubernetes StatefulSet pod that contains:

- A **persistent workspace** (PVC) pre-populated from a git repo or blank
- **Seven in-browser coding-agent terminals**: Claude Code, OpenCode, Gemini CLI, Codex CLI, GitHub Copilot CLI, Mistral Vibe, and a plain shell
- An **OpenClaw gateway** serving the assistant's web UI
- All processes managed by **Supervisor**, started lazily on first browser interaction

Users access their assistant through a unique URL (`/agentx/<uuid>/`) and interact with agents entirely in the browser — no local CLI setup required.

## Key Features

### Assistant Management
- **Create & deploy** — launch assistants from scratch or from a template in one click
- **Workspace sources** — optionally clone a git repo (SSH) into the workspace at creation time, or start blank
- **Lifecycle control** — start, stop, restart, and delete assistants; status reflected in real time
- **Real-time logs** — stream pod logs directly in the UI via Server-Sent Events

### Coding-Agent TUIs
Each assistant pod exposes seven browser-accessible terminals:

| ID | Label | Description |
|---|---|---|
| `shell` | Terminal | Plain bash shell in the workspace |
| `claude` | Claude Code | Anthropic Claude Code CLI |
| `opencode` | OpenCode | anomalyco/opencode CLI |
| `gemini` | Gemini CLI | Google Gemini CLI |
| `codex` | Codex CLI | OpenAI Codex CLI |
| `copilot` | Copilot CLI | GitHub Copilot CLI |
| `vibe` | Mistral Vibe | Mistral Vibe coding agent |

Terminals are **lazily activated** — a process starts only when the user first opens that terminal tab.

### Collaboration
- **Share assistants** with other users; three permission levels: VIEW, USE, MANAGE
- **Pin favorites** for quick access across sessions
- **Shared with Me** tab shows all assistants shared with you

### Templates
- **Publish** any assistant's configuration as a reusable template
- **Version control** — create and deprecate template versions
- **One-click deploy** — create a new assistant from a template

### Administration
- **User management** — create, update, and delete users; assign admin roles
- **System monitoring** — health overview, pod CPU/memory metrics
- **Audit log** — record of all admin actions

## How It Works

```
1. Create Assistant  →  2. Workspace Set Up  →  3. Use in Browser  →  4. Share & Collaborate
```

1. **Create** — submit a name, description, provider/model, and optional workspace source (blank or git repo)
2. **Deploy** — AgentX renders Kubernetes manifests and applies them; the pod reaches `running` status once the readiness probe passes
3. **Use** — open the assistant URL; agent terminals lazy-start on first interaction; workspace persists across pod restarts
4. **Share** — share with teammates at VIEW / USE / MANAGE permission; they see it in "Shared with Me"

## Technology Stack

- **Frontend**: React 18 + TypeScript, TanStack Query, Tailwind CSS, Vite
- **Backend**: FastAPI (Python 3.12+), SQLModel, PostgreSQL (production) / SQLite (development)
- **Assistant runtime**: Node.js 24, Jupyter terminal servers (terminado), OpenClaw gateway, Supervisor
- **Orchestration**: Kubernetes StatefulSets, Gateway API HTTPRoutes, Helm
- **Authentication**: OAuth2 Proxy (Kubernetes) / local-admin (development)
- **Model provider**: DKubeX (SecureLLM gateway)

## Use Cases

### Development Teams
- Shared, persistent coding environments for every project
- Standardize tooling with templates
- Pair-program by sharing an assistant

### AI/ML Projects
- Deploy multiple assistants for different experiments
- Version and share configurations via templates
- Use multiple coding agents side-by-side in the same workspace

### Enterprise
- Centralized assistant lifecycle management
- Role-based access control and audit trail
- Resource usage monitoring per user

## Quick Links

- [Getting Started](./getting-started.md) — installation and first assistant
- [User Guide](./user-guide.md) — full feature walkthrough
- [API Reference](./api-reference.md) — REST API documentation
