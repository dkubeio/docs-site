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

The minimum and recommended CPU, memory, storage and node counts, the extra resources for each user
workspace, and the external NFS server are listed in one place:
[Installation › Hardware requirements](../install/installation.md#hardware-requirements).
Once your cluster meets them, follow the rest of [Installation](../install/installation.md)
to deploy DKubeX.

## Next steps

- [Installation](../install/installation.md): install DKubeX on your cluster
- [Helm Values Reference](../reference/helm-values.md): the installer chart's values
- [Configuration](../platform-guide/configuration.md): enable and configure platform components
