# Workflows

These walkthroughs chain together the individual tasks described in [Getting started](./getting-started.md), [Managing workspaces](./managing-workspaces.md), and [Using your workspace](./using-your-workspace.md) into common, end-to-end scenarios.

## Spin up a workspace and start working in JupyterLab

1. On the **Home** page, click **New Workspace** and give it a **name** (Step 1).
2. Pick an **application bundle** — for example, the *Minimal* bundle, which includes JupyterLab, Terminal, and FileBrowser (Step 2).
3. Choose a **compute profile** for CPU, RAM, and GPU (Step 3), then review and click **Create** (Step 4).
4. Wait for the workspace card to move from **Creating** to **Running**.
5. On the workspace card, click **Add App**, select **JupyterLab**, and click **Launch**.
6. When the access link appears on the card, click it to open JupyterLab in a new tab.
7. Save your work under `/home/workspace` so it persists across pod restarts and stops.

## Share a workspace with a teammate

1. Make sure the workspace you want to share is one you own (it appears under **Your Workspaces** on the Home page).
2. Open the workspace's actions menu (⋮) → **Share**.
3. Enter the username(s) or email(s) of the people you want to share with, then click **Share**.
4. Your teammate will now see the workspace under **Shared with You** on their own Home page and can open apps in it.
5. To revoke access later, open **Share** again, find the user in the shared-access list, and click **Remove** next to their name.

## Pause and resume to save resources without losing data

1. When you are done for now, open the workspace's actions menu (⋮) → **Stop**. The pod shuts down cleanly and your data on the persistent volume is preserved.
2. When you want to continue, click **Start** on the workspace card — the pod starts and your previous session is restored.
3. If you will not need the workspace for a while, use **Archive** instead: the pod is stopped and the workspace moves off your main dashboard, with data retained.
4. To bring an archived workspace back, go to the **Archived** tab, click **Restore**, and then **Start** it normally.
