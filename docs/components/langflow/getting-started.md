# Getting Started

Langflow is a visual workflow builder for AI-powered agents and pipelines. On DKubeX, it comes pre-configured with platform authentication, a built-in deployment system, and DKubeX-native LLM and embedding components backed by **SecureLLM**.

## Prerequisites

- Access to a DKubeX environment with Langflow enabled.
- A modern browser (Chrome, Firefox, Safari, or Edge).

## Launching Langflow

1. Navigate to `https://<your-platform>/langflow/` or click the **Langflow** tile in your DKubeX dashboard.
2. You are automatically logged in via DKubeX SSO — no separate Langflow credentials needed.
3. The Langflow canvas loads with the DKubeX header pinned to the top.

## The DKubeX Header

The header at the top of every page provides:
- **DKubeX logo** — links back to the platform dashboard.
- **Development / Deployment tab switcher** — switch between authoring flows and managing deployed endpoints.
- **Theme toggle** — Light, Dark, or System (in the profile dropdown).
- **Flow breadcrumb** — shown when editing a flow, displays the folder and flow name with an edit shortcut.

## Creating Your First Flow

1. Click **New Flow** from the projects list.
2. Drag components from the left sidebar onto the canvas.
3. Connect component outputs to inputs by dragging between the colored ports.
4. Click the **Play** button on any component to run the flow up to that point, or click **Run** at the top of the canvas to execute the whole flow.

## Using DKubeX LLM and Embedding Components

DKubeX includes built-in components that connect to the cluster-local **SecureLLM** service:

1. In the left sidebar, open the **DKubeX Providers** category.
2. Drop **DKubeX LLM** or **DKubeX Embeddings** onto the canvas.
3. Enter your **SecureLLM API Key** in the component's side panel.
4. Click the refresh icon next to **Model Name** to load available models.
5. Select a model and wire the component into your flow.

> Contact your cluster administrator if you don't have a SecureLLM API key.

## Next Steps

- Learn [canvas basics and flow authoring](./building-flows.md).
- Browse the full [component catalog](./components.md).
- When ready, [deploy your flow](./deploying-flows.md) as a standalone API endpoint.
- See [API Usage](./api-usage.md) to call flows programmatically.
