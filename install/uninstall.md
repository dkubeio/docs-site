---
og:description: "Uninstall DKubeX with Helm: the command, what the uninstall job removes, and what it keeps."
myst:
  html_meta:
    description: "Uninstall DKubeX with Helm: the command, what the uninstall job removes, and what it keeps."
---

# Uninstall DKubeX

Uninstall the platform with:

```bash
helm uninstall dkubex-installer -n dkubex --timeout 20m
```

Always pass `--timeout 20m`. The uninstall job first deletes every installed application and waits
for the DKubeX controller to uninstall each one, then removes the platform. That wait plus the
removal exceeds Helm's default timeout of 5 minutes. When the timeout is hit, Helm reports a failure
and keeps the release, while the job goes on removing the platform.

The uninstall job, in order:

1. Deletes every installed application and waits (up to 300 seconds by default) for the controller to
   uninstall each one.
2. Scales the `dkubex` deployment to zero and deletes the user namespaces DKubeX created, together
   with each user's workspace and its storage.
3. Removes the platform components (`helmfile destroy`) and the in-cluster PostgreSQL release.
4. Deletes the `Application` CRD.
5. Only if the removal succeeded, deletes the installer's own resources, including its ConfigMap, the
   `dkubex-registry-secret` secret and the ClickStack volume claims.

The job can be run again safely. If Helm timed out, or the removal failed partway, run the same
`helm uninstall` command again.

## What uninstall keeps

- The PostgreSQL volume claim (`data-postgresql-0`) and the MinIO volume claim are left on purpose, so
  a new install reattaches to the same data instead of starting empty.
- The secret that holds the platform's generated credentials is left on purpose. A new install reuses
  it instead of generating new values, so data encrypted with its keys stays readable.
- A namespace DKubeX adopted rather than created is never deleted; only the resources DKubeX put
  inside it are removed.

Whether users' home data survives depends on the storage class:

- With NFS enabled, the `nfs` storage class uses `reclaimPolicy: Retain`. The NFS share still holds
  every user's home directory, and the released volumes are left to clean up by hand.
- With NFS disabled (the default), user storage uses the cluster's default storage class. On k3s that
  is `local-path` (`reclaimPolicy: Delete`), which removes the volume along with its claim.

```{note}
The drain wait and the job's time limit are set by `uninstall.drainTimeoutSeconds` (default `300`)
and `uninstall.jobDeadlineSeconds` (default `1200`). They are read at install time, so change them
with a `helm upgrade` before you uninstall. Keep `jobDeadlineSeconds` at or below the `--timeout` you
pass to `helm uninstall`.
```
