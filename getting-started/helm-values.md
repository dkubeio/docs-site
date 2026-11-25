---
og:description: "Every value of the DKubeX installer Helm chart (dkubex-installer): defaults and what each one does, grouped by purpose."
myst:
  html_meta:
    description: "Every value of the DKubeX installer Helm chart (dkubex-installer): defaults and what each one does, grouped by purpose."
---

# Helm Values Reference

These are the values of the `dkubex-installer` chart you install in [Installation](installation.md).
Pass them with `--set key=value` (or `--set-file` for certificates) on `helm install`. The defaults
below are the chart's own.

```{note}
Components an admin toggles in the admin UI (NFS, cert-manager, TLS, auth and others) are
stored in the installer ConfigMap, not in the Helm release values. Upgrade through the admin UI
(see [Platform Upgrade](../platform-guide/platform-upgrade.md)): a bare
`helm upgrade dkubex-installer` resets the ConfigMap to the release values and loses those toggles.
```

## Admin account and access

| Value | Default | What it does |
|---|---|---|
| `admin.email` | `admin@local.com` | Admin email. See [Admin account](installation.md#admin-account). |
| `admin.password` | none | Admin password. Not in the chart's values file; if you omit it, the installer generates a random one. See [Admin account](installation.md#admin-account). |
| `domain` | `""` | DKubeX domain. |
| `auth.enabled` | `false` | Turns auth on or off. |
| `auth.provider` | `github` | Auth provider. |
| `auth.github.client_id`, `auth.github.client_secret` | `""` | GitHub client ID and client secret. |
| `auth.github.redirect_url` | `http://k8s.orb.local/oauth2/callback` | OAuth callback, in the form `http://<dkubex-access-domain or ip>/oauth2/callback`. |
| `auth.github.organization` | `oneconvergence` | Optional. GitHub organization. |
| `auth.oidc.issuer`, `auth.oidc.client_id`, `auth.oidc.client_secret` | empty | OIDC issuer, client ID and client secret. |
| `tls.enabled` | `true` | The single HTTP-vs-HTTPS switch for the Traefik ingress. `false` serves plain HTTP; `true` without a certificate uses a self-signed one; `true` with `tls.cert` and `tls.key` uses the supplied certificate. |
| `tls.cert`, `tls.key` | `""` | Certificate and private key as PEM contents (not file paths). Load the files with `--set-file tls.cert=cert.pem --set-file tls.key=key.pem`. |

## Images and tokens

| Value | Default | What it does |
|---|---|---|
| `registry.server` | `ghcr.io` | Registry server. |
| `registry.username` | `dkubeio` | Registry username. |
| `registry.token` | `""` | Registry token. Without it no pull secret is created and the installer Job sits in `ImagePullBackOff`. See [Tokens](installation.md#tokens). |
| `dkubex.env.helm_token` | `""` | GitHub token for helm-charts repository access. See [Tokens](installation.md#tokens). |
| `dkubex.env.helm_url` | `https://raw.githubusercontent.com/dkubeio/helm-charts/main` | Helm repository URL. |
| `kyverno.enabled` | `true` | Kyverno clones the registry pull secret into user and application namespaces labeled `dkubex.io/managed-by=dkubex`. When disabled, the backend copies the secret into user namespaces and the dkubex chart renders it directly into `dkubex-apps`. |

## Database

| Value | Default | What it does |
|---|---|---|
| `postgres.enabled` | `true` | In-cluster PostgreSQL. Set `false` to use an external server instead and point `db_url` at it; see [External PostgreSQL](installation.md#external-postgresql). |
| `postgres.db_user`, `postgres.db_password` | `postgres`, `postgrespassword` | Credentials of the in-cluster server. Keep `db_url` in sync with them. |
| `postgres.image.repository`, `postgres.image.tag` | `dkubex123/bitnami-pgvector`, `pg16` | In-cluster PostgreSQL image. |
| `postgres.tls.enabled` | `true` | Serves TLS with a chart-generated self-signed certificate. `db_url`'s `sslmode=require` makes DKubeX refuse plaintext; drop it from `db_url` if you disable this. |
| `pgadmin.enabled` | `true` | pgAdmin web UI for the in-cluster database. Installs only when `postgres.enabled` is also `true`; set `false` to drop it while keeping the database. |
| `db_url` | `postgresql+psycopg://postgres:postgrespassword@postgresql/dkubex?sslmode=require` | Database URL, also used by Prefect. The installer creates the `dkubex` and `prefect` databases on this server, so on an external server the user needs `CREATEDB` unless both databases already exist. |

## Storage

| Value | Default | What it does |
|---|---|---|
| `storageClassName` | `""` | Platform-wide StorageClass: infrastructure releases, the NFS server volume, every `dkubex-apps` chart, and user and workspace volumes. Empty means the `nfs` class when the NFS provisioner is on, otherwise the cluster default. |
| `nfs.enabled` | `false` | NFS provisioner. |
| `nfs.server`, `nfs.path` | `nfs-server.dkubex.svc.cluster.local`, `/` | NFS server and path. |
| `nfs.storageSize`, `nfs.storageClassName` | `10Gi`, `nfs` | NFS storage size and StorageClass name. |
| `userStorage.size` | `10Gi` | Size of each user's volume. |
| `userStorage.accessMode` | `""` | Empty means `ReadWriteMany` when NFS is enabled, `ReadWriteOnce` otherwise. |
| `userStorage.pvcName` | `user-storage` | Name of each user's volume. Do not change it after the first user namespace is created: existing user volumes are not renamed and apps that mount this name will break. |
| `minio.enabled`, `minio.storageSize` | `true`, `50Gi` | MinIO and its storage size. |
| `filebrowser.enabled`, `filebrowser.hostPath` | `false`, `/var/lib/rancher/k3s/storage` | File browser and its host path. |

## GPUs

See [GPU nodes](installation.md#gpu-nodes) for when to change these.

| Value | Default | What it does |
|---|---|---|
| `hami.enabled` | `true` | HAMi GPU sharing (scheduler and device plugin). |
| `hami.devicePlugin.nvidiaNodeSelector` | `{gpu: "on"}` | Node labels the HAMi device plugin requires. On DGX (nodes not labelled `gpu=on`) drop it with `--set hami.devicePlugin.nvidiaNodeSelector.gpu=null`. |
| `hami.devicePlugin.preConfiguredDeviceMemory` | `0` | MiB of GPU memory advertised per device. `0` auto-detects it (discrete GPUs); unified-memory GPUs (DGX) can't be auto-detected, so set a value such as `120000`. |
| `hami.devicePlugin.runtimeClassName` | `nvidia` | Runtime class name of the HAMi device plugin. |
| `hami.devicePlugin.reportNodeCapacity` | `true` | Reports each node's total GPU memory and GPU cores in its capacity. Required wherever Karpenter provisions GPU nodes; also lets cluster-autoscaler size scale-ups from a live node. Unused with static pools. |
| `gpuOperator.enabled` | `false` | GPU Operator. |
| `cloudProvider` | `""` | Managed Kubernetes platform: empty (generic or on-premises), `aks`, `eks` or `gke`. Enables platform-specific workarounds in the installed charts. See [Cloud-specific notes](installation.md#cloud-specific-notes). |

## Observability and services

| Value | Default | What it does |
|---|---|---|
| `telemetry.enabled` | `true` | Single switch for the whole observability stack: ClickStack, the OpenTelemetry collectors, Traefik and backend tracing, and (with `hami.enabled`) the HAMi WebUI. |
| `clickstack.tag` | `2.38.0` | ClickStack tag. |
| `clickstack.storageSize` | `10Gi` | ClickHouse data volume. |
| `clickstack.keeperStorageSize` | `5Gi` | ClickHouse Keeper volume. Small by design: it stores coordination state, never table data. |
| `clickstack.memory` | `4Gi` | ClickHouse server memory (request = limit). |
| `otel.tracesEndpoint` | `http://cluster-telemetry-opentelemetry-collector.dkubex.svc.cluster.local:4318` | OTLP/HTTP endpoint that Traefik and the DKubeX backend export traces to. |
| `otel.sampleRate` | `1.0` | Head-sampling ratio applied at the Traefik edge (0.0 to 1.0). |
| `redis.enabled`, `redis.memory_limit` | `true`, `256Mi` | Redis and its memory limit. |
| `prefect.enabled` | `false` | Prefect. |
| `cert-manager.enabled` | `false` | cert-manager. |
| `headlamp.enabled` | `true` | Headlamp. |

## Workspaces

Defaults applied when a user installs a workspace from the Applications page. An admin can edit CPU,
memory, GPU, image tag and tolerations per workspace afterwards.

| Value | Default | What it does |
|---|---|---|
| `workspace.imageRepository`, `workspace.imageTag` | `ghcr.io/dkubeio/workspace`, `v1.0.1` | Workspace image. |
| `workspace.defaultCpu` | `2` | CPU limit. The request is half of it. |
| `workspace.defaultMemory` | `16` (Gi) | Memory limit. The request is half of it. |
| `workspace.defaultGpu` | `0` | GPUs per workspace. |
| `workspace.defaultGpuMemory` | `0` | Per-GPU memory cap in MiB; `0` means no cap (the workspace sees the whole card). Applies only when `defaultGpu` is above `0`. |
| `workspace.defaultTolerations` | `[]` | Tolerations applied to newly installed workspaces. |

## Platform lifecycle

| Value | Default | What it does |
|---|---|---|
| `defaultApps` | `[{applicationName: securellm}]` | Apps installed automatically on a fresh platform, at their latest published version. An admin uninstall is durable: a seeded app is not re-created. |
| `uninstall.drainTimeoutSeconds` | `300` | How long uninstall waits for applications to be finalized before force-clearing their finalizers. `0` skips the wait. Read at install time. |
| `uninstall.jobDeadlineSeconds` | `1200` | Time limit of the uninstall job. Read at install time; uninstall with `helm uninstall dkubex-installer -n dkubex --timeout 20m`. |
| `airgap.enabled` | `false` | Air-gap image-mutation webhook. |
| `controller.enabled` | `true` | Controller. |

## Internal values

These exist in the chart but are not meant to be changed for a normal install.

| Value | Default | Note |
|---|---|---|
| `environment` | `production` | Deployment environment reported to the backend. Must be `local`, `staging` or `production`. |
| `dkubex.image.tag` | `dev` | Image tag. No description in the chart. |
| `dkubex.env.apps_chart_image_tag` | `main` | Chart-server sidecar image tag. The sidecar is rendered only when `helm_url` points at `localhost:8081` or `127.0.0.1:8081`. |
| `chart_versions.traefik` | `40.1.0` | No description in the chart. |
| `auth.supported_providers` | `[github]` | No description in the chart. |
| `pgvector.host`, `pgvector.user`, `pgvector.password`, `pgvector.db`, `pgvector.model` | `""` | No description in the chart. |
