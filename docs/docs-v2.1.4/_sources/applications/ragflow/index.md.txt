# RAGFlow

RAGFlow on DKubeX is a retrieval-augmented generation (RAG) engine built on deep document understanding. It turns your documents into searchable knowledge bases and lets you chat with them, returning truthful answers backed by citations from your own data. On DKubeX, RAGFlow is pre-integrated with platform single sign-on and with cluster-local chat, embedding, and rerank models served through **SecureLLM** — so the built-in DKubeX model provider is preconfigured with your DKubeX credentials and ready to use out of the box.

## Key features

- **Knowledge bases** — Upload documents, parse them with configurable parsers and chunking, and run retrieval tests to tune quality.
- **Chat assistants** — Ground a chat on one or more knowledge bases and get answers with citations back to the source.
- **DKubeX models** — Chat, embedding, and rerank models from the built-in DKubeX provider, backed by SecureLLM. No external API keys.
- **Agents** — Build multi-step agents on top of your knowledge bases.
- **Team & sharing** — Share knowledge bases, assistants, agents, and models with your team.
- **Platform SSO** — Automatically signed in via DKubeX; no separate RAGFlow login.

## Tutorials

- [Getting started](./getting-started.md) — Sign in, connect the DKubeX model provider, and build your first knowledge base and chat.
- [Using models on DKubeX](./models.md) — Add the built-in DKubeX provider and set your default models.
- [Knowledge bases](./knowledge-bases.md) — Create and tune datasets: parsing, chunking, metadata, and retrieval testing.
- [Chat](./chat.md) — Create chat assistants and configure their behavior.
- [Agents](./agents.md) — Build an agent on top of your knowledge bases.
- [Team & sharing](./team-and-sharing.md) — Share your work with teammates.

```{toctree}
:hidden:

getting-started
models
knowledge-bases
chat
agents
team-and-sharing
```
