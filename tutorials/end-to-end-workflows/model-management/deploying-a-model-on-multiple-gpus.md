# Deploying a Model on Multiple GPUs on the Same Host

Large models that don't fit on one GPU can be sharded across several GPUs on a **single host**. This
takes **two settings**, and you must set **both**:

1. **Request N GPUs in one pod** — via the resource profile. Because one pod is scheduled onto one node,
   requesting N GPUs places all N on the **same host**.
2. **Tell vLLM to shard across them** — add the `--tensor-parallel-size=N` engine argument. This is
   **not** added automatically.

Keep **replicas at 1** — replicas are separate pods that may land on different hosts, which is not what
you want here.

## Prerequisites

- Access to **Model Studio**.
- A host with **N GPUs** available.

## Step 1 — Create a multi-GPU resource profile

1. In Model Studio, open **Resource Profiles** → **New Profile**.
2. Set:
   | Field | Set to |
   |---|---|
   | **Profile Name** | e.g. `2x-gpu`. |
   | **Use for** | **LLM (HuggingFace)** (or **Both**). |
   | **CPU / Memory** | Request values appropriate for the model. |
   | **GPU → GPU Type** | `NVIDIA GPU (nvidia.com/gpu)`. |
   | **GPU → Count** | **N** — the number of GPUs (e.g. `2`, `4`). |
   | **GPU node target** *(optional)* | Pin the node type if the cluster has mixed GPU hardware. |
3. Click **Save Profile** (KubeAI restarts briefly).

Alternatively, use a built-in GPU profile at a count of N — the deploy dialog lists built-in GPU
profiles at each available count.

## Step 2 — Deploy with tensor parallelism

1. Open **LLM Catalog**, select the model → **Deploy**.
2. On the **Deploy** tab, set **Inference Engine** to **vLLM**, turn **Use GPU** on, and select your
   multi-GPU profile. Keep **Min/Max replicas = 1**.
3. Open the **Advanced** tab → **Additional args**.
4. Add the tensor-parallel argument, matching N to your GPU count:
   ```
   --tensor-parallel-size=2
   ```
   For very large models you can add pipeline parallelism as well: `--pipeline-parallel-size=2`.
5. Click **Deploy**.
6. Open **LLM Models** and wait for **Running**.

:::{note}
The GPU **count** sets how many GPUs the pod gets (co-located on one host); `--tensor-parallel-size`
tells vLLM to actually split the model across them. If you set the profile count but omit the argument,
the extra GPUs sit idle.
:::
