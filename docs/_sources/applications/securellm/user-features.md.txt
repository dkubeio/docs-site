# Core Features

Once you log in, the top menu shows four pages available to every user: **Dashboard**, **API Keys**, **Models**, and **Usage**.

## Dashboard

The Dashboard gives you a snapshot of your AI usage at a glance.

![SecureLLM Dashboard in the admin view: Total Requests, Input Tokens, Output Tokens and Total Cost cards above the By Provider and By Model tables](./media/screenshot-1.png)

- **Total Requests** — how many AI calls you have made
- **Input / Output Tokens** — a measure of how much text was sent and received (tokens ≈ words)
- **Total Cost** — estimated spend based on your requests
- **By Provider / By Model** — tables showing which AI services and models you used most

:::{note}
If you have admin access, the Dashboard shows usage for your entire organization, not just your own.
:::

## API Keys

An API key is like a password that lets an application (a script, a tool, or an IDE plugin) talk to SecureLLM on your behalf. You create keys here and paste them into whichever tool needs them.

**Creating a key:**

1. Click **API Keys** in the top menu.
2. Find the **Create New Key** card.
3. Enter a descriptive name in **Key Name** (e.g., `my-vscode-plugin` or `data-pipeline`).
4. Click **+ Create Key**.
5. **Copy the key immediately** — it is only shown once. Store it somewhere safe (a password manager or `.env` file).

**Revoking a key:**

1. Find the key in your list.
2. Click **Revoke**.
3. Confirm the action.

:::{tip}
If you suspect a key has been leaked or is no longer needed, revoke it right away. Revoking a key instantly stops any further requests made with it.
:::

## Models

The Models page lists every AI model available to you through SecureLLM: "Unique models across all configured providers. When multiple providers expose the same model it appears once, with all providers listed."

![SecureLLM Models page: Unique Models, Providers and Chat cards, the Search models box with the All providers and All categories filters, and the Chat group listing each model ID with its provider chips and price per 1M tokens](./media/securellm-models.png)

- Cards at the top show the number of **Unique Models**, **Providers**, and models per category (for example **Chat**).
- Use **Search models…** to find a specific model by name.
- Use the **All providers** and **All categories** filters to narrow the list (e.g., Chat, Reasoning, Embedding). Models are grouped by category, each group with its model count.
- Each row shows the **Model ID**, a chip for each provider that serves it (for example `dkubex/qwen2-5-7b-instruct`), and the **Price per 1M tokens (input / output)**.
- Click the **copy icon** on a provider chip to copy the model's identifier — paste this directly into your code or tool.

:::{note}
If an admin has restricted your access, you will only see the models and providers your organization has made available to you.
:::

## Usage (my requests)

The **Usage** menu item opens the **Usage Logs** page, which shows your request history — everything you or your keys have sent to SecureLLM.

![Request Detail modal](./media/screenshot-2.png)

- Use the **filters** at the top to narrow by provider, status, date and more, or type a model or API key name in **Search**.
- Click any row to open the **Request Detail** panel, which shows:
  - The exact messages sent and the AI's response
  - Request status, cost, token counts, and latency
  - Any guardrail events triggered by that request
