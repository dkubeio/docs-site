# Installing DKubeX 2.0

This guide installs DKubeX 2.0 using the Helm chart.

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

1. `GITHUB_TOKEN` and `dkubex.env.helm_token`: the same fine-grained read-only token used to read the DKubeX 2.0 Helm chart repository.
2. `registry.token`: a GitHub PAT for registry access. The user must have access to the DKubeX 2.0 repository on GitHub.

Export them:

```bash
export GITHUB_TOKEN="<finegrained_readonly_token_for_helm_repo>"
export REGISTRY_TOKEN="<github_pat_with_access_to_dkubex_repo>"
```

## Install DKubeX 2.0

```bash
helm repo add dkubeio-dev \
	--username "${GITHUB_TOKEN}" \
	--password "${GITHUB_TOKEN}" \
	"https://raw.githubusercontent.com/dkubeio/helm-charts/dev/"

helm repo update

helm install -n dkubex --create-namespace dkubex-installer dkubeio-dev/dkubex-installer \
	--set registry.token="${REGISTRY_TOKEN}" \
	--set dkubex.env.helm_token="${GITHUB_TOKEN}"
```

