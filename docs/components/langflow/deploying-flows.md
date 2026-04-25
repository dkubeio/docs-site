# Deploying Flows

Langflow on DKubeX separates authoring from serving using two modes, switchable from the header:

- **Development Mode** — The full canvas for editing and testing.
- **Deployment Mode** — A simplified form to promote a flow to a served endpoint.

## Deploying from the Canvas

1. Open the flow you want to deploy.
2. Click the red **Deploy** button in the header (visible in Development Mode on a flow page).
3. The project and workflow are pre-selected. Review and click **Deploy**.
4. Confirm in the modal to start the deployment.

## Deploying from Deployment Mode

1. Click **Deployment Mode** in the header tab slider.
2. Choose a **Project** from the dropdown.
3. Choose a **Workflow** within that project.
4. Click **Deploy** and confirm.

## After Deployment

- The flow is exposed as an HTTP endpoint managed by DKubeX.
- Monitor logs, metrics, and request history from the DKubeX deployment dashboard.
- See [API Usage](./api-usage.md) for how to call the endpoint.
