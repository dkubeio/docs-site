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
Values are read at install time. After that, settings you change in the admin console under
**Config** are stored with the platform, and tokens rotated under **Config → Credentials** take
precedence over any token passed on the command line. Upgrade from the admin console's **Platform**
page rather than running `helm upgrade dkubex-installer` by hand (see
[Platform Upgrade](../platform-guide/platform-upgrade.md)).
```

## Admin account and access

| Value | Default | What it does |
|---|---|---|
| `admin.email` | `admin@local.com` | Email of the first admin. Set only on the first install; see [Admin account](installation.md#admin-account). |
| `admin.password` | generated | Password of the first admin. If omitted, a random one is generated and stored in the `dkubex-secret` secret; see [Open DKubeX and sign in](installation.md#open-dkubex-and-sign-in). |
| `domain` | `""` | Hostname DKubeX is served on. Empty means any host or IP address. |
| `auth.enabled` | `false` | Turns on sign-in through an OAuth provider (OAuth2 Proxy). |
| `auth.provider` | `github` | OAuth provider: `github` or `oidc`. |
| `auth.github.client_id`, `auth.github.client_secret` | `""` | Credentials of the GitHub OAuth app. |
| `auth.github.redirect_url` | `http://k8s.orb.local/oauth2/callback` | OAuth callback, in the form `http://<dkubex-access-domain or ip>/oauth2/callback`. |
| `auth.github.organization` | `oneconvergence` | Optional. GitHub organization whose members may sign in. |
| `auth.oidc.issuer`, `auth.oidc.client_id`, `auth.oidc.client_secret` | empty | OIDC provider settings, used when `auth.provider` is `oidc`. |
| `tls.enabled` | `true` | HTTPS switch. `false` serves plain HTTP; `true` without a certificate uses a self-signed one. |
| `tls.cert`, `tls.key` | `""` | Certificate and private key as PEM contents (not file paths). Load the files with `--set-file tls.cert=cert.pem --set-file tls.key=key.pem`. |

## Images and tokens

| Value | Default | What it does |
|---|---|---|
| `registry.server` | `ghcr.io` | Container registry for platform and application images. |
| `registry.username` | `dkubeio` | Registry user. |
| `registry.token` | `""` | Registry token. Without it no image pull secret is created and the installer cannot pull its images. See [Tokens](installation.md#tokens). |
| `dkubex.env.helm_token` | `""` | GitHub token for the application chart repository. See [Tokens](installation.md#tokens). |
| `dkubex.env.helm_url` | `https://raw.githubusercontent.com/dkubeio/helm-charts/main` | Repository the application catalog comes from. |
| `kyverno.enabled` | `true` | Copies the registry pull secret into user and application namespaces. When off, DKubeX copies it itself. |

## Database

| Value | Default | What it does |
|---|---|---|
| `postgres.enabled` | `true` | Installs an in-cluster PostgreSQL. Set `false` to use an external server through `db_url`; see [External PostgreSQL](installation.md#external-postgresql). |
| `postgres.db_user`, `postgres.db_password` | `postgres`, `postgrespassword` | Credentials of the in-cluster server. Keep `db_url` in sync with them. |
| `postgres.image.repository`, `postgres.image.tag` | `dkubex123/bitnami-pgvector`, `pg16` | In-cluster PostgreSQL image. |
| `postgres.tls.enabled` | `true` | Serves the in-cluster database over TLS with a self-signed certificate. `db_url`'s `sslmode=require` relies on it; remove that from `db_url` if you turn this off. |
| `pgadmin.enabled` | `true` | pgAdmin web UI for the in-cluster database. Installed only when `postgres.enabled` is also `true`. |
| `db_url` | `postgresql+psycopg://postgres:postgrespassword@postgresql/dkubex?sslmode=require` | Database DKubeX (and Prefect) use. On an external server the user needs permission to create databases. |

## Storage

| Value | Default | What it does |
|---|---|---|
| `storageClassName` | `""` | StorageClass for the whole platform: infrastructure, applications and user volumes. Empty means `nfs` when NFS is on, otherwise the cluster's default class. |
| `nfs.enabled` | `false` | Turns on the NFS provisioner. |
| `nfs.server`, `nfs.path` | `nfs-server.dkubex.svc.cluster.local`, `/` | NFS server and export path. |
| `nfs.storageSize`, `nfs.storageClassName` | `10Gi`, `nfs` | Size of the NFS volume and the name of its StorageClass. |
| `userStorage.size` | `10Gi` | Size of each user's storage volume. |
| `userStorage.accessMode` | `""` | Empty means `ReadWriteMany` when NFS is on, `ReadWriteOnce` otherwise. |
| `userStorage.pvcName` | `user-storage` | Name of each user's volume. Do not change it after the first user exists: existing volumes are not renamed and apps that mount this name break. |
| `minio.enabled`, `minio.storageSize` | `true`, `50Gi` | In-cluster object storage and its size. |
| `filebrowser.enabled`, `filebrowser.hostPath` | `false`, `/var/lib/rancher/k3s/storage` | Platform file browser and the host path it serves. |

## GPUs

See [GPU nodes](installation.md#gpu-nodes) for when to change these.

| Value | Default | What it does |
|---|---|---|
| `hami.enabled` | `true` | HAMi GPU sharing (scheduler and device plugin). |
| `hami.devicePlugin.nvidiaNodeSelector` | `{gpu: "on"}` | Node labels the HAMi device plugin runs on. |
| `hami.devicePlugin.preConfiguredDeviceMemory` | `0` | GPU memory per device in MiB. `0` detects it automatically; unified-memory GPUs (DGX) need a value such as `120000`. |
| `hami.devicePlugin.runtimeClassName` | `nvidia` | RuntimeClass GPU pods use. |
| `hami.devicePlugin.reportNodeCapacity` | `true` | Reports GPU memory and cores in each node's capacity. Needed wherever Karpenter or cluster-autoscaler provisions GPU nodes. |
| `gpuOperator.enabled` | `false` | Installs the NVIDIA GPU Operator. |
| `cloudProvider` | `""` | `aks`, `eks` or `gke` turn on platform-specific workarounds; empty for generic or on-premises clusters. See [Cloud-specific notes](installation.md#cloud-specific-notes). |

## Observability and services

| Value | Default | What it does |
|---|---|---|
| `telemetry.enabled` | `true` | The whole observability stack: ClickStack, the OpenTelemetry collectors, tracing, and (with HAMi) the HAMi WebUI. |
| `clickstack.tag` | `2.46.0` | ClickStack version. |
| `clickstack.storageSize` | `10Gi` | ClickHouse data volume. |
| `clickstack.keeperStorageSize` | `5Gi` | ClickHouse Keeper volume (coordination state only). |
| `clickstack.memory` | `4Gi` | ClickHouse server memory. |
| `otel.tracesEndpoint` | `http://cluster-telemetry-opentelemetry-collector.dkubex.svc.cluster.local:4318` | Where traces are sent. |
| `otel.sampleRate` | `1.0` | Share of requests traced (0.0 to 1.0). |
| `redis.enabled`, `redis.memory_limit` | `true`, `256Mi` | Redis and its memory limit. |
| `prefect.enabled` | `false` | Prefect server and worker. |
| `cert-manager.enabled` | `false` | Installs cert-manager. |
| `headlamp.enabled` | `true` | Headlamp cluster UI. |

## Workspaces

Defaults for each user's workspace when they install it. An admin can change CPU, memory, GPU, image
tag and tolerations per workspace afterwards.

| Value | Default | What it does |
|---|---|---|
| `workspace.imageRepository`, `workspace.imageTag` | `ghcr.io/dkubeio/workspace`, `v1.0.1` | Workspace image. |
| `workspace.defaultCpu` | `2` | CPU limit. The request is half of it. |
| `workspace.defaultMemory` | `16` (Gi) | Memory limit. The request is half of it. |
| `workspace.defaultGpu` | `0` | GPUs per workspace. |
| `workspace.defaultGpuMemory` | `0` | GPU memory cap per GPU in MiB; `0` means no cap. Applies only when `defaultGpu` is above `0`. |
| `workspace.defaultTolerations` | `[]` | Tolerations for new workspaces, for example to run on tainted GPU nodes. |

## Platform lifecycle

| Value | Default | What it does |
|---|---|---|
| `defaultApps` | `[securellm]` | Applications installed automatically on a new platform. An app an admin uninstalls is not re-created. |
| `uninstall.drainTimeoutSeconds` | `300` | How long uninstall waits for applications to be removed. Read at install time. |
| `uninstall.jobDeadlineSeconds` | `1200` | Time limit of the uninstall job. Read at install time; uninstall with `helm uninstall dkubex-installer -n dkubex --timeout 20m`. |
| `airgap.enabled` | `false` | Air-gap mode. |
| `controller.enabled` | `true` | The application controller. |

## Internal values

These exist in the chart but are not meant to be changed for a normal install.

| Value | Default | Note |
|---|---|---|
| `environment` | `production` | Must be `local`, `staging` or `production`. |
| `dkubex.image.tag` | set by the release | Platform image tag. |
| `dkubex.env.apps_chart_image_tag` | `main` | Used only with a local chart server. |
| `auth.supported_providers` | `[github]` | Not used. |
| `pgvector.host`, `pgvector.user`, `pgvector.password`, `pgvector.db`, `pgvector.model` | empty | Not used. |
