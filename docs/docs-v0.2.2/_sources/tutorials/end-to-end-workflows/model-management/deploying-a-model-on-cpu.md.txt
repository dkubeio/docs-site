# Deploying a Model on CPU

Deploy a language model that runs on CPU using Model Studio's **LLM Catalog**. The CPU path uses the
**Ollama** engine with a quantized GGUF model, so it runs without a GPU.

## Prerequisites

- Access to **Model Studio**.
- A CPU resource profile — the built-in **`cpu`** profile works, or create one (see
  [Deploying a Model on GPU](deploying-a-model-on-gpu.md#create-a-resource-profile) for the profile
  form; set GPU **Count** to 0 for a CPU profile).

## Steps

1. In Model Studio, open **LLM Catalog**.
2. Find a model — browse **Trending / Most Downloaded / Recent**, or search HuggingFace (or paste a
   `author/model` slug). Choose a small instruct model for a first deployment.
3. Click the model card, then click **Deploy**.
4. On the **Deploy** tab of the dialog:
   | Field | Set to |
   |---|---|
   | **Deployment Name** | Leave blank to use the model's slug, or enter your own. |
   | **Inference Engine** | **Ollama** (GGUF models, CPU-friendly). |
   | **GGUF Repository** | The auto-detected GGUF repo (required for Ollama). |
   | **Quantization** | A GGUF quantization — **Q4_K_M** is a good default. |
   | **Resource profile** | Leave the **Use GPU** toggle **off** and pick a CPU profile (for example `cpu` with a count). |
   | **Replicas** | Set **Min** and **Max** (start with 1 and 1). |
5. Click **Deploy**.
6. Open **LLM Models** and wait for the model's status to become **Running**.

## Next steps

- [Test the model in the Playground](testing-a-model-in-the-playground.md).
- To run a larger model or speed up inference, [deploy on GPU](deploying-a-model-on-gpu.md).
