# Using Your Workspace

Once your workspace is **Running**, you can launch development apps inside it, work with persistent files, and share it with teammates.

## Using Apps

Each workspace can run multiple development tools, called **apps**, side by side.

### Available Apps

| App | What it is |
|---|---|
| **JupyterLab** | Interactive notebook environment for Python, R, and more |
| **Terminal** | Browser-based command-line terminal |
| **FileBrowser** | Graphical file manager for your workspace files |

### Launching an App

1. Open your workspace card and click **Add App** (or the **+** button).
2. Select the app you want to launch.
3. Click on **Launch**.

The app starts inside the workspace pod and an access link appears on the workspace card. Click the link to open it in a new tab.

### Stopping an App

Click the **Stop** button next to an app's link on the workspace card. The app process inside the pod is stopped; other apps continue running.

> **Note:** Apps open in your browser over a secure, authenticated route — you do not need to manage ports or SSH tunnels.

## Workspace Files

Every workspace has a persistent volume mounted at `/home/workspace`. Files saved here survive pod restarts and stops. Use the **FileBrowser** app or the **Terminal** to manage files.

To transfer files from your laptop:
- Use the **FileBrowser** app's upload button.
- Use `scp` or `rsync` from the Terminal (if SSH is configured by your admin).

## Sharing a Workspace

You can give other users access to your workspace (read-and-execute, not ownership).

**To share:**

1. Open the actions menu → **Share**.
2. Enter the username(s) or email(s) of the people you want to share with.
3. Click **Share**.

Shared users will see the workspace in the **Shared with Me** section on their Home page and can open apps in it.

**To remove access:**

1. Open the actions menu → **Share**.
2. Find the user in the shared-access list.
3. Click **Remove** next to their name.

> **Note:** Only the workspace owner can share or unshare it. Shared users cannot modify workspace settings or delete it.
