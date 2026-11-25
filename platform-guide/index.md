# Platform Guide

The Platform Guide covers administering DKubeX itself — the control plane underneath every
application. All the tasks here are performed from the **admin console**, which an administrator opens
from the **Admin** link in the top-right header (`/admin/dashboard`).

The admin console sidebar has: **Dashboard, Applications, Workspaces, Users, Licenses, Config,
Platform**.

## In this section

- **[Architecture & Specifications](architecture-and-specifications.md)** — subsystems and the hardware/software requirements.
- **[User Management](user-management.md)** — add, edit, assign roles to, and remove users.
- **[Access Requests](access-requests.md)** — approve or dismiss users' requests for application access.
- **[Application Management](application-management.md)** — install, upgrade, and uninstall applications.
- **[Configuration](configuration.md)** — authentication, TLS, storage, and platform components.
- **[Workspaces](workspaces.md)** — view and manage per-user developer workspaces.
- **[Licensing](licensing.md)** — cluster ID, licenses, and seats.
- **[Platform Upgrade](platform-upgrade.md)** — upgrade the DKubeX installer.

## The admin dashboard

**Dashboard** is the console landing page. It is read-only and shows:

- **Users** — total users and superusers.
- **Deployments** — total, successful, failed, and last deployment date.
- **Cluster Overview** — nodes (ready/total), pods (running/pending/failed), and per-node details.
- **Platform Status** — each platform component (auth, cert-manager, clickstack, filebrowser, minio,
  nfs, otel, prefect, redis, tls) shown as Enabled or Disabled.
- **App Role Distribution** — admin/user counts per application.

```{toctree}
:hidden:

architecture-and-specifications
user-management
access-requests
application-management
configuration
workspaces
licensing
platform-upgrade
```
