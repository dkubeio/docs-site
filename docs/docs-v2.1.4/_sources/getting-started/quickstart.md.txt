# Quickstart

This quickstart takes you from a fresh login to chatting with a live model in a few minutes. It
assumes DKubeX is already [installed](installation.md) and that an administrator has given you access
to **ModelStudio**.

By the end you will have logged in, deployed a language model onto the cluster, and sent it a prompt.

## 1. Log in

1. Open your DKubeX platform URL in a browser.
2. On the login page, sign in with your credentials — either **email and password**, or **Sign in with
   GitHub** if your organization uses OAuth.
3. You land on your dashboard. The **Work** section lists the applications assigned to you.

You are now authenticated across every DKubeX application through single sign-on — you will not be
asked to log in again when you open an app.

## 2. Open ModelStudio

Click the **ModelStudio** tile in your **Work** section. It opens in place, already authenticated.

ModelStudio is where you discover, deploy, and run inference on models. For this quickstart you will
deploy a small language model from the LLM Catalog.

## 3. Deploy a model

1. Go to the **LLM Catalog**.
2. Browse the **Trending** or **Most Downloaded** tabs, or search HuggingFace for a small
   text-generation model (a compact instruct model is a good first choice).
3. On the model card, click **Deploy** to open the deployment form.
4. Choose a **resource profile** that fits the model, then confirm the deployment.
5. Watch the model in **LLM Models** — it moves through its status states until it is **Running**.

:::{tip}
Start with a small model the first time. Larger models need more memory or a GPU node, and take
longer to pull and start. See [Architecture & Specifications](../platform-guide/architecture-and-specifications.md#system-requirements)
for sizing guidance.
:::

## 4. Chat with it

1. Open the **Playground**.
2. Select your deployed model from the dropdown at the top.
3. On the **Chat** tab, type a message and press **Enter** (or click **Send**).
4. The response streams back in real time, with token usage shown beneath it.

That's the full path — login, deploy, inference — on your own cluster.

## Where to go next

- **[Platform Overview](platform-overview.md)** — understand how the pieces you just used fit together.
- **[ModelStudio](../applications/modelstudio/index.md)** — the complete guide to deploying and running models.
- **[Tutorials](../tutorials/index.md)** — end-to-end workflows for RAG, model governance, MLOps, and coding agents.
