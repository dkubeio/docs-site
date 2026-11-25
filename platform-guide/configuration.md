# Configuration

Enable and configure platform components from the admin console under **Config**. The page has five
tabs — **Auth & Certs, Storage, Services, Telemetry, Workspace** — and an **Apply** button. A sixth tab, **Credentials**, holds the **Helm Repository Token** (used to pull
application charts from the built-in dkubeio repository) and the **Container Registry Token** (used by
the cluster to pull platform and application images).

:::{warning}
Clicking **Apply** redeploys the affected components in the background. Applying an authentication
change can affect every user's ability to sign in — confirm your values before applying, and apply
during a maintenance window. Only one platform deployment (config apply or platform upgrade) can run at
a time.
:::

## Configure authentication (OAuth2)

1. Open **Config** → **Auth & Certs**.
2. Turn on **OAuth2 Proxy**.
3. Enter the provider details — provider (**GitHub** or **SSO**/OIDC), client ID, client secret,
   organization, and the OAuth redirect URL.
4. Click **Apply**.

While OAuth is enabled, new users are provisioned automatically on first sign-in and admins do not
create accounts by hand (see [User Management](user-management.md)).

## Enable HTTPS / TLS

1. Open **Config** → **Auth & Certs**.
2. Turn on **HTTPS / TLS Certificate**.
3. Provide the **Certificate (PEM)** and **Private Key (PEM)** — paste them in, or use **Upload file**.
4. Click **Apply**.

The ingress serves over HTTPS once the certificate is provisioned.

## Configure other components

The remaining tabs enable and configure the platform's built-in components:

| Tab | Configures |
|---|---|
| **Storage** | Object storage and shared/persistent storage. |
| **Services** | Platform services. |
| **Telemetry** | Observability components. |
| **Workspace** | Developer-workspace defaults. |

Change the settings on a tab and click **Apply**.

## Follow a deployment

Clicking **Apply** (shown as **Save & Apply** while a tab has unsaved changes) opens a dialog that follows
the deployment. It shows **Applying configuration** ("Processing… This can take a few minutes. Closing
this window does not stop the deployment."), then **Deployment completed** ("The configuration was
applied successfully.") or **Deployment failed** ("The deployment did not complete. See the logs
below.").
