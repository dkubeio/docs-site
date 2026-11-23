---
og:description: "Install DKubeX with its Helm chart: prerequisites, production recommendations, external PostgreSQL, GPU nodes, NVIDIA DGX and cloud-specific notes."
myst:
  html_meta:
    description: "Install DKubeX with its Helm chart: prerequisites, production recommendations, external PostgreSQL, GPU nodes, NVIDIA DGX and cloud-specific notes."
---

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
- An **external NFS server** is required in every configuration for shared and per-user storage, with **1 TB** of storage recommended.
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

#### Admin account

Choose the email and password of the first DKubeX admin user:

```bash
export ADMIN_EMAIL="<admin_email>"
export ADMIN_PASSWORD="<admin_password>"
```

```{note}
The admin credentials are set only on the first install. Later upgrades keep the existing admin
account, even if you pass different values. If you omit `admin.password`, the installer generates a
random one; if you omit `admin.email`, it defaults to `admin@local.com`.
```

## Production recommendations

For anything beyond evaluation, set up storage and the database as follows:

| Area | Recommendation |
|---|---|
| Storage | Use an **external NFS server**, or a **StorageClass that supports `ReadWriteMany` (RWX)**. User workspaces and apps share volumes across pods and nodes, which a `ReadWriteOnce` class cannot do. |
| Database | Use an **external PostgreSQL** server (managed or self-hosted) that you back up and monitor yourself. The in-cluster PostgreSQL suits evaluation only. |
| PostgreSQL user | The user in `db_url` must be able to **create databases**. See [External PostgreSQL](#external-postgresql). |

To use an existing RWX StorageClass instead of NFS, pass its name at install time:

```bash
--set storageClassName="<rwx_storage_class>" \
--set userStorage.accessMode=ReadWriteMany
```

When `storageClassName` is empty, DKubeX uses the `nfs` class if NFS is enabled, and the cluster's
default StorageClass otherwise.

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
   	--set dkubex.env.helm_token="${GITHUB_TOKEN}" \
   	--set admin.email="${ADMIN_EMAIL}" \
   	--set admin.password="${ADMIN_PASSWORD}"
   ```

````{note}
For production, use an **external NFS server** for storage and an **external PostgreSQL** (see
[Production recommendations](#production-recommendations)). To install with both, first export their values:

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
	--set admin.email="${ADMIN_EMAIL}" \
	--set admin.password="${ADMIN_PASSWORD}" \
	--set postgres.enabled=false \
	--set pgadmin.enabled=false \
	--set db_url="postgresql+psycopg://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:5432/dkubex?sslmode=require" \
	--set nfs.enabled=true \
	--set nfs.server="${NFS_SERVER}" \
	--set nfs.path="${NFS_PATH}"
```
````

## External PostgreSQL

When `postgres.enabled=false`, DKubeX connects to the server in `db_url`. On every install and
upgrade, the installer creates the `dkubex` and `prefect` databases on that server if they are missing.
Applications you install from the **App Store** also get their own databases provisioned on the same
server.

The user in `db_url` therefore needs **privileges to create databases**. Use a superuser or a user
with `CREATEDB`:

```sql
CREATE USER dkubex WITH PASSWORD '<password>' CREATEDB;
```

```{warning}
If the user cannot create databases, the platform installs but App Store apps that need a database
fail to deploy.
```

### Required PostgreSQL extensions

DKubeX and its apps use these extensions:

- `uuid-ossp`
- `pg_trgm`
- `pgcrypto`

Self-hosted PostgreSQL ships them by default. Managed services may require you to allow them first;
see [Cloud-specific notes](#cloud-specific-notes).

## GPU nodes

DKubeX uses [HAMi](https://project-hami.io/) to share GPUs between workloads. HAMi runs its own NVIDIA
device plugin, which is the only component that may register `nvidia.com/gpu` on a node.

### Label GPU nodes

By default, HAMi's device plugin runs only on nodes labeled `gpu=on`:

```bash
kubectl label node <gpu_node_name> gpu=on
```

To select GPU nodes by a different label instead, for example the one NVIDIA's feature discovery adds,
pass:

```bash
--set hami.devicePlugin.nvidiaNodeSelector.gpu=null \
--set-string 'hami.devicePlugin.nvidiaNodeSelector.nvidia\.com/gpu\.present=true'
```

### Clusters running the NVIDIA GPU Operator

If the NVIDIA GPU Operator is already installed on the cluster, its device plugin conflicts with
HAMi's: both register `nvidia.com/gpu`, and the scheduler sees the physical GPU count instead of
HAMi's shared slots. **Disable the GPU Operator's device plugin** and keep HAMi's.

Update the existing GPU Operator release, keeping its other values:

```bash
helm upgrade gpu-operator nvidia/gpu-operator -n gpu-operator \
	--reuse-values \
	--set devicePlugin.enabled=false
```

Then confirm no GPU Operator device-plugin pods remain:

```bash
kubectl get pods,daemonsets -n gpu-operator | grep device-plugin
```

Also disable any separately installed NVIDIA device plugin on the same nodes.

For more details, see HAMi's guide to
[preparing nodes with the NVIDIA GPU Operator](https://project-hami.io/docs/v2.10.0/installation/prerequisites#prepare-nodes-with-nvidia-gpu-operator).

## Installing on NVIDIA DGX

DGX nodes need two changes to the default GPU settings:

1. **Node selection.** DGX nodes are not labeled `gpu=on`. Label each DGX node so HAMi's device plugin
   runs on it:

   ```bash
   kubectl label node <dgx_node_name> gpu=on
   ```

2. **GPU memory.** On DGX systems whose GPUs use unified memory, HAMi cannot detect the GPU memory size.
   Set the memory advertised per GPU, in MiB:

   ```bash
   --set hami.devicePlugin.preConfiguredDeviceMemory=120000
   ```

   Adjust the value to the memory you want to make available to GPU workloads on each device.

If the DGX runs the NVIDIA GPU Operator, also disable its device plugin as described in
[Clusters running the NVIDIA GPU Operator](#clusters-running-the-nvidia-gpu-operator).

A full DGX install command looks like this:

```bash
helm install -n dkubex --create-namespace dkubex-installer dkubeio/dkubex-installer \
	--set registry.token="${REGISTRY_TOKEN}" \
	--set dkubex.env.helm_token="${GITHUB_TOKEN}" \
	--set admin.email="${ADMIN_EMAIL}" \
	--set admin.password="${ADMIN_PASSWORD}" \
	--set hami.devicePlugin.preConfiguredDeviceMemory=120000
```

## Cloud-specific notes

Set `cloudProvider` to the managed Kubernetes platform you install on (`aks`, `eks`, or `gke`). It
turns on platform-specific workarounds in the installed charts:

```bash
--set cloudProvider=aks
```

### Azure (AKS and Azure Database for PostgreSQL)

- **Allow the required extensions.** Azure Database for PostgreSQL – Flexible Server only creates
  extensions that are on its allow list. In the Azure portal, open the server's
  **Server parameters**, find `azure.extensions`, and add **`UUID-OSSP`**, **`PG_TRGM`**, and
  **`PGCRYPTO`**. Save the change before installing DKubeX. With the Azure CLI:

  ```bash
  az postgres flexible-server parameter set \
  	--resource-group <resource_group> \
  	--server-name <server_name> \
  	--name azure.extensions \
  	--value UUID-OSSP,PG_TRGM,PGCRYPTO
  ```

  If `azure.extensions` already lists other extensions, keep them in the value.

- **Database creation.** Use the server's admin user in `db_url`, or a role granted `CREATEDB`
  (see [External PostgreSQL](#external-postgresql)).
- **TLS.** Azure requires TLS, so keep `sslmode=require` in `db_url`.
- **AKS.** Set `cloudProvider=aks`. AKS's Admissions Enforcer owns the namespace selector on
  admission webhooks, and Helm upgrades of HAMi otherwise conflict with it.
- **Create the `nvidia` RuntimeClass.** DKubeX runs HAMi's device plugin with the `nvidia`
  RuntimeClass, and HAMi adds it to every pod that requests a GPU. The NVIDIA GPU Operator
  normally creates it, but AKS GPU node pools without the operator do not have it, and then every
  GPU pod fails to start. Check whether it exists:

  ```bash
  kubectl get runtimeclass nvidia
  ```

  If it is missing, create it before installing DKubeX. On AKS the handler must be
  `nvidia-container-runtime`, the name of the containerd runtime that AKS GPU nodes configure;
  the GPU Operator's `nvidia` handler does not exist there:

  ```bash
  kubectl apply -f - <<'EOF'
  apiVersion: node.k8s.io/v1
  kind: RuntimeClass
  metadata:
    name: nvidia
  handler: nvidia-container-runtime
  EOF
  ```

  If a `nvidia` RuntimeClass already exists with a different handler, check that its handler
  matches a runtime configured on the GPU nodes; otherwise GPU pods fail to start.

#### GPU autoscaling on AKS (Karpenter)

GPU node autoscaling on AKS requires **Karpenter**, which AKS provides as node auto-provisioning
(NAP). Enable it on your cluster with the official guide:
[Node auto-provisioning in AKS](https://learn.microsoft.com/en-us/azure/aks/node-autoprovision).

Then create a Karpenter `NodePool` for each GPU VM size, plus a `NodeOverlay` for each VM size.

**Why the overlays are needed.** HAMi splits each GPU into shared slots and adds HAMi resources
(`nvidia.com/gpumem`, `nvidia.com/gpucores`) to GPU pods. Karpenter only knows the VM's physical
GPU count, so without an overlay it cannot tell which VM size fits a pending GPU pod. A
`NodeOverlay` tells Karpenter what HAMi will report on that VM size:

| Resource | Value |
|---|---|
| `nvidia.com/gpu` | `deviceSplitCount` (default 10) × physical GPUs |
| `nvidia.com/gpumem` | Total GPU memory in MiB. Keep it at or below the real value, or Karpenter places pods that HAMi then rejects. |
| `nvidia.com/gpucores` | 100 × physical GPUs |

Requirements:

- HAMi must report these resources on the node. Keep `hami.devicePlugin.reportNodeCapacity=true`
  (the default). Without it, Karpenter never marks GPU nodes as initialized and never removes them.
- The NodePool must label nodes `gpu: "on"`, which matches the default
  `hami.devicePlugin.nvidiaNodeSelector`. NAP nodes don't get the `accelerator` label.
- If the NodePool taints GPU nodes (recommended), GPU workspaces need a matching toleration. Set it
  for new workspaces with `workspace.defaultTolerations`:

  ```bash
  --set-json 'workspace.defaultTolerations=[{"key":"nvidia.com/gpu","operator":"Exists","effect":"NoSchedule"}]'
  ```

- Workloads must not request `nvidia.com/gpumem-percentage`. Karpenter can't place them.

Example for one A10 VM size (`Standard_NV36ads_A10_v5`, 1× A10 24 GB):

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: gpu-a10
spec:
  weight: 20                      # higher weight is tried first
  template:
    metadata:
      labels:
        gpu: "on"                 # selected by HAMi's device plugin and dcgm-exporter
    spec:
      nodeClassRef:
        group: karpenter.azure.com
        kind: AKSNodeClass
        name: default
      taints:
        - key: nvidia.com/gpu
          value: present
          effect: NoSchedule
      requirements:
        - key: karpenter.azure.com/sku-name
          operator: In
          values: ["Standard_NV36ads_A10_v5"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
      expireAfter: Never
  disruption:
    consolidationPolicy: WhenEmpty  # remove only empty nodes; never evict GPU workloads
    consolidateAfter: 5m
  limits:
    nodes: "1"                      # cap on GPU nodes from this pool
---
apiVersion: karpenter.sh/v1alpha1
kind: NodeOverlay
metadata:
  name: hami-nv36ads-a10-v5
spec:
  requirements:
    - key: node.kubernetes.io/instance-type
      operator: In
      values: ["Standard_NV36ads_A10_v5"]
  capacity:
    nvidia.com/gpu: "10"          # 10 HAMi slots x 1 GPU
    nvidia.com/gpumem: "24512"    # MiB
    nvidia.com/gpucores: "100"    # 100 x 1 GPU
```

To find the real `gpumem` value for a VM size, start one node and read what HAMi reports:

```bash
kubectl get node <node> -o jsonpath='{.status.capacity.nvidia\.com/gpumem}'
```


### AWS (EKS)

- **EKS.** Set `cloudProvider=eks`.
- **Create the `nvidia` RuntimeClass.** As on AKS, DKubeX needs a RuntimeClass named `nvidia`,
  because HAMi adds it to every pod that requests a GPU. Check whether it exists:

  ```bash
  kubectl get runtimeclass nvidia
  ```

  If it is missing, create it before installing DKubeX. On EKS the handler is `nvidia`:

  ```bash
  kubectl apply -f - <<'EOF'
  apiVersion: node.k8s.io/v1
  kind: RuntimeClass
  metadata:
    name: nvidia
  handler: nvidia
  EOF
  ```

#### GPU autoscaling on EKS (Karpenter)

GPU node autoscaling on EKS requires **Karpenter**. Install and configure it with the
[Karpenter getting started guide](https://karpenter.sh/docs/getting-started/), including an
`EC2NodeClass` for your cluster. Enable Karpenter's **`nodeOverlay` feature gate**, or Karpenter
ignores the overlays below.

Then create one GPU `NodePool` and one `NodeOverlay` for each GPU instance type. The overlay values
and requirements are the same as in
[GPU autoscaling on AKS (Karpenter)](#gpu-autoscaling-on-aks-karpenter).

Example for `g5.4xlarge` (1× NVIDIA A10G), using an `EC2NodeClass` named `default`:

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: gpu-g5-4xlarge
spec:
  template:
    metadata:
      labels:
        gpu: "on"                 # selected by HAMi's device plugin and dcgm-exporter
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      taints:
        - key: nvidia.com/gpu
          value: present
          effect: NoSchedule
      requirements:
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["g5.4xlarge"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
  limits:
    nodes: "4"                    # cap on GPU nodes from this pool
  disruption:
    consolidationPolicy: WhenEmpty  # remove only empty nodes; never evict GPU workloads
    consolidateAfter: 10m
---
apiVersion: karpenter.sh/v1alpha1
kind: NodeOverlay
metadata:
  name: hami-gpu-g5-4xlarge
spec:
  requirements:
    - key: node.kubernetes.io/instance-type
      operator: In
      values: ["g5.4xlarge"]
  capacity:
    nvidia.com/gpu: "10"          # 10 HAMi slots x 1 GPU
    nvidia.com/gpumem: "23028"    # MiB
    nvidia.com/gpucores: "100"    # 100 x 1 GPU
```

To find the `gpumem` value for an instance type, start one node and read what HAMi reports:

```bash
kubectl get node <node> -o jsonpath='{.status.capacity.nvidia\.com/gpumem}'
```
