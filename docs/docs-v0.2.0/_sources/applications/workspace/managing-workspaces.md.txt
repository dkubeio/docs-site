# Managing Workspaces

Every workspace moves through a lifecycle — from creation, through running and stopping, to archiving or deletion. This page covers the statuses a workspace can have and the actions available on each workspace card.

## Workspace Statuses

| Status | What it means |
|---|---|
| **Creating** | The workspace pod is being provisioned |
| **Running** | The workspace is active and apps are accessible |
| **Stopped** | The pod is shut down; your data is preserved |
| **Archived** | The workspace is soft-deleted; pod is stopped but data is retained |
| **Error** | Something went wrong; check logs for details |

## Managing Your Workspace

Each workspace card has an actions menu (⋮) with the following options:

### Start / Stop / Restart

- **Start** — wakes a stopped workspace; the pod starts and your previous session is restored.
- **Stop** — shuts down the pod cleanly; data on the persistent volume is preserved.
- **Restart** — stops and immediately restarts the pod; useful when an app becomes unresponsive.

### Edit

Click **Edit** (pencil icon) to change the workspace's compute resources (CPU, GPU, memory, storage). Changes take effect on the next start.

### Logs

Click the **Logs** button to view live logs from the workspace pod — useful for diagnosing startup failures or app errors.

### Archive

Archiving is a soft-delete: the workspace pod is stopped and the workspace is moved off your main dashboard. Your data is preserved on the persistent volume.

1. Open the actions menu → **Archive**.
2. Confirm the action.

To view archived workspaces, use the **Archived** tab on the Home page.

### Restore

To bring an archived workspace back:

1. Go to the **Archived** tab.
2. Find the workspace and click **Restore**.

The workspace returns to the **Stopped** status and can be started normally.

### Delete

Permanently removes the workspace and all its data. This action **cannot be undone**.

1. Open the actions menu → **Delete**.
2. Type the workspace name to confirm.
3. Click **Delete**.

> **Warning:** Deleting a workspace destroys its persistent volume. Archive it instead if you might need the data later.

## Getting Help

If your workspace is stuck in **Creating** or **Error** state for more than a few minutes, click **Logs** to see what went wrong and share the output with your platform administrator.
