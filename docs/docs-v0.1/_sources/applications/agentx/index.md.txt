# AgentX

AgentX is an AI Assistant Management Platform for Kubernetes. It lets users create, manage, and share AI coding assistants — each running as an isolated Kubernetes StatefulSet with a browser-accessible workspace and multiple coding-agent terminals.

## Key Features

- **Multi-agent workspaces** — Each assistant includes Claude Code, OpenCode, Gemini CLI, Codex CLI, Copilot CLI, Mistral Vibe, and a plain shell terminal, all accessible in-browser.
- **Lazy activation** — Agent processes start on first browser interaction; idle pods consume minimal resources.
- **Workspace sources** — Clone a git repo or start blank on assistant creation; workspace persists on a PVC across restarts.
- **Sharing & collaboration** — Share assistants with fine-grained permissions (VIEW / USE / MANAGE).
- **Templates** — Publish assistant configurations as versioned, reusable templates.
- **Pin favorites** — Quick-access pinned assistants across sessions.
- **Real-time status** — Server-Sent Events keep every browser tab in sync with pod state.
- **Admin dashboard** — User management, system health, pod metrics, and audit logs.
- **Kubernetes-native** — StatefulSets, Gateway API HTTPRoutes, PVCs; managed via Helm.

## Tutorials

- [Overview](./overview.md) — Platform overview, features, architecture, and use cases.
- [Getting Started](./getting-started.md) — Installation, configuration, and creating your first assistant.
- [User Guide](./user-guide.md) — Managing assistants, sharing, templates, and admin features.

```{toctree}
:hidden:

overview
getting-started
user-guide
```
