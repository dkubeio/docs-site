# Workspace

DKubeX Workspace is your personal, on-demand development environment in the cloud. Instead of setting up tools locally or sharing a shared server, you get an isolated workspace running in the cluster — with JupyterLab, VS Code, a terminal, and more pre-installed. Spin one up in seconds, share it with a teammate, and tear it down when you're done.

## Key features

- **On-demand and isolated** — Spin up a personal development environment running in the cluster in seconds, and tear it down when you are done.
- **Single sign-on** — Log in automatically with your organization's existing credentials; no separate account or password.
- **Choose your compute** — Pick a compute profile (CPU, RAM, GPU) when you create a workspace, and edit it later without losing your data.
- **Multiple apps side by side** — Run JupyterLab, Terminal, and FileBrowser in the same workspace over secure, authenticated routes.
- **Persistent storage** — Files under `/home/workspace` survive pod restarts and stops.
- **Lifecycle control** — Start, stop, restart, archive, restore, or delete workspaces from the actions menu.
- **Sharing** — Give teammates read-and-execute access to your workspace.

## Tutorials

- [Getting started](./getting-started.md) — Log in and create your first workspace.
- [Managing workspaces](./managing-workspaces.md) — Statuses and the full workspace lifecycle.
- [Using your workspace](./using-your-workspace.md) — Apps, files, and sharing.
- [Workflows](./tutorials.md) — End-to-end walkthroughs for common tasks.

## At a glance

| Action | How to do it |
|---|---|
| Create a workspace | Home → **New Workspace** |
| Start a workspace | Workspace card → **Start** |
| Stop a workspace | Actions menu (⋮) → **Stop** |
| Restart a workspace | Actions menu → **Restart** |
| Open an app | Workspace card → app link or **Add App** |
| Edit compute resources | Actions menu → **Edit** |
| View logs | Actions menu → **Logs** |
| Share with a teammate | Actions menu → **Share** |
| Archive (soft-delete) | Actions menu → **Archive** |
| Restore archived workspace | **Archived** tab → **Restore** |
| Permanently delete | Actions menu → **Delete** (irreversible) |

```{toctree}
:hidden:

getting-started
managing-workspaces
using-your-workspace
tutorials
```
