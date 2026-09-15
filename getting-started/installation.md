# Installing DKubeX

This guide installs DKubeX using the Helm chart.

## Before you begin

Make sure your cluster meets the minimum hardware and software requirements before installing.
DKubeX runs on a single Kubernetes cluster and needs, at minimum, **8 CPU cores, 32 GB RAM, 200 GB SSD,
one node, and an external NFS server**; 16 cores / 64 GB RAM / 500 GB SSD is recommended for comfortable
headroom. GPUs are optional and only needed to serve your own models on-prem. See
[Architecture & Specifications](../platform-guide/architecture-and-specifications.md#system-requirements)
for the full requirements, including how to size additional user workspaces.

## Prerequisites

Install Helm (Helm 3.x).

### Install Helm

macOS (Homebrew):

```bash
brew install helm
```

Linux:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify Helm:

```bash
helm version
```

## Tokens

You need two GitHub PATs:

1. `GITHUB_TOKEN` and `dkubex.env.helm_token`: the same fine-grained read-only token used to read the DKubeX Helm chart repository.
2. `registry.token`: a GitHub PAT for registry access. The user must have access to the DKubeX repository on GitHub.

Export them:

```bash
export GITHUB_TOKEN="<finegrained_readonly_token_for_helm_repo>"
export REGISTRY_TOKEN="<github_pat_with_access_to_dkubex_repo>"
```

## Install DKubeX

```bash
helm repo add dkubeio \
	--username "${GITHUB_TOKEN}" \
	--password "${GITHUB_TOKEN}" \
	"https://raw.githubusercontent.com/dkubeio/helm-charts/main/"

helm repo update

helm install -n dkubex --create-namespace dkubex-installer dkubeio/dkubex-installer \
	--set registry.token="${REGISTRY_TOKEN}" \
	--set dkubex.env.helm_token="${GITHUB_TOKEN}"
```

