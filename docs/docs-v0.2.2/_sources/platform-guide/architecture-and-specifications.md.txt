# Architecture & Specifications

DKubeX layers a self-service application platform over a standard Kubernetes cluster. This page
describes the platform's subsystems and the hardware and software it requires.

## Architecture

```{figure} ../images/dkubex-architecture.png
:alt: DKubeX 2.0 platform architecture — the user interface routed through ingress and authentication into the Kubernetes cluster, with the control plane, application store, data and storage, observability, and admin tooling.
:width: 100%

DKubeX 2.0 platform architecture at a glance.
```

The platform is organized into a few coordinated subsystems, all running on a single cluster:

- **Control plane** — the platform backend, web UI, and the operator that reconciles the `Application`
  custom resource into running Helm releases.
- **Ingress & authentication** — a single cluster ingress fronted by an authentication layer that
  provides single sign-on across every application.
- **Application catalog** — the set of installable applications, each modeled as a declarative
  Kubernetes resource with a live status and access URL.
- **Model & compute plane** — LLM/embedding serving (KubeAI) and classic-ML serving (KServe), backed by
  the MLflow model registry, with optional GPU acceleration.
- **Data & storage** — the platform database, object storage, and shared NFS-backed storage for the
  cluster and per-user volumes.
- **Observability & admin tooling** — cluster telemetry and the operational dashboards administrators
  use to run the platform.

(system-requirements)=
## System requirements

DKubeX runs on a single Kubernetes cluster. The core platform is entirely CPU-based — you only need
GPUs if you intend to deploy and serve your own models on-premises.

### Minimum

A single node running all services:

| Resource | Minimum |
|---|---|
| CPU | 8 cores |
| Memory | 32 GB RAM |
| Storage | 200 GB SSD |
| Nodes | 1 |
| Storage backend | External NFS server |

### Recommended

Comfortable headroom for all applications plus a few user workspaces on a single node:

| Resource | Recommended |
|---|---|
| CPU | 16 cores |
| Memory | 64 GB RAM |
| Storage | 500 GB SSD |
| Nodes | 1 |
| Storage backend | External NFS server |

### Sizing notes

- **Per additional user workspace**, add **1 CPU core, 8 GB RAM, and 20 GB storage**.
- **GPUs are optional and model-dependent.** The core platform runs on CPU only. GPUs are required
  only when you want to deploy and serve your own models on-premises.
- An **external NFS server** is required in every configuration for shared and per-user storage.

Once your cluster meets these requirements, follow [Installation](../getting-started/installation.md)
to deploy DKubeX.
