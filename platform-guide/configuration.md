# Configuration

Enable and configure platform components from the admin console under **Config**. The page has six
tabs — **Auth & Certs, Storage, Services, Telemetry, Workspace, Credentials** — and an **Apply** button. The **Credentials** tab holds the **Helm Repository Token** (used to pull
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
3. Enter the provider details — **Auth Provider** (**GitHub** or **OIDC**), **Client ID**, **Client
   Secret**, **GitHub Organization** (GitHub only), and **OAuth Redirect URL**.
4. Click **Apply**.

While OAuth is enabled, new users are provisioned automatically on first sign-in and admins do not
create accounts by hand (see [User Management](user-management.md)).

## Enable HTTPS / TLS

1. Open **Config** → **Auth & Certs**.
2. Turn on **HTTPS / TLS Certificate**.
3. Provide the **Certificate (PEM)** and **Private Key (PEM)** — paste them in, or use **Upload file**.
4. Click **Apply**.

The ingress serves over HTTPS once the certificate is provisioned.

## Rotate credentials

The **Credentials** tab rotates the tokens DKubeX uses to pull application charts and container images.
The change applies in place, with no reinstall.

1. Open **Config** → **Credentials**. Each token shows **Configured** or **Not set**.
2. To rotate the **Helm Repository Token** (used to pull application charts from the built-in dkubeio
   repository; the card shows the **Repository URL**), paste the new token in **New token**. The token is
   verified against the repository before anything is saved. Applying it restarts the backend, which may
   be briefly unavailable.
3. To rotate the **Container Registry Token** (used by the cluster to pull platform and application
   images; the card shows the **Registry** and **Username**), paste the new token in **New token**. It
   updates the image pull secret, and managed namespaces pick it up from there. Pods stuck pulling images
   retry with the new token.
4. Click **Apply** to save the changes.

```{note}
You can rotate one token or both: leave the **New token** field empty for any token you do not want to
update. Then click **Apply** to save the changes.
```

## Configure other components

The remaining tabs enable and configure the platform's built-in components:

| Tab | Configures |
|---|---|
| **Storage** | Object storage and shared/persistent storage. |
| **Services** | Platform services. |
| **Telemetry** | Observability components. |
| **Workspace** | Developer-workspace defaults. |
| **Credentials** | The Helm repository and container registry tokens (see [Rotate credentials](#rotate-credentials)). |

Change the settings on a tab and click **Apply**.

## Follow a deployment

Clicking **Apply** (shown as **Save & Apply** while a tab has unsaved changes) opens a dialog that follows
the deployment. It shows **Applying configuration** ("Processing… This can take a few minutes. Closing
this window does not stop the deployment."), then **Deployment completed** ("The configuration was
applied successfully.") or **Deployment failed** ("The deployment did not complete. See the logs
below.").

## Next steps

- [User Management](user-management.md): manage user accounts and sign-in modes
- [Platform Upgrade](../install/platform-upgrade.md): upgrade DKubeX in place; component toggles are preserved
- [Application Management](application-management.md): install and manage applications
