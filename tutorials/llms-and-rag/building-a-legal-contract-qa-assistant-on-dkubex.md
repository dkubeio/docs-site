# Building a Legal Contract Q&A Assistant on DKubeX

This tutorial shows how to build a document Q&A assistant on DKubeX. You deploy a chat model
and an embedding model in **Model Studio**, expose them through the **SecureLLM** gateway, and
use them in **RAGFlow** to turn a set of documents into a chat assistant that answers questions
with citations.

The example corpus is a set of non-disclosure agreements (the
[ContractNLI](https://stanfordnlp.github.io/contract-nli/) dataset), but any set of documents
works the same way.

## Prerequisites

- A DKubeX 2.0 deployment with the **Model Studio**, **SecureLLM**, and **RAGFlow** applications
  installed. To add an application, a user requests access to it from the dashboard's **Add app**
  section, and an administrator approves the request.
- The documents you want to query, downloaded and unzipped **on your computer** — RAGFlow uploads
  files from your local machine. For this example, download the ContractNLI dataset
  ([direct download](https://stanfordnlp.github.io/contract-nli/resources/contract-nli.zip) —
  from the [dataset download page](https://stanfordnlp.github.io/contract-nli/#download)) and
  unzip it on your computer.

## Step 1 — Deploy the models in Model Studio

RAGFlow needs two models: a **chat** model to write answers and an **embedding** model to index
and retrieve document chunks. Deploy both in Model Studio.

1. Open **Model Studio**.
2. Go to **Resource Profiles** and create a profile for the deployment. For better extraction and
   query quality, a **GPU** profile is recommended.
3. Go to **LLM Catalog**, search for a chat model (for example, `qwen2-5-7b-instruct`), and click
   **Deploy**. Select your resource profile, then deploy.
4. Deploy an **embedding model** the same way (for example, `jina-embeddings-v3`).
5. Track both under **LLM Models** until each reaches the running state.

## Step 2 — Connect the models in RAGFlow

RAGFlow reaches the models through the SecureLLM gateway using your default DKubeX user key, so
every model you have access to appears automatically.

1. Open **RAGFlow**, click the profile icon in the top-right, and open **Model Providers**.
2. On the **DKubeX** provider, the models you have access to are listed automatically. Assign each
   one a type and adjust the max-token limits if needed, then **Save**. For example:

   | Model | Type |
   | --- | --- |
   | `qwen2-5-7b-instruct` | chat |
   | `jina-embeddings-v3` | embedding |

3. In the **Set Default Models** section on the same page, choose your default **LLM**
   (`qwen2-5-7b-instruct`) and **Embedding** (`jina-embeddings-v3`) model.

> **Note:** All requests routed through the models are recorded by SecureLLM and can be monitored in
> its **Usage** tab.

## Step 3 — Create the knowledge base

1. Go to **Dataset** and create a dataset. Give it a name.
2. On the dataset's **Configuration**, confirm the **embedding model** and choose a document
   parser:
   - **Naive** — fast text extraction; a good fit for clean, digital documents.
   - **DeepDoc** — runs OCR, table, and layout recognition for better results on scanned or
     layout-heavy documents, but is slower.
3. Open **Upload file**, choose the **Files** or **Folder** tab, and drag and drop your documents
   from your computer. Enable **Parse on creation** in the upload dialog to start parsing on
   upload. Otherwise, once the upload completes, select the uploaded documents and click **Parse**
   to start parsing.
4. When parsing completes, open a file to review its **chunks**.

## Step 4 — Create the chat assistant

1. Go to **Chat** and click **Create chat**. Give the assistant a name.
2. In **Chat setting**, configure:
   - **Datasets** — select the dataset you created.
   - **System prompt** — the system prompt used by the chat application. You can keep the default
     or provide your own. If your prompt includes the `{knowledge}` variable, enable that variable
     in the settings. See the example prompt below.
   - **Similarity threshold** — `0.2` by default.
   - **Vector similarity weight** — `0.3` by default.
   - **Top N** — `8` by default; set it to `3`–`5` for better results.
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
