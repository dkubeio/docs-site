# Platform Upgrade

Upgrade DKubeX in place from the admin console under **Platform** — no reinstall. Post-install
component toggles (from [Configuration](configuration.md)) are preserved across upgrades.

The **Installer** card shows the current and available versions of the `dkubex-installer` chart.

## Upgrade the platform

1. Open the admin console → **Platform**.
2. On the **Installer** card, check the **Current Version**.
3. Select the target from the **Upgrade To** selector.
4. Click **Upgrade Platform**.
5. Watch the live progress until it completes. Your installed applications stay available throughout.

When you are already on the latest version, the card shows **Up to date** and the **Upgrade Platform**
button is disabled.

:::{warning}
A platform upgrade changes the running control plane. Run it during a maintenance window, and be ready
to recover before you start.
:::

## Recover a stuck upgrade

If an upgrade is interrupted and leaves the platform in a stuck state, run the following in the
installer namespace, then retry the upgrade:

```bash
helm rollback dkubex-installer
```
