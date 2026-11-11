# Creating and Using API Keys in SecureLLM

This tutorial shows how users can create and use API keys in SecureLLM to connect external tools, scripts, and applications through a managed AI gateway.

API keys allow tools to authenticate to SecureLLM without directly exposing provider credentials, while enabling centralized access control, usage tracking, and governance.

---

## Tutorial Overview

In this tutorial, a user:

- Creates an API key in SecureLLM  
- Configures the key in an external tool or application  
- Sends requests through SecureLLM using the key  
- Monitors request activity and usage  
- Revokes the key when no longer needed  

---

## Prerequisites

Before you begin, ensure:

- You have access to SecureLLM  
- At least one provider and model are available  
- You have permission to create API keys  
- You have a tool or application ready to connect  

Examples:

- IDE plugin  
- Script or application  
- Data pipeline  
- AI-enabled developer tool  

---

## Tutorial Steps

### Step 1: Open API Keys

1. Log into SecureLLM.
2. From the sidebar, select **API Keys**.
3. Review existing keys or create a new one.

---

### Step 2: Create an API Key

1. Click **Create Key**.
2. Enter a descriptive name.

Example:

```text
my-vscode-plugin
```

3. Click **Create**.
4. Copy the generated API key immediately.

> Note: The key is shown only once. Store it securely.

---

### Step 3: Configure the Key in a Tool

Paste the API key into the application or tool that will connect through SecureLLM.

Example environment variable:

```bash
export SECURELLM_API_KEY=your-api-key
```

Or in an application configuration:

```json
{
  "api_key": "your-api-key"
}
```

Save the configuration.

---

### Step 4: Send Requests Through SecureLLM

Use the configured application to submit a request.

The request is authenticated using the API key and routed through SecureLLM to an approved model.

Verify:

- Request succeeds  
- Response is returned  
- Usage is recorded  

---

### Step 5: Monitor Key Activity

1. Open **Usage**.
2. Filter by API key name.
3. Review:

- Request volume  
- Token usage  
- Costs  
- Latency  
- Request history  

Use this to monitor activity associated with the key.

---

### Step 6: Revoke the Key When Needed

If a key is no longer needed or may be compromised:

1. Return to **API Keys**.
2. Locate the key.
3. Click **Revoke**.
4. Confirm the action.

Revoked keys can no longer be used for requests.

---

## Expected Outcome

After completing this workflow, you should be able to:

- Connect tools and applications through SecureLLM  
- Authenticate requests using managed API keys  
- Track usage associated with a specific key  
- Revoke access when needed  
- Use SecureLLM without exposing provider credentials  

---

## Troubleshooting

### Requests Fail with Authentication Errors

Check:

- API key was copied correctly  
- Key is still active  
- Application is using the correct variable or config  

---

### No Usage Appears for the Key

Verify:

- Requests are actually routed through SecureLLM  
- Correct API key filter is selected in Usage  
- Requests completed successfully  

---

### Lost API Key

If the key was not copied when created:

- Revoke the original key  
- Create a new one  
- Update your application configuration  

---

## Related Tutorials

- Discovering and Selecting Models in SecureLLM  
- Monitoring Request Activity and Usage in SecureLLM  
- Managing User Access Controls in SecureLLM  
- Testing and Deploying Guardrail Policies in SecureLLM  