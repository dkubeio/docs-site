# Workspaces

View and manage per-user developer workspaces from the admin console under **Workspaces**. Users
install and uninstall their own workspaces; this page gives administrators a cluster-wide view.

The page opens with four summary cards — **Total Workspaces**, **Running**, **Stopped**, and **Failed** —
above the workspace table and a **Search workspaces…** box. Each workspace row shows:

| Column | Meaning |
|---|---|
| **User** | The workspace owner. |
| **Status** | Running, or another lifecycle state. |
| **Resources** | Allocated CPU, memory, and GPU (for example, `2 CPU · 16Gi · 0 GPU`). |
| **Version** | The workspace version. |

## Manage a user's workspace

1. Open the admin console → **Workspaces**.
2. Find the user's workspace in the table, or type in **Search workspaces…**.
3. Open the **⋮** menu on the row to act on that workspace.

Use this to check a user's workspace status and resource usage across the cluster.

```{figure} ../images/admin-workspaces.png
:alt: The admin console Workspaces page — Total Workspaces, Running, Stopped and Failed cards above a search box and a table with User, Status, Resources and Version columns and a ⋮ actions menu on the row. The version value is blurred.
:width: 100%

The admin console's Workspaces page.
```

## Next steps

- [User Management](user-management.md): manage user accounts
- [Troubleshooting](../reference/troubleshooting.md#workspace-and-coding-agents): workspace and coding agent problems
