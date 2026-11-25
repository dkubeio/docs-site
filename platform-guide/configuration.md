# Configuration

Enable and configure platform components from the admin console under **Config**. The page has five
tabs — **Auth & Certs, Storage, Services, Telemetry, Workspace** — a **Apply** button, and a **Recent
Deployments** history. A sixth tab, **Credentials**, holds the **Helm Repository Token** (used to pull
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

### Recover from a bad authentication change

If an authentication change stops users from signing in, the first administrator can still sign in with
a password, because the login page always offers **Sign in with email and password**.

1. Open the login page and choose **Sign in with email and password**.
2. Sign in as the first administrator. The password is stored in the `dkubex-secret` secret:

   ```bash
   kubectl get secret dkubex-secret -n dkubex -o jsonpath='{.data.first-superuser-password}' | base64 -d
   ```

3. Open **Config → Auth & Certs**, correct the OAuth2 Proxy settings or turn it off, and click **Apply**.

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

## If an apply fails

**Apply** opens a dialog that follows the deployment and, if it fails, shows **Deployment failed** with
the full output. Your new settings stay saved; nothing is reverted automatically.

1. Read the output in the dialog to find the setting or component that failed.
2. Correct that setting, or turn the component back off.
3. Click **Apply** again. If another apply or a platform upgrade is still running, wait for it to finish
   first; only one can run at a time.

## Review configuration history

The **Recent Deployments** section lists past configuration applies with their timestamp, status, and
what changed (for example, *Enabled: nfs, clickstack, otel, minio, redis, tls*).
