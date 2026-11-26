---
og:description: "Terms used across the DKubeX documentation, each with a short meaning and a link to the page that explains it."
myst:
  html_meta:
    description: "Terms used across the DKubeX documentation, each with a short meaning and a link to the page that explains it."
---

# Glossary

Terms used across these docs, in alphabetical order. Each entry links to the page that explains it in
full.

| Term | Meaning | See |
|---|---|---|
| Access request | A request from a user for access to an application they aren't assigned to. An administrator approves or dismisses it. | [Access Requests](../platform-guide/access-requests.md) |
| `Application` custom resource | The declarative Kubernetes resource each installed application is modeled as. The platform reconciles it into a Helm release, so you never run Helm by hand. | [Application Management](../platform-guide/application-management.md) |
| App Store | The page where users install applications, such as their Workspace. | [Workspace](../applications/workspace/index.md) |
| Browse Catalog | The admin console tab (under **Applications**) that lists the applications an administrator can install. | [Application Management](../platform-guide/application-management.md) |
| Cluster ID | The identifier of your cluster. A license is bound to one cluster, so DKube needs it to issue a license. | [Licensing](../platform-guide/licensing.md#get-your-cluster-id) |
| CRD | A Kubernetes custom resource definition. DKubeX uses the `Application` CRD for applications; ModelStudio deploys LLMs as KubeAI `Model` CRDs and ML models as KServe `InferenceService` CRDs. | [Application Management](../platform-guide/application-management.md), [ModelStudio › Deploying models](../applications/modelstudio/deploying-models.md) |
| `dkubex-installer` | The Helm chart that installs DKubeX. Its values are listed in the Helm Values Reference. | [Helm Values Reference](helm-values.md) |
| GGUF | A quantized model format. The Ollama engine runs GGUF models, so a model can be deployed without a GPU. | [Deploying a Model on CPU](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-cpu.md) |
| Guardrail | An automatic safety filter in SecureLLM that inspects AI requests and responses before they reach the AI or your users. | [SecureLLM › Admin features](../applications/securellm/admin-features.md#guardrails) |
| HAMi | The GPU sharing component (scheduler and device plugin) installed with DKubeX. It lets several models share one GPU through ModelStudio's **GPU Memory (GiB)** setting. | [Helm Values Reference](helm-values.md), [ModelStudio › Deploying models](../applications/modelstudio/deploying-models.md) |
| KServe | The serving layer for classic machine-learning models (for example sklearn, XGBoost, PyTorch), deployed from an MLflow registry or HuggingFace. | [Architecture & Specifications](../platform-guide/architecture-and-specifications.md), [ModelStudio](../applications/modelstudio/index.md) |
| KubeAI | The serving layer for large language models and embedding models. | [Architecture & Specifications](../platform-guide/architecture-and-specifications.md), [ModelStudio](../applications/modelstudio/index.md) |
| License, seat | DKubeX applications are gated by seat-based licenses. A license is issued for one cluster and grants a number of seats per application: one seat per user, per application. | [Licensing](../platform-guide/licensing.md) |
| NGC API key | An NVIDIA NGC Personal API Key, added in ModelStudio **Settings → NGC API Keys**, needed to deploy NIM models. | [ModelStudio › Deploying models](../applications/modelstudio/deploying-models.md) |
| NIM | NVIDIA NIM models: registered from the NVIDIA NGC catalog and deployed in-cluster on GPU nodes. | [ModelStudio › Deploying models](../applications/modelstudio/deploying-models.md) |
| OAuth2 Proxy | The authentication layer you turn on under **Config → Auth & Certs** to sign users in through GitHub or OIDC, giving single sign-on across every application. | [Configuration](../platform-guide/configuration.md#configure-authentication-oauth2) |
| Ollama | The inference engine for CPU deployments; it runs GGUF models. | [Deploying a Model on CPU](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-cpu.md) |
| PAT | A GitHub personal access token. The install command asks for one with access to the DKubeX repository (`REGISTRY_TOKEN`), and publishing an app to the App Store uses a classic personal access token. | [Installation](installation.md), [Publishing an app](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md) |
| Placeholder | A value in angle brackets in a command, such as `<admin_email>` or `<rwx_storage_class>`. Replace it with your own value before you run the command. | [Installation](installation.md) |
| Resource profile | A named resource configuration (CPU, memory, GPU, replicas) in ModelStudio that you load into the deploy forms. A GPU deployment requests its GPUs through the resource profile you select. | [ModelStudio › Getting started](../applications/modelstudio/getting-started.md#resource-profiles), [Deploying a Model on GPU](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-gpu.md) |
| SecureLLM | Your organization's secure gateway to AI: every AI request goes through one central hub your team controls, for consistent access, cost tracking and safety guardrails. | [SecureLLM](../applications/securellm/index.md) |
| Single sign-on (SSO) | Signing in once with your organization's existing credentials to use every DKubeX application, with no separate account or password. | [Quickstart](quickstart.md), [Architecture & Specifications](../platform-guide/architecture-and-specifications.md) |
| vLLM | The inference engine for GPU deployments. | [Deploying a Model on GPU](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-gpu.md) |
| Workspace | Your personal, on-demand development environment in the cluster, installed from the App Store, with JupyterLab, VS Code, a terminal, a file browser and AI coding agents. | [Workspace](../applications/workspace/index.md) |
