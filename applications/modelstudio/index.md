# ModelStudio

ModelStudio is a web application for discovering, deploying, and running inference on AI models in the DKubeX platform. It supports three model tracks — large language models via [KubeAI](https://github.com/kubeai-project/kubeai) or NVIDIA Dynamo, traditional machine-learning models via [KServe](https://kserve.github.io/website/), and production-optimized [NVIDIA NIM](https://docs.nvidia.com/nim/) microservices — all browsable, deployable, and testable from a single interface.

## Key features

- Browse and deploy LLM models from HuggingFace Hub with one click.
- Deploy ML models (sklearn, XGBoost, PyTorch, etc.) from an MLflow registry or HuggingFace via KServe.
- Register and run NVIDIA NIM models in-cluster on GPU nodes via the k8s-nim-operator.
- Unified Playground for chat, vision, embeddings, reranking, speech-to-text, text-to-speech, and image generation.
- Client-side document RAG with PDF, DOCX, TXT, and MD support — documents never leave your browser.
- Real-time model status, resource-profile management, and an activity log of every deploy/undeploy action.

## Guides

- [Getting started](./getting-started.md) — an overview of every page.
- [Workflows](./tutorials.md) — deploy your first LLM, ML, and NIM model, step by step.
- [Deploying models](./deploying-models.md) — LLM, ML, and NIM deployment paths in depth.
- [Playground guide](./playground.md) — every inference mode walked through end-to-end.

## At a glance

| Page | What it does |
|---|---|
| Dashboard | The landing page: model counts, models by type, a model status table, and recent activity |
| LLM Catalog | Browse HuggingFace, NVIDIA NIM, and local models and deploy LLM models directly |
| LLM Deployments | A table of the deployed LLM models; open one to see its details and actions |
| Playground | A unified inference workbench for testing your deployed LLM models |
| ML Registry | Browse and deploy ML models (non-LLM); only visible when KServe is enabled |
| ML Deployments | A table of your deployed KServe InferenceServices; only visible when KServe is enabled |
| Resource Profiles | Create, edit, and delete custom resource configurations (CPU, memory, GPU) to load into the deploy forms, and view the bundled KubeAI profiles |
| Settings | Your HuggingFace and NVIDIA NIM tokens (per user) and the shared model cache (global) |

```{toctree}
:hidden:

getting-started
tutorials
deploying-models
playground
```
