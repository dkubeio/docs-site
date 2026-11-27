# Administrator Features

:::{note}
Admin pages are only visible if your account has been granted admin access. Contact your SecureLLM administrator if you believe you should have admin rights.
:::

Admins see all four user pages (with organization-wide data) plus six additional pages: **Providers**, **Users**, **Guardrails**, **Guardrail Logs**, **Audit Logs**, and **Performance**.

## Dashboard (admin view)

Identical to the user dashboard, but all numbers reflect the **entire organization** — every user's requests, tokens, and costs. Use this to monitor overall AI spend and identify which teams or models drive the most usage.

## Providers

Providers are the AI services SecureLLM connects to (e.g., OpenAI, Anthropic, or your organization's own AI deployment).

**Adding a provider:**

1. Click **Providers** → **Add Provider**.
2. Select the provider type from the dropdown.
3. Enter the provider's **API Key** and, if needed, a custom **Base URL**.
4. Optionally list **Allowed Models** (leave blank to allow all models from this provider).
5. Click **Save**.

**Enabling / disabling a provider:**

Use the toggle switch on each provider card. Disabling pauses routing to that provider without losing its configuration — useful for maintenance or cost control. Only delete a provider when you are certain it will never be used again.

## Users

The Users page lets you set access policies for individual users — controlling which providers and models each person can use.

**Adding a restriction:**

1. Click **Users** → **Add Restriction**.
2. Enter the user's email or username.
3. Specify **Allowed Providers** and/or **Allowed Models** (comma-separated).
4. Click **Save**.

**Setting a spend limit:**

In the same form, enter a **Spend Limit (USD)** and choose how often it **Resets** (never, daily, weekly, every 30 days or monthly). The limit covers the cost of all requests made with the user's API keys. Once the user's spend in the current period reaches the limit, their chat, completion and embedding requests are rejected with a `400` "budget exceeded" error until the period resets, or until you raise the limit or tick **Reset spend to $0 now**. A request that starts under the limit is allowed to finish, so spend can end slightly above it. Leave the field empty for no limit.

To remove all restrictions and the spend limit from a user (giving them full access), click **Remove** next to their policy.

## Guardrails

Guardrails are automatic safety filters that inspect AI requests and responses before they reach the AI or your users.

**Three guardrail types:**

| Type | What it does |
|---|---|
| **Content Filter** | Blocks or masks sensitive content — credit card numbers, passwords, PII (names, phone numbers, etc.) |
| **Prompt Injection** | Detects attempts to manipulate the AI into ignoring its instructions (jailbreak attempts) |
| **Custom** | Advanced: accepts a raw JSON configuration for organization-specific rules |

**Enabling or disabling a guardrail:** Use the toggle switch on each guardrail card. Changes take effect immediately for all new requests.

**Testing a guardrail:**

1. Click the **Test Guardrails** tab.
2. Select one or more guardrails to test.
3. Paste sample text into the input box.
4. Click **Run Test**.
5. Results show whether the guardrail triggered, what action it took (block / mask / warn), and how long it took to run.

## Guardrail Logs

Every time a guardrail evaluates a request, it writes a log entry here.

- Filter by **guardrail name** or **trigger status** (triggered / not triggered).
- The summary bar shows total events, how many triggered, and the overall pass rate.
- Click any row to see the exact text that was flagged and the action taken.

Use this page to verify that your guardrails are catching what they should — and not over-blocking legitimate requests.

## Audit Logs

Audit Logs record every administrative action taken in SecureLLM: who created or revoked a key, who changed a provider, who updated a user policy — with timestamps and IP addresses.

- Filter by **actor** (admin's email) or **action type** (e.g., `create_key`, `revoke_key`, `update_provider`).
- Use this page for compliance reviews or to investigate unexpected changes.

## Performance

The Performance page shows how the gateway itself is behaving.

- **Uptime** — how long SecureLLM has been running since last restart
- **Total Requests / 5xx Errors** — overall traffic and error counts
- **Latency by Endpoint** — P50, P95, and P99 response times per API endpoint

:::{tip}
P95 latency is the response time that 95% of requests fall under. A spike here usually means a specific provider is slow, not that SecureLLM itself is the bottleneck.
:::
