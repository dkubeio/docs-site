# Deploying a Model on Multiple GPUs on the Same Host

A large model that does not fit on a single GPU can be deployed across several GPUs on one node in
Model Studio. This takes **two settings**, and you set **both**:

1. A **resource profile** that requests **N GPUs** — this places N GPUs on a single node for the
   deployment.
2. One **vLLM argument** on the deployment that tells the model to use all N GPUs.

Keep **replicas at 1** — replicas are separate copies of the model, which is not what you want here.

## Prerequisites

- Access to **Model Studio**.
- A node with **N GPUs** available.

## Step 1 — Create a resource profile with N GPUs

1. In Model Studio, open **Resource Profiles** → **New Profile**.
2. Set:
   | Field | Set to |
   |---|---|
   | **Profile Name** | e.g. `2x-gpu`. |
   | **Use for** | **LLM (HuggingFace)** (or **Both**). |
   | **CPU / Memory** | Request values appropriate for the model. |
   | **GPU → GPU Type** | `NVIDIA GPU (nvidia.com/gpu)`. |
   | **GPU → Count** | **N** — the number of GPUs the model is deployed on (e.g. `2`, `4`). |
   | **GPU node target** *(optional)* | Pin the node type if the cluster has mixed GPU hardware. |
3. Click **Save Profile** (KubeAI restarts briefly).

## Step 2 — Deploy across the GPUs

1. Open **LLM Catalog**, select the model → **Deploy**.
2. On the **Deploy** tab, set **Inference Engine** to **vLLM**, turn **Use GPU** on, and select the
   profile you created. Keep **Min/Max replicas = 1**.
3. Open the **Advanced** tab → **Additional args**.
4. Add the following vLLM argument, setting the value to your GPU count (**N**):
   ```
   --tensor-parallel-size=2
   ```
   This is an internal vLLM parameter that makes the model use all N GPUs in the profile.
5. Click **Deploy**.
6. Open **LLM Models** and wait for **Running**.

:::{note}
The profile's GPU **count** decides how many GPUs the deployment gets (all on one node); the argument
in Step 2 makes the model actually use all of them. Set both, or the extra GPUs sit idle.
:::
