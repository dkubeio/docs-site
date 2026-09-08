# Using Claude Code in DKubeX Workspace with DKubeX or Cloud Provider Models

DKubeX Workspace ships with several coding agents built in — including **Claude Code**, **Codex**,
**Copilot CLI**, **OpenCode**, **Antigravity**, and **Mistral Vibe**. Instead of a Claude
subscription, you can run Claude Code in DKubeX Workspace against a model served through the
platform — either a model you **deployed in Model Studio** or a model from a **cloud provider
(such as Anthropic, OpenAI, or OpenRouter) added in SecureLLM**. The workspace injects your chosen
model into the coding agent, and all requests are governed and billed through the platform.

Use this flow when you want the coding agent to run on platform-served models. To use your own
Claude subscription instead, see
[Using Claude Code in DKubeX Workspace with a Claude subscription](./using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md).

```{raw} html
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;margin:1.5rem 0;border-radius:8px;">
  <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    src="https://www.youtube-nocookie.com/embed/5DJhP9rYS6o" title="Claude Code with DKubeX or cloud provider models"
    loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
</div>
```

> 📺 Prefer to watch? See the walkthrough on YouTube: <https://youtu.be/5DJhP9rYS6o>

## Prerequisites

- DKubeX Workspace, installed from the app catalog.
- At least one model available to your DKubeX user key, provided by either:
  - a model **deployed in Model Studio**, or
  - a **cloud provider added in SecureLLM** (such as Anthropic, OpenAI, or OpenRouter), which
    exposes that provider's models to you.

## Step 1 — Make a model available

Choose one of the following so a model shows up under your key:

- **Deploy a model in Model Studio** — deploy a coding-capable model and wait until it reaches the
  running state. See
  [Deploying models on DKubeX using Model Studio](../llms-and-rag/deploying-models-on-dkubex-using-model-studio.md).
- **Add a cloud provider in SecureLLM** — add a provider such as Anthropic, OpenAI, or OpenRouter so
  its models become available to your key. See
  [Configuring and enabling AI providers in SecureLLM](../governing-llm-access/configuring-and-enabling-ai-providers-in-securellm.md).

## Step 2 — Set the workspace default model

The workspace default model is what the coding agent uses. Open **Profile → Settings → Workspace**.
The **Default model** starts at **None**, which injects no model settings and lets each agent use
its own defaults.

```{figure} media/workspace-settings-default-model-none.png
:alt: Workspace settings with default model set to None
:width: 100%

Workspace settings — the default model starts at None.
```

Open the **Default model** dropdown and pick a model. The list shows the models available to your
key — DKubeX-deployed models appear under the `dkubex/` prefix, and each cloud provider's models
appear under the **name you gave that provider** in SecureLLM (for example, a provider named
`openrouter-1` exposes models like `openrouter-1/anthropic/claude-opus-4.8`). Choose a
coding-capable model.

```{figure} media/workspace-settings-select-model.png
:alt: Workspace default model dropdown listing DKubeX-deployed and cloud-provider models
:width: 100%

Pick a model from those available to your key — `dkubex/` for deployed models, and each cloud provider under its own prefix.
```

With the model selected, click **Apply and restart**. Applying restarts your workspace so the new
model settings take effect.

```{figure} media/workspace-settings-model-set.png
:alt: Workspace settings with a default model selected
:width: 100%

The selected default model. Click Apply and restart to roll it out.
```

## Step 3 — Open Claude Code and confirm the model

Wait for the workspace pod to finish restarting, then open **Claude Code**. Run the `/model` command
to confirm which model the agent is using — you should see your default model listed as the active
model.

```{figure} media/claude-code-model-command.png
:alt: The /model command in Claude Code showing the active platform model
:width: 100%

Run `/model` to confirm the active model in Claude Code.
```

You can change the model at any time from within the agent using the `/model` command.

```{note}
All requests routed through the models are recorded by SecureLLM and can be monitored in its
**Usage** tab.
```

## Reverting to your Claude subscription

To go back to your Claude subscription, open **Profile → Settings → Workspace**, set the
**Default model** to **None**, and click **Apply and restart**. Once the workspace restarts, Claude
Code returns to your original Claude subscription login. See
[Using Claude Code in DKubeX Workspace with a Claude subscription](./using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md).

## Troubleshooting

- No models in the dropdown: confirm a model is deployed and running in Model Studio, or that a
  cloud provider is added in SecureLLM, so a model is available to your key.
- `/model` still shows the old model: make sure you clicked **Apply and restart** and waited for the
  workspace pod to finish restarting.
- Agent behaves poorly: pick a coding-capable model — small embedding-only models are not suited to
  driving a coding agent.

## Next steps

With Claude Code running, have it build and host an app straight from your workspace — see
[Building and hosting an app in DKubeX Workspace with a coding agent](./building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md).
