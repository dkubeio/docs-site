# ModelStudio

ModelStudio is a web application for discovering, deploying, and running inference on AI models in the DKubeX platform. It supports three model tracks — large language models via [KubeAI](https://github.com/substratusai/kubeai), traditional machine-learning models via [KServe](https://kserve.github.io/website/), and production-optimized [NVIDIA NIM](https://docs.nvidia.com/nim/) microservices — all browsable, deployable, and testable from a single interface.

## Key features

- Browse and deploy LLM models from HuggingFace Hub with one click.
- Deploy ML models (sklearn, XGBoost, PyTorch, etc.) from an MLflow registry or HuggingFace via KServe.
- Register and run NVIDIA NIM models in-cluster on GPU nodes via the k8s-nim-operator.
- Unified Playground for chat, vision, embeddings, reranking, speech-to-text, text-to-speech, and image generation.
- Client-side document RAG with PDF, DOCX, TXT, and MD support — documents never leave your browser.
- Real-time model status, resource-profile management, and an activity log of every deploy/undeploy action.

## Tutorials

- [Getting started](./getting-started.md) — an overview of every page.
- [Workflows](./tutorials.md) — deploy your first LLM, ML, and NIM model, step by step.
- [Deploying models](./deploying-models.md) — LLM, ML, and NIM deployment paths in depth.
- [Playground guide](./playground.md) — every inference mode walked through end-to-end.

```{toctree}
:hidden:

getting-started
tutorials
deploying-models
playground
```
