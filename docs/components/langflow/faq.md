# FAQ

## General

### The canvas is blank after login.
Refresh the page. If the issue persists, confirm your DKubeX session is still valid from the profile menu in the header. On the very first login, Langflow auto-provisions your user account which may take a second or two.

### My component shows a red error badge.
Click the component to open its side panel and scroll to the **Logs** section. Most errors are missing API keys or invalid field values. For DKubeX LLM / DKubeX Embeddings components, verify your SecureLLM API Key is set and the model dropdown has been refreshed.

### How do I switch between light and dark mode?
Use the theme toggle in the top-right of the DKubeX header. Options are **Light**, **Dark**, and **System** (follows your OS preference). The setting is persisted across sessions.

### Where are my flows stored?
Flows are stored in the DKubeX PostgreSQL database, organized into projects (folders). Projects are per-user and can be shared with other DKubeX users from the project settings.

### How do I roll back to a previous version of a flow?
Open the flow menu (pencil icon next to the flow name in the header) and choose **Version history**.

---

## DKubeX Providers Components

### The DKubeX LLM / DKubeX Embeddings model dropdown is empty after clicking refresh.
This means the SecureLLM service returned no models of the matching type, or the API key is invalid. Check:
1. The **SecureLLM API Key** field is filled in correctly.
2. Your cluster administrator has deployed at least one model of the matching type (TextGeneration for LLM, TextEmbedding for Embeddings).
3. The SecureLLM service is running: ask your admin to verify `kubectl get pods -n dkubex-apps | grep securellm`.

### The model dropdown shows "No models available".
Same as above — either the API key is wrong or no models of that type are registered in SecureLLM.

### I entered an API key but get a 401 error in the flow logs.
The API key is being sent as the `x-api-key` header. Verify the key is correct by testing directly:
```bash
curl http://securellm.dkubex-apps.svc.cluster.local/securellm/v1/models \
  -H "x-api-key: <your-key>"
```
(Run this from within the cluster, e.g. via `kubectl exec` into a pod.)

### Do I need to enter the SecureLLM API Key every time?
No. The key is stored using Langflow's `SecretStrInput` which persists it encrypted in the database. You only need to enter it once per component instance. It will be pre-filled on subsequent sessions.

---

## Flow Deployment

### How long does a deployment take?
Typically 1–2 minutes. The pod must be scheduled, the image pulled (if not cached on the node), and Langflow must start up. Watch the status in the Deployments tab — it transitions from **Deploying** to **Deployed** when ready.

### My deployment is stuck in "Deploying".
After 5 minutes without becoming ready, the status automatically changes to **Failed**. Click **⋯ → Logs** to see what went wrong. Common causes: image pull failure, missing global variables, insufficient cluster resources.

### My deployment shows "Failed".
Check the logs via **⋯ → Logs**. Common causes:
- **Missing Global Variables** — the flow references a global variable that wasn't defined. Add it in Langflow **Settings → Global Variables** and re-deploy.
- **Python error on startup** — a component in the flow fails to initialize. The traceback will be in the logs.
- **ImagePullBackOff** — the runtime image cannot be pulled. Contact your cluster administrator.

### I get "Name already in use" when deploying.
Either a deployment with that name already exists or a previous one is still being deleted. Wait ~30 seconds for cleanup and try again, or choose a different name.

### How do I call my deployed flow from outside the cluster?
The deployed pod is accessible only within the cluster by default (`*.dkubex-apps.svc.cluster.local`). For external access, contact your cluster administrator to set up an ingress or gateway route. Alternatively, use the main Langflow instance's `/api/v1/run/{flow_id}` endpoint which is externally accessible through the DKubeX gateway.

### Does removing a deployment delete my flow?
No. **Remove Deployment** only stops the standalone serving pod. Your flow in the Langflow canvas is unaffected. You can re-deploy the same flow at any time.

### Can I update a deployment without removing it?
You can edit the description, CPU/memory limits, and environment variables via **⋯ → Edit Resources**. This triggers a rolling restart. If you need to update the flow logic itself, you must remove the deployment and re-deploy the updated flow.

---

## Self-hosting

### Can I self-host this?
Yes. See the upstream [Langflow project](https://github.com/langflow-ai/langflow) for self-hosting instructions. The DKubeX integration (header, deployment feature, SecureLLM components) is maintained in this repository and requires a DKubeX cluster. Contact your DKubeX administrator for access.
