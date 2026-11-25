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

## If an upgrade fails

A failed upgrade leaves the platform on the version that was already running, and the **Platform** page
keeps showing that version.

1. Read the error output shown on the **Platform** page. The cause is often in the installer job's log:

   ```bash
   kubectl logs job/dkubex-installer -n dkubex
   ```

2. Fix the cause, select the version in **Upgrade To** again, and click **Upgrade Platform**. A failed
   upgrade can be retried directly; it does not need a rollback first.

:::{note}
Upgrade from the **Platform** page rather than running `helm upgrade dkubex-installer` by hand. The
settings you change under **Config** are stored with the platform, and the **Platform** page upgrade
reuses them.
:::

## Recover a stuck upgrade

If an upgrade is interrupted and leaves the platform in a stuck state, run the following in the
installer namespace (`dkubex`), then retry the upgrade:

```bash
helm rollback dkubex-installer -n dkubex
```
