# Platform Overview

DKubeX is a Kubernetes-native platform for deploying, managing, and operating AI and ML applications
from a single control plane. Rather than stitching together separate tools for training, serving, RAG,
and developer environments, it layers a self-service application catalog, a governed model plane, and
integrated developer tooling over a standard Kubernetes cluster.

## What DKubeX gives you

- **The full model lifecycle** — train in a Workspace, register versions in MLflow, deploy classic ML
  through KServe and LLMs/embeddings through KubeAI, then govern every model through SecureLLM.
- **Applications as declarative Kubernetes resources** — each install is a custom `Application` resource
  that an operator reconciles to a running Helm release, with a live status and access URL. The catalog
  abstracts Helm away behind one-click install, upgrade, and uninstall.
- **One identity and governance layer** — a single authenticated control plane provides SSO across every
  app, per-application RBAC, and per-user isolation.
- **Models and data on your own infrastructure** — models are served cluster-local and fronted by an
  auditable gateway; the platform is firewall-aware and pulls images from a configurable private registry.

## Platform architecture

The user interface is routed through ingress and authentication into the Kubernetes cluster, where the
control plane, application catalog, data and storage, observability, and admin tooling run as
coordinated subsystems.

```{figure} ../images/dkubex-architecture.png
:alt: DKubeX 2.0 platform architecture — the user interface routed through ingress and authentication into the Kubernetes cluster, with the control plane, application store, data and storage, observability, and admin tooling.
:width: 100%

DKubeX 2.0 platform architecture at a glance.
```

For the full breakdown of subsystems, components, and hardware requirements, see
[Architecture & Specifications](../platform-guide/architecture-and-specifications.md).

## The applications

DKubeX ships a set of first-class applications that share one identity layer, one model plane, and one
gateway:

| Application | What it is |
|---|---|
| **Workspace** | On-demand, isolated cloud development environment with built-in AI coding agents |
| **ModelStudio** | Browse, deploy, and test open-source and NVIDIA models on your cluster |
| **MLflow** | Experiment tracking and model registry |
| **SecureLLM** | Governed, OpenAI-compatible AI gateway fronting every model |
| **RAGFlow** | Document-grounded RAG — knowledge bases, hybrid search, cited chat |
| **Langflow** | Visual, low-code builder for AI workflows and agents |
| **VKE** | Virtual Kubernetes Engineer — an SRE console for the cluster |

Each application has its own guide under [Applications](../applications/index.md).

## The model lifecycle

DKubeX covers the full path from training to governed inference:

1. **Train** — in a Workspace, with model-tracking credentials available in the environment.
2. **Track & register** — log runs and register model versions in the MLflow registry.
3. **Deploy** — classic ML models via KServe; LLMs and embeddings via KubeAI, onto CPU or GPU resource
   profiles.
4. **Govern** — front every deployed model with SecureLLM for keys, guardrails, and metering.
5. **Consume** — run inference from the ModelStudio Playground, RAGFlow, Langflow, or Workspace agents.

## Where to go next

- **[Installation](installation.md)** — stand up DKubeX on your cluster.
- **[Quickstart](quickstart.md)** — deploy and chat with a model in minutes.
- **[Platform Guide](../platform-guide/index.md)** — architecture, access management, the catalog, and licensing.
