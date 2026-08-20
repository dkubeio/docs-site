# Deploying Models on DKubeX Using Model Studio

This page walks through deploying models on DKubeX using Model Studio. Text-generation, embedding, and reranking models all use the same LLM deployment flow.

Model Studio supports discovering models from **HuggingFace** and **NVIDIA NIM**, deploying them through a guided form, and validating them in Playground.

```{raw} html
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;margin:1.5rem 0;border-radius:8px;">
  <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    src="https://www.youtube-nocookie.com/embed/ahTeYTSyPV8" title="Deploying Models on DKubeX Using Model Studio"
    loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
</div>
```

> 📺 Prefer to watch? See the walkthrough on YouTube: <https://youtu.be/ahTeYTSyPV8>

## Shared Deployment Lifecycle

Deployments follow this platform lifecycle:

Pending -> Downloading -> Starting -> Running

Use the **LLM Models** page to monitor status, edit resources, scale replicas, and manage model scope (Private/Shared).

## Deploying LLM Models

Use this flow for text-generation, embedding, and reranking models — it's the same whether you're deploying a chat model or the embedding model behind a RAG assistant.

### Prerequisites

- DKubeX workspace access with Model Studio enabled.
- Access to the HuggingFace or NVIDIA NIM model you want to deploy.

### Deployment Process

This walkthrough deploys `qwen3-8b` on a GPU; the same flow works for any LLM.

1. **Create a resource profile.** Because we're serving on a GPU, provision one first. From the top
   navigation, open **Resource Profiles** and click **New Profile**. Give the profile a name, set it
   to provision a single **GPU** instance, and pick your **instance type** (for example,
   `g5.4xlarge`). Leave the remaining settings at their defaults and click **Save Profile**.
2. Open the **LLM Catalog** and browse models from **HuggingFace** or **NVIDIA NIM**.
3. In the search bar, type the model you want — here, `qwen3-8b` — and click its card. A **Deploy
   Model** panel opens on the right.
4. On the **Deploy** tab, configure:
   - **Deployment Name** — a name for this deployment (leave blank to use the model's own name).
   - **Source Model ID** — the HuggingFace path used to pull the weights (for example,
     `Qwen/Qwen3-8B`).
   - **Inference Engine** — choose how you're serving the model: **vLLM** for GPU serving, or
     **Ollama** for CPU or quantized (GGUF) models.
   - **Resources** — make sure **Use GPU** is checked, then select the **resource profile** you
     created in step 1.
   - **Replicas** — usually start with 1.
   - **Scope** — either **Private** or **Shared**.
5. For finer control, open the **Advanced** tab and set engine parameters as needed:
   - **Max context length** — for example, `16384`.
   - **GPU memory utilization** — for example, `0.90`.
   - **Quantization** — leave at **none** for a full-precision vLLM deployment, or pick a method
     (for example, `Q4_K_M`) for a quantized GGUF model on Ollama.
   - **Data type**, **prefix caching**, and any **additional arguments** to pass to the engine.
6. Click **Deploy**. You're taken to the **LLM Models** page, where the deployment appears while
   DKubeX pulls the model into a shared cache — it downloads once and remounts instantly on future
   restarts. Wait until the status reaches **Running**.

### Inspect the Deployment

Once the model is **Running**, click it on the **LLM Models** page to open its details:

- **Overview** — the OpenAI-compatible endpoint URL you use to call the model.
- **Config** — the deployment's full configuration.
- **Pods** — the running pod and its status.
- **Logs** — the live serving logs.
- **Events** — everything that happened during scheduling and startup.

### Validate the Deployment

1. Open Playground from the deployed model row.
2. Go to Chat.
3. Send a short prompt and verify a streamed response.
4. Confirm token usage appears after the response completes.

### Operate the Model After Deployment

- Edit: update resource profile or replica count.
- Promote/Demote: move between Private and Shared scope.
- Delete: remove the deployment when it is no longer needed.

### Recommended Starting Configuration

| Model Size | Suggested Profile | Replicas | Notes |
| --- | --- | --- | --- |
| Small (1B to 3B) | CPU profile | 1 | Good for functional testing |
| Medium (7B to 8B) | GPU profile | 1 | Better latency and quality |
| Larger (13B+) | Larger GPU profile | 1 | Validate memory headroom before scaling |

### Troubleshooting

- Stuck in Downloading: verify outbound registry/network access and image pull status.
- Stuck in Starting: check resource profile capacity and pod scheduling.
- Failed: review model runtime logs and deployment events in the cluster.
