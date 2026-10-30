# Getting Started

RAGFlow on DKubeX turns your documents into knowledge bases you can chat with. This guide takes you from signing in to your first answer.

## Sign in

RAGFlow uses DKubeX single sign-on. Open the app from your DKubeX dashboard and you are signed in automatically with your existing credentials — no separate RAGFlow login.

## Set up the DKubeX model provider

RAGFlow needs models to embed your documents and generate answers. On DKubeX these come from the built-in **DKubeX** provider, backed by SecureLLM.

1. Click your avatar in the top-right and open the **Model providers** page.
2. Find the **DKubeX** provider, start its setup, paste your **SecureLLM API key**, and confirm. RAGFlow registers the chat, embedding, and rerank models your key permits.
3. Open **Set Default Models** and choose your default chat and embedding models.

See [Using models on DKubeX](./models.md) for details.

## Create your first knowledge base

1. Create a dataset.
2. On its **Configuration** page, choose a **chunking method** (for example, **General**) and your **embedding model**.
3. Upload one or more documents and **parse** them.
4. Optionally run a [retrieval test](./knowledge-bases.md#run-a-retrieval-test) to confirm the right chunks come back.

See [Knowledge bases](./knowledge-bases.md) for the full set of parsing and tuning options.

## Start a chat

1. Click the **Chat** tab, then **Create an assistant**.
2. Give the assistant a name and select the dataset you just created.
3. Keep **Show quote** enabled so answers cite their sources, and start chatting.

See [Chat](./chat.md) for all assistant settings.

## Next steps

- [Build a document Q&A assistant](./build-a-qa-assistant.md) — the full workflow, end to end.
- [Agents](./agents.md) — build multi-step agents on top of your knowledge bases.
- [Team & sharing](./team-and-sharing.md) — share your work with teammates.
