# Installing DKubeX

This guide installs DKubeX using the Helm chart.

## Prerequisites

### Hardware requirements

DKubeX runs on a single Kubernetes cluster.

| Resource | Minimum | Recommended |
|---|---|---|
| CPU | 8 cores | 16 cores |
| Memory | 32 GB RAM | 64 GB RAM |
| Storage | 200 GB SSD | 500 GB SSD |
| Nodes | 1 | 1 |

```{note}
- **Per additional user workspace**, add **1 CPU core, 8 GB RAM, and 20 GB storage**.
- **GPUs are optional and model-dependent.** The core platform runs on CPU only. GPUs are required
  only when you want to deploy and serve your own models on-premises.
- An **external NFS server** is required in every configuration for shared and per-user storage.
```

### Additional requirements

#### Install Helm

DKubeX is installed with Helm 3.x. Install it on the machine you will run the install from:

::::{tab-set}

:::{tab-item} macOS
```bash
brew install helm
```
:::

:::{tab-item} Linux
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
:::

::::

Then confirm Helm is installed and reports a 3.x version:

```bash
helm version
```

#### Tokens

You need two GitHub PATs:

1. `GITHUB_TOKEN` and `dkubex.env.helm_token`: the same fine-grained read-only token used to read the DKubeX Helm chart repository.
2. `registry.token`: a GitHub PAT for registry access. The user must have access to the DKubeX repository on GitHub.

Export them:

```bash
export GITHUB_TOKEN="<finegrained_readonly_token_for_helm_repo>"
export REGISTRY_TOKEN="<github_pat_with_access_to_dkubex_repo>"
```

## Install DKubeX

Run these commands in order.

1. Add the DKubeX Helm repository:

   ```bash
   helm repo add dkubeio \
   	--username "${GITHUB_TOKEN}" \
   	--password "${GITHUB_TOKEN}" \
   	"https://raw.githubusercontent.com/dkubeio/helm-charts/main/"
   ```

2. Update the repository index:

   ```bash
   helm repo update
   ```

3. Install DKubeX:

   ```bash
   helm install -n dkubex --create-namespace dkubex-installer dkubeio/dkubex-installer \
   	--set registry.token="${REGISTRY_TOKEN}" \
   	--set dkubex.env.helm_token="${GITHUB_TOKEN}"
   ```

````{note}
The recommended setup is an **external NFS server** for storage with the **internal PostgreSQL**.
To install with an external NFS server and an external PostgreSQL, first export their values:

```bash
export PG_USER="<postgres_user>"
export PG_PASSWORD="<postgres_password>"
export PG_HOST="<postgres_host>"
export NFS_SERVER="<nfs_server_address>"
export NFS_PATH="<nfs_export_path>"
```

Then run:

```bash
helm install -n dkubex --create-namespace dkubex-installer dkubeio/dkubex-installer \
	--set registry.token="${REGISTRY_TOKEN}" \
	--set dkubex.env.helm_token="${GITHUB_TOKEN}" \
	--set postgres.enabled=false \
	--set pgadmin.enabled=false \
	--set db_url="postgresql+psycopg://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:5432/dkubex?sslmode=require" \
	--set nfs.enabled=true \
	--set nfs.server="${NFS_SERVER}" \
	--set nfs.path="${NFS_PATH}"
```
````
