# Workspace

DKubeX Workspace is your personal, on-demand development environment in the cluster. Install it once from the App Store and you get an isolated environment with JupyterLab, VS Code, a terminal, a file browser, and a set of pre-configured AI coding agents.

## Key features

- **One-click install** — Install your workspace from the App Store; no configuration wizard and nothing to size up front.
- **Single sign-on** — Log in with your organization's existing credentials; no separate account or password.
- **Twelve apps, ready to use** — JupyterLab, VS Code, Terminal and FileBrowser, plus eight AI coding agents.
- **Two ways to configure models** — Point every coding agent at the platform's own models by choosing a default model in workspace settings, or leave the default model set to none and sign in to the agents with your own subscriptions.
- **Apps start on demand** — An app starts the first time you open it, so an idle workspace uses almost nothing.
- **Persistent home directory** — Everything in your home directory survives restarts, and survives uninstalling and reinstalling.
- **SSH access** — Connect from your own terminal or IDE with your own SSH key.
- **Reach your own services** — Start a dev server on any port and open it through your workspace URL.

## Guides

- [Getting started](./getting-started.md) — Log in and install your workspace.
- [Managing your workspace](./managing-workspaces.md) — Statuses, what persists, and uninstalling.
- [Using your workspace](./using-your-workspace.md) — Apps, files, ports, and SSH.
- [Working with AI agents](./working-with-agents.md) — The coding agents and how to choose a model.
- [Workflows](./tutorials.md) — End-to-end walkthroughs for common tasks.

## At a glance

| Action | How to do it |
|---|---|
| Install your workspace | **App Store** → **Workspace** → **Install** |
| Open an app | **Apps** → click the app's tile |
| Choose your default model | **Settings** → **Workspace** → **Default model** |
| Set environment variables | **Settings** → **Workspace** → **Environment variables** |
| Connect over SSH | **Settings** → **SSH access** |
| Remove your workspace | **App Store** → **Workspace** → **Uninstall** |
| Start or stop the pod | Ask your administrator — these are admin-only actions |

> **Note:** You have one workspace. There is no workspace creation wizard, no compute-profile picker, and no workspace sharing — your administrator sets the CPU, memory and GPU defaults for everyone.

```{toctree}
:hidden:

getting-started
managing-workspaces
using-your-workspace
working-with-agents
tutorials
```
