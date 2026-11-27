# Troubleshooting

Find your problem below, then follow the link to the page that explains the fix. Each fix lives next
to the task it belongs to, so you also get the surrounding steps.

## Installing and upgrading

| Problem | Fix |
|---|---|
| The cluster is too small for DKubeX | [Installing DKubeX › Hardware requirements](../install/installation.md#hardware-requirements) |
| Workspaces and apps can't share volumes across pods or nodes | [Installing DKubeX › Production recommendations](../install/installation.md#production-recommendations) |
| App Store apps that need a database fail to deploy on an external PostgreSQL | [Installing DKubeX › External PostgreSQL](../install/installation.md#external-postgresql) |
| A managed PostgreSQL is missing the extensions DKubeX needs | [Installing DKubeX › Required PostgreSQL extensions](../install/installation.md#required-postgresql-extensions) |
| Installing on Azure: PostgreSQL extensions, TLS or GPU pods fail | [Installing DKubeX › Azure (AKS and Azure Database for PostgreSQL)](../install/installation.md#azure-aks-and-azure-database-for-postgresql) |
| Installing on AWS: GPU pods fail to start | [Installing DKubeX › AWS (EKS)](../install/installation.md#aws-eks) |
| GPUs aren't detected on a GPU node | [Installing DKubeX › Label GPU nodes](../install/installation.md#label-gpu-nodes) |
| The cluster shows the physical GPU count instead of shared GPU slots (NVIDIA GPU Operator installed) | [Installing DKubeX › Clusters running the NVIDIA GPU Operator](../install/installation.md#clusters-running-the-nvidia-gpu-operator) |
| GPUs aren't detected, or show no memory, on an NVIDIA DGX | [Installing DKubeX › Installing on NVIDIA DGX](../install/installation.md#installing-on-nvidia-dgx) |
| The admin login still uses the old email and password after an upgrade | [Installing DKubeX › Admin account](../install/installation.md#admin-account) |
| An upgrade was interrupted and the platform is stuck | [Platform Upgrade › Recover a stuck upgrade](../install/platform-upgrade.md#recover-a-stuck-upgrade) |

## Sign-in, licenses and access

| Problem | Fix |
|---|---|
| A user is blocked because no seat is free | [Licensing › View license details and seats](../platform-guide/licensing.md#view-license-details-and-seats) |
| A user is blocked because the trial or the license expired | [Licensing › Renew or remove a license](../platform-guide/licensing.md#renew-or-remove-a-license) |
| A blocked user raised a license request | [Licensing › Handle license requests](../platform-guide/licensing.md#handle-license-requests) |
| A user's access request was approved, but they still can't open the app | [Access Requests › Approve a request](../platform-guide/access-requests.md#approve-a-request) |
| A user was assigned to an app, but it doesn't appear on their Apps page | [Application Management › Manage users and roles](../platform-guide/application-management.md#manage-users-and-roles-for-an-application) |
| An App Store install shows Failed | [Application Management › Install an application](../platform-guide/application-management.md#install-an-application) |
| The **Admin** link is missing from the header | [User Management › Edit a user](../platform-guide/user-management.md#edit-a-user) |
| The SecureLLM admin pages (Providers, Users, Guardrails) are missing | [SecureLLM › Administrator features](../applications/securellm/admin-features.md#administrator-features) |

## Models (ModelStudio)

| Problem | Fix |
|---|---|
| An LLM stays in Pending, Downloading or Starting | [Deploying Models › LLM deployment lifecycle](../applications/modelstudio/deploying-models.md#llm-deployment-lifecycle) |
| A NIM model stays in Deploying for a long time | [Deploying Models › NIM deployment lifecycle](../applications/modelstudio/deploying-models.md#nim-deployment-lifecycle) |
| A model doesn't use the GPU | [Deploying a Model on GPU › Deploy the model](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-gpu.md#deploy-the-model) |
| A model deployed on several GPUs leaves the extra GPUs idle | [Deploying a Model on Multiple GPUs › Step 2](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-multiple-gpus.md#step-2-deploy-across-the-gpus) |
| A model won't deploy on CPU | [Deploying a Model on CPU › Steps](../tutorials/end-to-end-workflows/model-management/deploying-a-model-on-cpu.md#steps) |
| A deployed model doesn't appear in the Playground | [Playground › Tips](../applications/modelstudio/playground.md#tips) |
| Vision, image generation or speech-to-text doesn't work in the Playground | [Playground › Coming in future KubeAI releases](../applications/modelstudio/playground.md#coming-in-future-kubeai-releases) |

## Workspace and coding agents

| Problem | Fix |
|---|---|
| An agent asks you to log in or for an API key | [Working with AI Agents › Troubleshooting](../applications/workspace/working-with-agents.md#troubleshooting) |
| An agent reports a model that no longer exists | [Working with AI Agents › Troubleshooting](../applications/workspace/working-with-agents.md#troubleshooting) |
| An agent asks you to trust the folder | [Working with AI Agents › Troubleshooting](../applications/workspace/working-with-agents.md#troubleshooting) |
| You want to use your own Claude or ChatGPT subscription | [Working with AI Agents › Troubleshooting](../applications/workspace/working-with-agents.md#troubleshooting) |
| Claude Code sign-in: the browser did not open | [Claude Code with a Claude subscription › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md#troubleshooting) |
| Claude Code sign-in: the code is rejected | [Claude Code with a Claude subscription › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md#troubleshooting) |
| Claude Code sign-in: wrong Claude account | [Claude Code with a Claude subscription › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md#troubleshooting) |
| No models in the model dropdown | [Claude Code with DKubeX or cloud models › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-dkubex-or-cloud-provider-models.md#troubleshooting) |
| `/model` still shows the old model | [Claude Code with DKubeX or cloud models › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-dkubex-or-cloud-provider-models.md#troubleshooting) |
| The coding agent behaves poorly | [Claude Code with DKubeX or cloud models › Troubleshooting](../tutorials/coding-agents/using-claude-code-in-dkubex-workspace-with-dkubex-or-cloud-provider-models.md#troubleshooting) |
| A workspace stays in Provisioning or shows Failed | [Managing Your Workspace › Getting help](../applications/workspace/managing-workspaces.md#getting-help) |
| Files are gone after a restart or reinstall | [Managing Your Workspace › What persists](../applications/workspace/managing-workspaces.md#what-persists) |
| Installed packages are gone after an uninstall and reinstall | [Workspace Workflows › Install Python packages in your own environment](../applications/workspace/tutorials.md#install-python-packages-in-your-own-environment) |
| Applying environment variables restarted the workspace | [Using Your Workspace › Environment variables](../applications/workspace/using-your-workspace.md#environment-variables) |
| Applying a default model restarted the workspace | [Working with AI Agents › Using your organization's models](../applications/workspace/working-with-agents.md#using-your-organizations-models) |
| SSH from your local editor is rejected | [Workspace Workflows › Connect from your local editor over SSH](../applications/workspace/tutorials.md#connect-from-your-local-editor-over-ssh) |
| A dev server at `<your-workspace-url>/<port>/` gives a gateway error or a blank page | [Using Your Workspace › Running your own services](../applications/workspace/using-your-workspace.md#running-your-own-services) |

## Publishing apps

| Problem | Fix |
|---|---|
| Pushing the app's images to GitHub Container Registry fails | [Building, Hosting, and Publishing an App › Before you publish](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md#before-you-publish) |
| DKubeX can't resolve the Helm repository you added | [Building, Hosting, and Publishing an App › Step 4](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md#step-4-copy-the-helm-repo-raw-url) |
| The published app fails to install because the chart can't be downloaded | [Building, Hosting, and Publishing an App › Step 5](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md#step-5-create-a-classic-token-for-dkubex) |
| The published app fails to install because its private images can't be pulled | [Building, Hosting, and Publishing an App › Step 6](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md#step-6-add-the-repository-in-dkubex) |
| Users can't see the published app on their Apps page | [Building, Hosting, and Publishing an App › Step 8](../tutorials/coding-agents/building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md#step-8-give-users-access) |

## RAGFlow

| Problem | Fix |
|---|---|
| The assistant makes things up when nothing relevant is retrieved | [Chat › Assistant settings](../applications/ragflow/chat.md#assistant-settings) |
| Answers ignore your documents | [Knowledge Bases › Run a retrieval test](../applications/ragflow/knowledge-bases.md#run-a-retrieval-test) |
| PDF parsing is very slow | [Knowledge Bases › Select a PDF parser](../applications/ragflow/knowledge-bases.md#select-a-pdf-parser) |
| Uploaded files aren't parsed | [Knowledge Bases › Upload and parse files](../applications/ragflow/knowledge-bases.md#upload-and-parse-files) |
| An error when you pick datasets with different embedding models for a chat assistant | [Knowledge Bases › Select an embedding model](../applications/ragflow/knowledge-bases.md#select-an-embedding-model) |
| A model deployed in ModelStudio doesn't appear in RAGFlow | [Using Models on DKubeX › Refresh models](../applications/ragflow/models.md#refresh-models) |

## Langflow

| Problem | Fix |
|---|---|
| A deployment shows "Failed" (missing global variables, a Python error on startup, or `ImagePullBackOff`) | [Deploying Flows › Troubleshooting](../applications/langflow/deploying-flows.md#troubleshooting) |
| "Name already in use" when deploying | [Deploying Flows › Troubleshooting](../applications/langflow/deploying-flows.md#troubleshooting) |
| "The following global variables are referenced but not found" | [Deploying Flows › Troubleshooting](../applications/langflow/deploying-flows.md#troubleshooting) |
| A deployment stays in "Deploying" for more than 5 minutes | [Deploying Flows › Troubleshooting](../applications/langflow/deploying-flows.md#troubleshooting) |
| A model is missing from a Language Model or Embedding Model component | [Components › SecureLLM models](../applications/langflow/components.md#securellm-models) |

## SecureLLM

| Problem | Fix |
|---|---|
| An AI provider fails authentication | [AI providers › Provider fails authentication](../tutorials/end-to-end-workflows/llm-governing/configuring-and-enabling-ai-providers-in-securellm.md#provider-fails-authentication) |
| A provider's models do not appear on the Models page | [AI providers › Models do not appear](../tutorials/end-to-end-workflows/llm-governing/configuring-and-enabling-ai-providers-in-securellm.md#models-do-not-appear-in-models-page) |
| Requests fail after a provider is enabled | [AI providers › Requests fail after enabling](../tutorials/end-to-end-workflows/llm-governing/configuring-and-enabling-ai-providers-in-securellm.md#requests-fail-after-provider-is-enabled) |
| Requests with an API key fail with authentication errors | [API keys › Authentication errors](../tutorials/end-to-end-workflows/llm-governing/creating-and-using-api-keys-in-securellm.md#requests-fail-with-authentication-errors) |
| No usage appears for an API key | [API keys › No usage appears](../tutorials/end-to-end-workflows/llm-governing/creating-and-using-api-keys-in-securellm.md#no-usage-appears-for-the-key) |
| An API key was lost | [API keys › Lost API key](../tutorials/end-to-end-workflows/llm-governing/creating-and-using-api-keys-in-securellm.md#lost-api-key) |
| A guardrail does not trigger | [Guardrail policies › Guardrail does not trigger](../tutorials/end-to-end-workflows/llm-governing/testing-and-deploying-guardrail-policies-in-securellm.md#guardrail-does-not-trigger) |
| A guardrail gives too many false positives | [Guardrail policies › Too many false positives](../tutorials/end-to-end-workflows/llm-governing/testing-and-deploying-guardrail-policies-in-securellm.md#too-many-false-positives) |
| Legitimate requests are being blocked | [Guardrail policies › Legitimate requests blocked](../tutorials/end-to-end-workflows/llm-governing/testing-and-deploying-guardrail-policies-in-securellm.md#legitimate-requests-are-being-blocked) |
| Requests fail with a `400` "budget exceeded" error | [SecureLLM › Administrator features › Users](../applications/securellm/admin-features.md#users) |
| An API key was leaked | [SecureLLM › Core features › API Keys](../applications/securellm/user-features.md#api-keys) |

## MLflow

| Problem | Fix |
|---|---|
| Logged runs don't show in MLflow | [MLflow › Point your code at the tracking server](../applications/mlflow/getting-started.md#point-your-code-at-the-tracking-server) |
| A training script can't authenticate to MLflow | [Training and Deploying an ML Model › Step 2](../tutorials/end-to-end-workflows/mlops/training-and-deploying-an-ml-model-on-dkubex.md#step-2-configure-the-environment-variables) |

## SRE

| Problem | Fix |
|---|---|
| A user is locked out after five wrong PINs | [SRE › Getting started › Log in](../applications/sre/getting-started.md#log-in) |
| SRE can't change the cluster (no write access) | [SRE › Administrator features › Autonomy & safety](../applications/sre/admin-features.md#autonomy--safety) |
| A fine-tune in Training Studio never runs | [SRE › Administrator features › Training Studio](../applications/sre/admin-features.md#training-studio) |
