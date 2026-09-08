# Workflows

This walkthrough chains together the steps from [Getting started](./getting-started.md), [Building flows](./building-flows.md), [Components](./components.md), and [Deploying flows](./deploying-flows.md) into one end-to-end scenario: building a chat flow that uses DKubeX models, testing it, and deploying it as an API endpoint.

## Build and deploy a chat flow with DKubeX models

1. **Launch Langflow.** Click the **Langflow** tile in your DKubeX dashboard — you are logged in automatically via DKubeX SSO.
2. **Create a new flow.** Click **New Flow** from the projects list and choose a blank canvas.
3. **Add the components.** From the left sidebar, drag a **Chat Input** and a **Chat Output** (both in the **Input & Output** category) onto the canvas, then open the **DKubeX Providers** category and drag a **DKubeX LLM** component alongside them.
4. **Configure the DKubeX LLM.** Click the component to open its side panel, enter your **SecureLLM API Key**, click **Model Name** and then **Refresh list** to load the available models, and select a model.
5. **Connect the components.** Drag from each component's output port to a compatible input port (compatible ports share a colour) to wire **Chat Input → DKubeX LLM → Chat Output**.
6. **Test the flow.** Click the **Playground** button in the top-left corner of the canvas to chat with your flow and see its output. You can also click **Run Component** on any component to execute the flow up to that point.
7. **Deploy the flow.** In **Development Mode**, open the three-dots **⋯** menu next to the flow name and click **Deploy**. In the **Deploy Workflow** modal, enter a **Name** (4–30 characters) and an optional **Description**, then click **Deploy**. You are switched to **Deployment Mode**, where the new deployment appears in the table.
8. **Call the endpoint.** Once the deployment's status is **Deployed**, click its row and open the **API Access** tab for a ready-to-use call to your flow.

> **Tip:** To reuse a secret such as your SecureLLM API Key across flows, store it once under **Settings → Global Variables** and reference it from the component. If you deploy a flow that uses global variables, make sure those variables are defined before deploying — see [Building flows](./building-flows.md#variables-and-secrets).

> **Extending to retrieval:** To ground a flow in your own documents, add a **DKubeX Embeddings** component and connect it to a **Vector Store** component to index and retrieve documents — see [Components](./components.md#dkubex-embeddings).
