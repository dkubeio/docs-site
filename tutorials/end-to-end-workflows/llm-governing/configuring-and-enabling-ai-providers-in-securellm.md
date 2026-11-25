# Configuring and Enabling AI Providers in SecureLLM

This tutorial shows how administrators can configure and enable AI providers in SecureLLM to make models available through the gateway.

Providers define which external or internal model services SecureLLM can route requests to. Administrators can add providers, control allowed models, and enable or disable providers as needed.

---

## Tutorial Overview

In this tutorial, an administrator:

- Adds a new AI provider  
- Configures provider credentials and endpoint settings  
- Defines allowed models  
- Enables the provider for use  
- Verifies models are available to users  

---

## Prerequisites

Before you begin, ensure:

- You have administrator access in SecureLLM  
- You have provider connection details available  
- You have an API key or authentication credential for the provider  
- You know which models should be exposed to users  

Examples of provider types:

- Commercial model providers  
- Internal model endpoints  
- Private model services  

---

## Tutorial Steps

### Step 1: Open Providers

1. Log into SecureLLM.
2. From the top menu, open **Gateway**, then **Providers** (shown to administrators only).
3. Review configured providers or add a new one.

---

### Step 2: Add a Provider

1. Click **+ Add Provider**.
2. Select the provider **Type**: OpenAI, Anthropic, OpenRouter, Amazon Bedrock, **OpenAI Compatible**
   (for example a vLLM or LiteLLM server), or Ollama (local).
3. Enter required configuration details:

- **API Key** (for Amazon Bedrock, **Bedrock API Key**)  
- **Base URL** (if applicable: OpenAI Compatible and Ollama; include `/v1`). Amazon Bedrock asks for the
  **AWS Region** and **Model Listing Endpoint** instead.  
- **Name** (the provider name; clients can use it to pick this provider)  
- Authentication settings: the form has no separate field for these; the API key above is the
  credential  
- **SafeAgents tool-call guard** (optional): Off, Log only, or Block  

Example:

```text
Type: OpenAI Compatible
Base URL: https://api.example.com/v1
```

4. Click **Add Provider** (when editing an existing provider, **Save Changes**).

---

### Step 3: Configure Allowed Models

Optionally restrict which models are exposed through this provider. **Allowed Models** is a field in
the same **Add Provider** form: enter comma-separated model IDs, or leave it empty to allow every model.

Example:

```text
gpt-4
claude-sonnet
embedding-model-v1
```

You can:

- Allow all models  
- Restrict to specific models  
- Limit access to approved models only  

Save configuration changes.

---

### Step 4: Enable the Provider

1. Locate the provider in the Providers page.
2. Use the toggle switch in the **Enabled** column to enable it. A new provider is enabled as soon as it
   is added, so this step is needed only if it was turned off.
3. Confirm the provider is active: the **Health** column shows **Healthy**.

Once enabled, SecureLLM can route requests to this provider.

---

### Step 5: Verify Model Availability

1. From the top menu, open **Gateway**, then **Models**.
2. Search ("Search models…") or filter by the provider (the **All providers** list). Use **↻ Refresh**
   to reload the list.
3. Verify configured models appear in the list.

Confirm users can discover models from the provider.

---

### Step 6: Test Requests Through the Provider

Submit a test request using one of the provider’s models. The SecureLLM UI has no test button: send
the request from a client or with `curl` using an API key, then check it under **Logs → Request Logs**.

Verify:

- Request succeeds  
- Response is returned  
- Usage is recorded  
- No routing or authentication errors occur  

---

## Managing Provider Availability

Providers can be enabled or disabled without deleting configuration.

### Disable a Provider

Use the provider toggle to temporarily stop routing requests.

Common reasons:

- Maintenance  
- Cost control  
- Provider instability  
- Policy changes  

---

### Delete a Provider

Delete a provider only if it will no longer be used. The built-in `dkubex` and `dkubex-dynamo` providers
have no **Delete** button.

Review dependencies before removal.

---

## Expected Outcome

After completing this workflow, you should be able to:

- Add and configure AI providers in SecureLLM  
- Control which models are available  
- Enable providers for request routing  
- Verify model access for users  
- Manage provider availability over time  

---

## Troubleshooting

### Provider Fails Authentication

Check:

- API key is valid  
- Credentials were entered correctly  
- Base URL is correct  
- Provider endpoint is reachable  

---

### Models Do Not Appear in Models Page

Verify:

- Provider is enabled  
- Allowed models are configured correctly  
- Model list was refreshed (**↻ Refresh** on the Models page)  
- User access restrictions are not blocking visibility  

---

### Requests Fail After Provider Is Enabled

Review:

- Provider configuration  
- Routing configuration  
- Request logs (**Logs → Request Logs**)  
- Provider-side availability  

---

## Related Tutorials

- Discovering and Selecting Models in SecureLLM  
- Managing User Access Controls in SecureLLM  
- Testing and Deploying Guardrail Policies in SecureLLM  
- Monitoring Gateway Health and Performance in SecureLLM  