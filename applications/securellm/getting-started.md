# Getting Started

SecureLLM is your organization's secure gateway to AI — one central hub that all AI requests pass through. This guide covers logging in and creating your first API key.

## Logging in

SecureLLM uses your company's single sign-on (SSO). Navigate to the app URL and you are logged in automatically using your existing credentials — no separate account or password needed.

Once logged in, you will see a menu across the top of the page with four pages: **Dashboard**, **API Keys**, **Models**, and **Usage**. Administrators see additional pages, some of them under **More** — see [Administrator features](./admin-features.md).

## Creating your first API key

An API key is like a password that lets an application (a script, a tool, or an IDE plugin) talk to SecureLLM on your behalf. You create keys here and paste them into whichever tool needs them.

1. Click **API Keys** in the top menu.
2. Find the **Create New Key** card.
3. Enter a descriptive name in **Key Name** (e.g., `my-vscode-plugin` or `data-pipeline`).
4. Click **+ Create Key**.
5. **Copy the key immediately** — it is only shown once. Store it somewhere safe (a password manager or `.env` file).

:::{tip}
If you suspect a key has been leaked or is no longer needed, revoke it right away from the **API Keys** page. Revoking a key instantly stops any further requests made with it.
:::

## Next steps

- Explore the [core features](./user-features.md) available to every user.
- Follow an [end-to-end workflow](./tutorials.md) to set things up.
