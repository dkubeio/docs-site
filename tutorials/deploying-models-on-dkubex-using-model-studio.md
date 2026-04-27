# Deploying Models on DKubeX Using Model Studio

This page combines the main DKubeX Model Studio deployment flows for both Large Language Models (LLMs) and machine learning (ML) models.

Model Studio supports discovering models from HuggingFace, deploying them through a guided form, and validating them in Playground.

## Shared Deployment Lifecycle

Both LLM and ML deployments follow the same platform lifecycle:

Pending -> Downloading -> Starting -> Running

Use the Deployed Models page to monitor status, edit resources, scale replicas, and manage model scope (Private/Shared).

## Deploying LLM Models

Use this flow for text-generation and instruction-following models, such as Qwen/Llama-class chat models.

### Prerequisites

- DKubeX workspace access with Model Studio enabled.
- Cluster resource profile for the model size you plan to run.
- Access to the HuggingFace model card you want to deploy.

### Deployment Process

1. Open Model Studio and go to Catalog.
2. Set Task to Text Generation.
3. Search for your model, such as a Qwen2-family model.
4. Click Deploy on the model card.
5. In the deploy form, configure:
   - Quantization, for example Q4_K_M for a smaller footprint
   - Resource Profile, such as a CPU or GPU preset
   - Replicas, usually starting with 1
   - Scope, either Private or Shared
6. Submit the deployment.
7. Track status in Deployed Models or Dashboard until the model reaches Running.

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

## Deploying ML Models

Use this flow for task-oriented ML inference models where the output is not long-form chat generation.

### Typical ML Tasks

- Embeddings
- Reranking
- Speech Recognition (ASR)

### Prerequisites

- DKubeX workspace access with Model Studio enabled.
- A suitable resource profile in the cluster.
- A HuggingFace model that matches the target task.

### Deployment Process

1. Open Model Studio and go to Catalog.
2. Choose the relevant Task filter:
   - Embeddings
   - Reranking
   - Speech Recognition
3. Pick a model and click Deploy.
4. In the deploy form, set:
   - Precision or quantization, as applicable
   - Resource Profile
   - Replicas
   - Scope, either Private or Shared
5. Submit the deployment.
6. Wait for status to reach Running.

### Validate by Task in Playground

Use Open Playground from Deployed Models and validate according to task type:

- Embeddings: run sample text and verify vector output is returned.
- Reranking: provide a query and passages and verify ranked ordering.
- Speech to Text: upload audio and verify transcript output.

### Operate and Scale

- Scale up replicas for higher throughput.
- Resize the resource profile for latency or memory improvements.
- Promote the model to Shared when team-wide reuse is needed.
- Delete deployments that are no longer serving traffic.

### LLM vs ML Deployment Differences

| Area | LLM Flow | ML Flow |
| --- | --- | --- |
| Primary task | Text generation and chat | Embeddings, reranking, and ASR |
| Primary validation | Chat response quality | Task-specific functional output |
| Typical optimization | Prompt latency and context handling | Throughput, ranking, and embedding quality |

### Troubleshooting

- Wrong output type in Playground: confirm the deployed model task matches the selected tab.
- No model in selector: ensure model status is Running and the tab supports that feature.
- Poor latency: increase profile resources or reduce replica contention.
