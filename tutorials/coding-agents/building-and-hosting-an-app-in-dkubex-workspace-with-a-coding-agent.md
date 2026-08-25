# Building and Hosting an App in DKubeX Workspace with a Coding Agent

Once you have a coding agent running in DKubeX Workspace, you can have it build an app and publish it
straight from the workspace — live at its own URL, with its own tile on the **Apps** page, reachable
by anyone who has access to the workspace. There is no Docker to write, no CI/CD pipeline, and no
manual deployment step. You describe the app in plain language, the agent builds it and publishes it,
and it runs.

This works because the workspace's coding agents ship with the **dkubex-app skill** — the platform's
own knowledge of how to host on DKubeX. The agent already knows how to allocate a port, configure
routing, and register the finished app as a first-class tile, so your prompts stay focused on what
the app does, not on how hosting works. And the same skill works across every coding agent in the
workspace — Claude Code, Codex, Copilot, and the rest — so the flow and the result are the same
whichever agent you prefer.

This tutorial walks through it end to end using a **document data-extraction app** as the worked
example, but the same flow builds and publishes any app.

To get a coding agent set up first, see
[Using Claude Code in DKubeX Workspace with a Claude subscription](./using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md)
or
[Using Claude Code in DKubeX Workspace with DKubeX or cloud provider models](./using-claude-code-in-dkubex-workspace-with-dkubex-or-cloud-provider-models.md).

```{raw} html
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;margin:1.5rem 0;border-radius:8px;">
  <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
    src="https://www.youtube-nocookie.com/embed/fq3Kubvw_wc" title="Building and hosting an app in DKubeX Workspace with a coding agent"
    loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen></iframe>
</div>
```

> 📺 Prefer to watch? See the walkthrough on YouTube: <https://youtu.be/fq3Kubvw_wc>

## Prerequisites

- A running DKubeX Workspace.
- A coding agent set up in the workspace — Claude Code, Codex, OpenCode, Copilot CLI, Antigravity,
  Mistral Vibe, or Hermes. See the two tutorials linked above.

## How it works — the dkubex-app skill

Building and hosting a web app the traditional way means standing up a development environment, a
hosting platform, and a deployment pipeline, and wiring them together — before you write a single
line of code. DKubeX collapses that into one prompt.

Every coding agent in the workspace carries the **dkubex-app skill**: standing platform knowledge the
agent applies automatically whenever you ask it to build a DKubeX app. With it, the agent:

- allocates a port for your app,
- configures routing so the app is reachable at its workspace URL, and
- registers the app as its own tile on the **Apps** page once it is running.

You never configure any of that yourself, and you never see it — you describe the app, and the agent
builds it, hosts it, and publishes the tile. Because the skill is part of the platform rather than of
any one agent, the flow is identical no matter which coding agent you open.

## Step 1 — Open a coding agent

From the workspace launcher, open a coding agent (for example, **Claude Code**). Any of the agents
work:

| Agent | Best for |
| --- | --- |
| **Claude Code** | Full-stack apps, complex logic |
| **Codex** | Quick prototyping, OpenAI models |
| **OpenCode** | Open-source model workflows |
| **Copilot CLI** | GitHub-integrated development |
| **Antigravity** | Google model exploration |
| **Mistral Vibe** | Mistral-powered coding |
| **Hermes** | Nous Research models |

## Step 2 — Describe the app you want built

Give the agent a prompt describing your app. Because it already has the dkubex-app skill, you don't
spell out ports, routing, or hosting — you describe what the app should do, and the agent takes care
of publishing it.

For anything beyond a quick prototype, the cleanest approach is to write your requirements into a
**specification file** and point the agent at it, so the build is driven by one reviewable source of
truth. The walkthrough builds a **document data-extraction app** — a tool that takes a PDF, extracts
the fields you define using a vision model, and returns structured results — from a spec file, with
this prompt:

```
Build a dkubex app for PDF document extraction using the specification in
`@document_extraction_prompt.md`. Implement the complete application described
in the specification.

Constraints:
- Create a fresh project directory for this build.
- Create a dedicated Python virtual environment — do not use any existing venvs.
- Build everything from scratch based solely on this reference file — do not
  reference or depend on any other folders or files in this workspace.

Read the reference file, then build and run the application.

Once the application is running, a tile with the app name will appear in the
apps launcher (Apps page).

SecureLLM endpoint to be used for fetching the models deployed locally is
https://<dkubex-host>/securellm/v1
```

The agent reads the specification and builds the complete application — frontend, backend, and
everything the spec calls for — then applies the dkubex-app skill to host and publish it. A build
like this usually takes only a few minutes.

:::{tip}
Keeping the requirements in a spec file (rather than one long prompt) makes the build repeatable and
easy to review or hand off. But it's optional — for a small app you can describe everything inline in
the prompt and the flow is the same.
:::

## Step 3 — Open your app from the Apps page

When the build finishes, the app is already live and published. Go to the DKubeX **Apps** page and
you'll find a new tile with your app's name, alongside the platform's built-in apps. Click it to open
— the app runs on your own cluster and is reachable by anyone with access to the workspace.

From here, iterate with the same agent: describe a change in plain language and the agent edits the
app in place. Its tile keeps pointing at the running app, so your users always reach the latest
version.
