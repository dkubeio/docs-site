# Workflows

These walkthroughs chain together the individual tasks described in [Core features](./user-features.md) and [Administrator features](./admin-features.md) into common, end-to-end scenarios. Each step links back to the page where it is performed.

## Connect an AI provider and confirm it is available

*For administrators.*

1. Go to **Providers** → **Add Provider**. Select the provider type, enter its **API Key** and (if needed) a custom **Base URL**, and optionally list **Allowed Models**. Click **Save**.
2. Make sure the provider is enabled using the toggle switch on its card.
3. Open the **Models** page and search for a model from that provider. Use the **Provider** filter to confirm the model now appears in the list.
4. As requests start coming in, use the **Dashboard** (the **By Provider** table) and the **Usage** page to confirm activity is routing through the new provider.

## Onboard a user with limited access

*For administrators, then the user.*

1. **(Admin)** Go to **Users** → **Add Restriction**. Enter the user's email or username, specify the **Allowed Providers** and/or **Allowed Models** they should have, and click **Save**.
2. **(User)** Log in, go to **API Keys** → **Create Key**, give it a descriptive name, and copy the key immediately — it is only shown once.
3. **(User)** Open the **Models** page. Only the models and providers made available to you appear here. Click the copy icon next to a model to copy its identifier, and paste the key and identifier into your script, tool, or IDE plugin.
4. **(User or admin)** Confirm the requests are flowing on the **Usage** page — the user sees their own history, and an admin sees all users' history from the admin Usage view.

## Turn on and verify a guardrail

*For administrators.*

1. Go to **Guardrails** and enable the guardrail you want (**Content Filter**, **Prompt Injection**, or **Custom**) using its toggle. Changes take effect immediately for all new requests.
2. Open the **Test Guardrails** tab, select the guardrail(s), paste sample text, and click **Run Test** to see whether it triggers and what action it takes (block / mask / warn).
3. Review **Guardrail Logs** to confirm the guardrail is catching what it should — filter by guardrail name or trigger status, and check the pass rate to make sure it is not over-blocking legitimate requests.
4. For any individual request, open its **Request Detail** panel from the **Usage** page to see the guardrail events that request triggered.
