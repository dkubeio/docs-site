# DKubeX Documentation

*Version {{ doc_version }}*

DKubeX is a Kubernetes-native platform for deploying, managing, and operating AI and ML applications from a single control plane. It layers a self-service application catalog, a governed model plane, and integrated developer tooling over a standard Kubernetes cluster — so teams can run the full model lifecycle, from training to governed inference, on their own infrastructure.

## At a glance

| | |
|---|---|
| **Category** | Self-hosted MLOps / LLMOps platform |
| **Foundation** | Kubernetes (k3s-compatible), single-cluster |
| **Deployment** | On-premises or cloud; firewall-aware, private-registry-based |
| **Control plane** | FastAPI backend · React 19 UI · Kopf operator |
| **App model** | Custom `Application` CRD + one-click catalog (Helm under the hood) |
| **Ingress & auth** | Traefik + ForwardAuth SSO, per-app RBAC, seat-based licensing |
| **Data layer** | PostgreSQL 16 · MinIO (S3-compatible) · Redis · NFS shared storage |
| **Model serving** | KubeAI (LLMs/embeddings) · KServe (classic ML) · MLflow registry |
| **AI gateway** | SecureLLM — governed, audited, OpenAI-compatible model access |
| **GPU** | NVIDIA GPU Operator, per-model resource profiles, scale-to-zero |
| **Observability** | ClickStack + OpenTelemetry (GPU / vLLM dashboards) |
| **Interfaces** | React web UI · REST API (`/api/v1`, Swagger/ReDoc) · `Application` CRD (`kubectl`) |
| **Applications** | Workspace · ModelStudio · MLflow · SecureLLM · RAGFlow · Langflow |
| **Core license** | MIT (platform core) |

## What DKubeX is

Rather than stitching together separate tools for training, serving, RAG, and developer environments, DKubeX provides a single control plane that:

- **Runs the full model lifecycle** — train in a workspace, register versions in MLflow, deploy classic ML through KServe and LLMs/embeddings through KubeAI, then govern every model through SecureLLM.
- **Treats applications as declarative Kubernetes resources** — each install is a custom `Application` resource that an operator reconciles to a running Helm release, with a live status phase and access URL.
- **Enforces one identity and governance layer** — a single authenticated control plane provides SSO across every app, per-application RBAC, seat-based licensing, and per-user namespace isolation.
- **Keeps models and data on your infrastructure** — models are served cluster-local and fronted by an auditable gateway; the platform is firewall-aware and pulls images from a configurable private registry.

> **Note:** Apps install into a dedicated `dkubex-apps` namespace; each user also receives an isolated namespace and a per-user persistent volume (`user-storage` PVC).

## Platform architecture

The user interface is routed through Traefik and authentication into the Kubernetes cluster, where the core control plane, application store, data and storage, observability, and admin tooling run as coordinated subsystems.

```{figure} images/dkubex-architecture.png
:alt: DKubeX platform architecture — user interface routed through Traefik and auth into the Kubernetes cluster (core control plane, app store, data and storage, observability, admin tools, and infrastructure).
:width: 100%

DKubeX platform architecture at a glance.
```

## Explore the documentation

- **[Installation](installation.md)** — install DKubeX on your Kubernetes cluster with Helm.
- **[Applications](applications/index.md)** — user guides for Workspace, ModelStudio, RAGFlow, SecureLLM, and Langflow.
- **[Tutorials](tutorials/index.md)** — end-to-end guides across governing LLM access, LLMs and RAG, MLOps, and coding agents.

```{toctree}
:maxdepth: 10
:includehidden:
:caption: Contents

self
installation
applications/index
tutorials/index
```
