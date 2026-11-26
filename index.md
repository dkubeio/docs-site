---
og:description: "Documentation for DKubeX, a Kubernetes-native platform for deploying, managing and operating AI and ML applications from a single control plane."
myst:
  html_meta:
    description: "Documentation for DKubeX, a Kubernetes-native platform for deploying, managing and operating AI and ML applications from a single control plane."
---

# DKubeX 2.0 Documentation

*Version {{ doc_version }}*

DKubeX is a Kubernetes-native platform for deploying, managing, and operating AI and ML applications
from a single control plane. It layers a self-service application catalog, a governed model plane, and
integrated developer tooling over a standard Kubernetes cluster — so teams can run the full model
lifecycle, from training to governed inference, on their own infrastructure.

## Where to start

Administrators start with **Install and upgrade**, then **Administer DKubeX**. Once DKubeX is running and
an administrator has given you access, start with the **Quickstart** under **Get started**.

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Get started
:link: getting-started/index
:link-type: doc

What DKubeX is and how it fits together, the Quickstart to run your first model, and the Glossary.
:::

:::{grid-item-card} Install and upgrade
:link: install/index
:link-type: doc

For administrators: install DKubeX on your cluster with Helm, the hardware it needs, upgrade, and uninstall.
:::

:::{grid-item-card} Administer DKubeX
:link: platform-guide/index
:link-type: doc

Configuration, user and access management, the application catalog, workspaces, and licensing.
:::

:::{grid-item-card} Use DKubeX
:link: applications/index
:link-type: doc

User guides for Workspace, ModelStudio, MLflow, SecureLLM, RAGFlow, Langflow, and SRE.
:::

:::{grid-item-card} Tutorials and how-to guides
:link: tutorials/index
:link-type: doc

End-to-end workflows across model management, LLM governance, RAG, and MLOps — plus coding agents.
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc

The Helm values of the installer chart, and Troubleshooting: every known problem with a link to its fix.
:::

:::{grid-item-card} Release notes and support
:link: support/index
:link-type: doc

Every published version of these docs, and where to get help.
:::

::::

```{toctree}
:hidden:
:caption: Contents

getting-started/index
install/index
platform-guide/index
applications/index
tutorials/index
reference/index
support/index
```
