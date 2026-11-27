# Platform Guide

The Platform Guide covers administering DKubeX itself — the control plane underneath every
application. All the tasks here are performed from the **admin console**, which an administrator opens
from the **Admin** link in the top-right header (`/admin/dashboard`).

The admin console sidebar has: **Dashboard, Applications, Workspaces, Users, Licenses, Config,
Platform**.

## In this section

- **[User Management](user-management.md)** — add, edit, assign roles to, and remove users.
- **[Access Requests](access-requests.md)** — approve or dismiss users' requests for application access.
- **[Application Management](application-management.md)** — install, upgrade, and uninstall applications.
- **[Configuration](configuration.md)** — authentication, TLS, storage, and platform components.
- **[Workspaces](workspaces.md)** — view and manage per-user developer workspaces.
- **[Licensing](licensing.md)** — cluster ID, licenses, and seats.

Installing and upgrading DKubeX are in [Install and upgrade](../install/index.md), including
[Platform Upgrade](../install/platform-upgrade.md) (upgrade the DKubeX installer). The platform's
subsystems and requirements are in
[Architecture & Specifications](../getting-started/architecture-and-specifications.md), under Get started.

## The admin dashboard

**Dashboard** is the console landing page. It is read-only and shows:

- **Cluster Overview** — Kubernetes cluster status: **Nodes** (ready/total), **Pods Running**, **Pods
  Pending**, and **Pods Failed**.
- **Resource Usage** — cluster-wide CPU, memory, and GPU usage. Usage history needs the ClickStack and
  OpenTelemetry components; until they are on, the section reads "Usage history needs the ClickStack and
  OpenTelemetry components. Enable them under Config → Telemetry." See
  [Configuration](configuration.md#configure-other-components).
- **Node Details** — capacity and status per cluster node: the node name, CPU, memory, and status (for
  example **Ready**).

```{figure} ../images/admin-dashboard.png
:alt: The admin console Dashboard — Cluster Overview cards for Nodes (1/1 ready), Pods Running, Pods Pending and Pods Failed; Resource Usage with the note that usage history needs the ClickStack and OpenTelemetry components; and Node Details listing one node with its CPU, memory and Ready status.
:width: 100%

The admin dashboard.
```

```{toctree}
:hidden:

user-management
access-requests
application-management
configuration
workspaces
licensing
```
