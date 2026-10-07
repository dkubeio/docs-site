# Deploying a Model on GPU

Deploy a language model on a GPU using Model Studio. GPU deployments use the **vLLM** engine with a
**GPU resource profile**. The GPU is requested entirely through the resource profile you select.

## Prerequisites

- Access to **Model Studio**.
- At least one GPU node in the cluster.
- A GPU resource profile — a built-in `nvidia-gpu-*` profile, or a custom one (below).

## Deploy the model

1. In Model Studio, open **LLM Catalog** and select a model → **Deploy**.
2. On the **Deploy** tab:
   | Field | Set to |
   |---|---|
   | **Deployment Name** | Optional. |
   | **Inference Engine** | **vLLM** (Safetensors · GPU required). |
   | **Resource profile** | Turn the **Use GPU** toggle **on**, then pick a GPU profile (for example `nvidia-gpu-l4`, `nvidia-gpu-a100-80gb`). Selecting vLLM auto-selects the first GPU profile. |
   | **Replicas** | Set **Min** and **Max**. Set **Min = 0** to enable scale-to-zero (the model scales down when idle and scales back up on the next request). |
3. Click **Deploy**.
4. Open **LLM Models** and wait for **Running** (or **Scaled-to-zero** if Min replicas is 0 and it is
   idle).

(create-a-resource-profile)=
## Create a resource profile

Resource profiles are reusable CPU / memory / GPU shapes. Built-in profiles are read-only; create your
own on the **Resource Profiles** page.

1. In Model Studio, open **Resource Profiles** → **New Profile**.
2. Fill in the form:
   | Field | Set to |
   |---|---|
   | **Profile Name** *(required)* | A name, e.g. `l4-single-gpu`. |
   | **Use for** | **LLM (HuggingFace)** for KubeAI deployments (or **Both**). |
   | **CPU** | Request (and optional Limit). |
   | **Memory** | Request (and optional Limit) — case-sensitive units (`4Gi`, not `4gi`). |
   | **GPU → GPU Type** | `NVIDIA GPU (nvidia.com/gpu)`. |
   | **GPU → Count** | Number of GPUs (**0** = no GPU; **1** for a single GPU). |
   | **GPU node target** *(optional)* | Leave blank to use any GPU node, or pin an instance type (e.g. `g5.4xlarge`) or GPU product (e.g. `NVIDIA-A10G`). |
3. Click **Save Profile**. Saving briefly restarts KubeAI (~10 seconds) to pick up the new profile.

The profile then appears in the deploy dialog under **My profiles**.

## Next steps

- To shard one model across several GPUs, see
  [Deploying a Model on Multiple GPUs](deploying-a-model-on-multiple-gpus.md).
- [Test the model in the Playground](testing-a-model-in-the-playground.md).
