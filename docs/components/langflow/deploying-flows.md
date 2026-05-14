# Deploying Flows

Langflow on DKubeX lets you promote any flow from the canvas into a standalone, always-on API endpoint running in the cluster. Each deployment gets its own Kubernetes pod, internal DNS name, and cURL command you can use to call it.

## How It Works

When you deploy a flow:
- DKubeX creates a dedicated Kubernetes `Deployment`, `Service`, `ConfigMap`, and `Secret` in the cluster.
- The flow JSON is baked into the pod via the ConfigMap.
- Any Langflow [Global Variables](./building-flows.md#variables-and-secrets) referenced by the flow are resolved and injected as environment variables in the pod's Secret.
- The deployment runs the same Langflow image as the main instance.

## Deploying a Flow

### Method 1 — From the Flow Canvas (quickest)

1. Open the flow you want to deploy in **Development Mode**.
2. Right-click the flow in the flows list (or use the three-dots **⋯** menu next to the flow name).
3. Click **Deploy**.
4. In the **Deploy Workflow** modal, enter:
   - **Name** — 4–30 characters, letters, numbers and spaces only. This becomes the deployment's identifier.
   - **Description** (optional) — up to 500 characters.
5. Click **Deploy**. The modal closes and you are switched to **Deployment Mode** where the new deployment appears in the table.

### Method 2 — From Deployment Mode

1. Click **Deployment** in the header tab switcher.
2. You will see the Deployments table. Previously deployed flows are listed here.
3. To deploy a new flow, use Method 1 from the canvas — there is no separate "new deployment" button in the table view.

## The Deployments Table

The **Deployment Mode** view shows a live table of all your deployments, polling for status every 5 seconds.

| Column | Description |
|--------|-------------|
| Name | Display name given at deploy time |
| Created At | Timestamp in your local timezone |
| Status | Current state (see below) |
| Actions | Three-dots menu: Logs, Edit Resources, Remove |

### Deployment Status

| Status | Meaning |
|--------|---------|
| **Deploying** | Pod is starting up. Usually resolves within 1–2 minutes. |
| **Deployed** | Pod is running and ready to accept requests. |
| **Failed** | Pod failed to start (image pull error, crash, or not ready after 5 minutes). Check logs. |
| **Removing** | Deletion in progress. The row disappears once Kubernetes finishes cleanup. |

## Viewing Deployment Details

Click any row (when not in Removing state) to open the **Detail panel**:

- **Description tab** — View or edit the deployment description.
- **cURL tab** — Shows the cluster-internal cURL command to call this deployment. Only available when status is `Deployed`.

> **Note:** The cURL endpoint is a cluster-internal address (`*.dkubex-apps.svc.cluster.local`). It is accessible from within the cluster but not directly from a browser or external client. For external access, contact your cluster administrator.

## Deployment Logs

Click **⋯ → Logs** on any deployment row to view the last 500 lines of the pod's logs. Useful for diagnosing `Failed` deployments.

## Editing Resources and Environment Variables

Click **⋯ → Edit Resources** (only available when `Deployed`) to:

- Adjust CPU and memory requests/limits
- Add, edit, or remove environment variables

Saving triggers a rolling restart of the deployment pod. The flow continues serving requests from the old pod until the new one is ready.

## Removing a Deployment

Click **⋯ → Remove Deployment** and confirm the browser prompt. The row transitions to `Removing` and disappears once Kubernetes finishes deleting the pod and associated resources.

> Removing a deployment does not delete the flow from Langflow — it only stops the standalone serving pod.

## Troubleshooting

**Deployment stays in "Deploying" for more than 5 minutes:**
- Check the logs via **⋯ → Logs**. Common causes: image pull failure, missing environment variables, insufficient cluster resources.
- After 5 minutes in a non-ready state, the status automatically transitions to **Failed**.

**Deployment shows "Failed":**
- Open logs to see the error. Common causes:
  - Missing Global Variables — add them in Langflow Settings → Global Variables and re-deploy.
  - Port conflict or crash on startup — check the Python traceback in logs.

**"Name already in use" error when deploying:**
- A deployment with the same name already exists (or a previous one is still terminating).
- Wait ~30 seconds and try again, or choose a different name.

**"The following global variables are referenced but not found":**
- The flow uses Global Variables that are not defined in your Langflow settings.
- Go to **Settings → Global Variables**, add the missing variables, then deploy again.

**cURL tab is blank or shows "Could not load":**
- The deployment is not yet in `Deployed` state — wait for it to finish starting up.
- If status is `Deployed` and cURL is still blank, try closing and reopening the detail panel.

See also: [API Usage](./api-usage.md) for how to call a deployed flow endpoint.
