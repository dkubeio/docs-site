# Building a Legal Contract Q&A Assistant on DKubeX

This tutorial shows how to build a document Q&A assistant on DKubeX. You deploy a chat model
and an embedding model in **Model Studio**, route all requests and responses through the
**SecureLLM** gateway, and use them in **RAGFlow** to turn a set of documents into a chat assistant
that answers questions with citations.

The example corpus is a set of non-disclosure agreements (the
[ContractNLI](https://stanfordnlp.github.io/contract-nli/) dataset), but any set of documents
works the same way.

## Prerequisites

- A DKubeX deployment with the **Model Studio**, **SecureLLM**, and **RAGFlow** applications
  installed. To add an application, a user requests access to it from the dashboard's **Add app**
  section, and an administrator approves the request.
- The documents you want to query, downloaded and unzipped **on your computer** — RAGFlow uploads
  files from your local machine. For this example, download the ContractNLI dataset
  ([direct download](https://stanfordnlp.github.io/contract-nli/resources/contract-nli.zip) —
  from the [dataset download page](https://stanfordnlp.github.io/contract-nli/#download)) and
  unzip it on your computer.

## Step 1 — Deploy the models in Model Studio

RAGFlow needs two models: a **chat** model to write answers and an **embedding** model to index
and retrieve document chunks. Deploy both in Model Studio, each on a **GPU** resource profile for
good extraction and query quality.

1. In **Model Studio**, deploy a **chat** model (this example uses `qwen3-8b`).
2. Deploy an **embedding** model the same way (this example uses `bge-m3`).
3. Wait until both reach the **running** state under **LLM Models**.

For the full deployment walkthrough — creating a resource profile, choosing the inference engine,
and setting deployment arguments — see
[Deploying Models on DKubeX Using Model Studio](./deploying-models-on-dkubex-using-model-studio.md).

## Step 2 — Connect the models in RAGFlow

RAGFlow reaches the models through the SecureLLM gateway using your default DKubeX user key, so
every model you have access to appears automatically.

1. Open **RAGFlow**, click the profile icon in the top-right, and open **Model Providers**.
2. In the **Available models** column on the right, find the built-in **DKubeX** provider and click
   **Add**. The chat and embedding models you deployed in Model Studio are registered automatically.
3. In the **Set default models** column, select the models you just added:
   - **LLM** — your chat model (`qwen3-8b`)
   - **Embedding** — your embedding model (`bge-m3`)

## Step 3 — Create the knowledge base

1. Go to **Dataset** and create a dataset. Give it a name (for example, `legal-contracts`), select
   your **embedding model** (`bge-m3`), and choose a **chunking method** (**General** works well for
   these contracts). Save to create the empty dataset.
2. Open the dataset's **Configuration** and set the **PDF parser**. Select **Naive** — fast text
   extraction that suits clean, digital documents. Save.
3. Open the **Files** tab, click **+ Add file**, and drag and drop your documents from your
   computer. Enable **Parse on creation** so ingestion starts as soon as the files finish
   uploading, then **Save**. Otherwise, select the uploaded files and click **Parse**.
4. When parsing completes, open a file to review its **chunks**.

## Step 4 — Create the chat assistant

1. Go to **Chat** and click **Create chat**. Name the assistant (for example, `legal-chat`), then
   open its settings.
2. In **Chat setting**, configure:
   - **Datasets** — select the dataset you created (`legal-contracts`).
   - **System prompt** — the system prompt used by the assistant. Keep the default or provide your
     own (see the example below). If your prompt includes the `{knowledge}` variable, scroll down
     and **enable that variable** so retrieved chunks are injected as context.
3. **Save**, then ask questions in the chat. Each answer cites the document chunks it used.

Example system prompt:

```text
You are a retrieval-augmented generation (RAG) assistant.

CRITICAL RULES (MUST FOLLOW):
1. You may ONLY use information that is EXPLICITLY stated in the <context>.
2. You MUST NOT use prior knowledge, assumptions, or general world knowledge.
3. If the <context> does NOT contain enough information to fully and directly answer the question,
   you MUST respond with EXACTLY:
   "I can't answer this question from the provided context."
4. This refusal response MUST be the only output in that case.
5. Do NOT explain why you cannot answer.
6. Do NOT partially answer.
7. Do NOT infer, guess, or extrapolate beyond the context.

PROCESS (INTERNAL - DO NOT OUTPUT):
Step 1: Determine whether the question can be answered using ONLY the context.
Step 2:
- If YES → Answer using ONLY context information.
- If NO → Output the exact refusal sentence.

CITATION RULES:
- Do NOT cite if no id is provided.
- Do NOT fabricate citations.

FORMAT RULES:
- Use Markdown formatting.
- Use headings, lists, and code blocks where appropriate.
- Do NOT use XML tags in the output.

<context>
'{knowledge}'
</context>
```

## Step 5 — Try some questions

Ask a few questions in the chat and check that each answer cites specific legal contracts:

1. What are personal and confidential information?
2. Briefly explain what a termination clause is.
3. What is a non-circumvention and non-disclosure agreement?
4. How do I frame a confidential information clause?
5. What is the difference between a unilateral and mutual NDA?
6. What are some common exceptions to confidential information clauses?

## Step 6 — Monitor usage in SecureLLM

Every request the assistant makes is routed through SecureLLM and recorded there.

1. Open the **SecureLLM** app from your workspace.
2. Go to the **Usage** tab to review the requests you have made. Each entry shows the prompt, the
   question, the answer, and metrics such as token usage.
