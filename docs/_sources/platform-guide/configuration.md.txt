# Configuration

Enable and configure platform components from the admin console under **Config**. The page has five
tabs — **Auth & Certs, Storage, Services, Telemetry, Workspace** — a **Apply** button, and a **Recent
Deployments** history.

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

## Review configuration history

The **Recent Deployments** section lists past configuration applies with their timestamp, status, and
what changed (for example, *Enabled: nfs, clickstack, otel, minio, redis, tls*).
