# Build a Document Q&A Assistant

This end-to-end walkthrough chains the steps from [Using models on DKubeX](./models.md), [Knowledge bases](./knowledge-bases.md), and [Chat](./chat.md) into one workflow: turning a set of documents into a chat assistant that answers questions with citations.

## 1. Set up your models

1. Open the **Model providers** page (avatar → **Model providers**).
2. Set up the **DKubeX** provider with your **SecureLLM API key**, then open **Set Default Models** and choose your default chat and embedding models.

## 2. Create and populate a knowledge base

1. Create a dataset.
2. On its **Configuration** page, select a **chunking method** that suits your files (for example, **General**) and confirm your **embedding model**. For PDFs with formatted or image-based text, choose an appropriate **PDF parser** such as **DeepDoc**; for plain-text PDFs, **Naive** is faster.
3. Upload your documents and **parse** them.
4. Optionally, open a parsed file to review its chunks and add keywords or questions to improve how they are retrieved.

## 3. Verify retrieval

Before wiring up a chat, run a retrieval test so you know the right chunks come back:

1. Go to the dataset's **Retrieval testing** page.
2. Enter a representative question in **Test text** and click **Testing**.
3. If the results are off, adjust the **Similarity threshold** (default 0.2) and **Vector similarity weight** (default 0.3), and rerun.

## 4. Create the chat assistant

1. Click the **Chat** tab, then **Create an assistant**.
2. Under **Assistant settings**, name the assistant and select your dataset. Keep **Show quote** enabled so answers cite their sources.
3. To confine answers to your documents, set an **Empty response**; leave it blank to let the model improvise when nothing is retrieved.
4. Under **Model settings**, pick your chat model and a **Creativity** preset (**Precise** is a good default for factual Q&A).
5. Save and start asking questions. Each answer cites the chunks it used.

## 5. Iterate

If answers are weak, return to the knowledge base and tune it — adjust the chunking method, add metadata or tag sets, or re-run retrieval tests — then refine the assistant's prompt and retrieval settings until the answers are accurate and well-cited.
