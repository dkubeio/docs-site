# Building, Hosting, and Publishing an App with a Coding Agent

A coding agent in DKubeX Workspace can build an app, host it, and publish it — all from
plain-language prompts, with no Docker, CI/CD pipeline, or manual deployment to set up. This tutorial
takes one app end to end: first the agent **builds and hosts** it in your workspace as a tile you can
test, then you **publish** it as a first-class DKubeX application that any user can install from the
App Store.

Both halves use the same **dkubex-app skill** that ships with every coding agent in the workspace, so
the flow is the same whichever agent you prefer. The worked example is a **document data-extraction
app**, but the same flow builds and publishes any app.

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

Every coding agent in the workspace carries the **dkubex-app skill** — the platform's own knowledge of
how to host on DKubeX. When you ask it to build an app, it automatically allocates a port, configures
routing so the app is reachable at its workspace URL, and registers the finished app as its own tile
on the **Apps** page. You never configure any of that — you describe what the app should do, and the
agent builds it, hosts it, and publishes the tile. Because the skill is part of the platform rather
than of any one agent, the flow is identical whichever coding agent you open.

## Build and host in your workspace

### Step 1 — Open a coding agent

From the workspace launcher, open a coding agent (for example, **Claude Code**). Any of the workspace's
coding agents work — Claude Code, Codex, OpenCode, Copilot CLI, Antigravity, Mistral Vibe, and
Hermes — and the dkubex-app skill behaves the same across all of them.

### Step 2 — Describe the app you want built

Give the agent a prompt describing what the app should do — because it already has the dkubex-app
skill, the agent takes care of hosting and publishing.

For anything beyond a quick prototype, the cleanest approach is to write your requirements into a
**specification file** and point the agent at it, so the build is driven by one reviewable source of
truth. For this walkthrough we use a ready-made spec file, `document_extraction_specs.md`, that describes a
**document data-extraction app** — a tool that takes a PDF, extracts the fields you define using a
vision model, and returns structured results. If you were building something else, you would write
your own spec file the same way and point the agent at that; here we use this one.

For this example, download the spec file and place it — using the FileBrowser application on your
DKubeX workspace — in the directory where you'll run the build, so the agent can read it when you
reference `@document_extraction_specs.md`:

- {download}`document_extraction_specs.md <../../example-files/prompts/document_extraction_specs.md>`

Then give the agent this prompt:

```
Build a dkubex app for PDF document extraction using the specification in
`@document_extraction_specs.md`. Implement the complete application described
in the specification.

Constraints:
- Create a fresh project directory for this build in the current directory.
- Create a dedicated Python virtual environment — do not use any existing venvs.
- Build everything from scratch based solely on this reference file — do not
  reference or depend on any other folders or files in this workspace.

Read the reference file, then build and run the application.
```

Once the application is running, a tile with the app name will appear in the apps launcher
(**Apps** page).

The SecureLLM endpoint to be used for fetching the models deployed locally is
`https://<dkubex-host>/securellm/v1`.

The agent reads the specification and builds the complete application — frontend, backend, and
everything the spec calls for — then applies the dkubex-app skill to host and publish it. A build
like this usually takes only a few minutes.

:::{tip}
Keeping the requirements in a spec file (rather than one long prompt) makes the build repeatable and
easy to review or hand off. But it's optional — for a small app you can describe everything inline in
the prompt and the flow is the same.
:::

### Step 3 — Open your app from the Apps page

When the build finishes, the app is already live and published. Go to the DKubeX **Apps** page and
you'll find a new tile with your app's name, alongside the platform's built-in apps. Click it to open
— the app runs on your own cluster and is reachable by anyone with access to the workspace.

From here, iterate with the same agent: describe a change in plain language and the agent edits the
app in place. Its tile keeps pointing at the running app, so your users always reach the latest
version.

## Publish to the DKubeX App Store

Building and hosting gets your app running in the workspace as a tile — a fast way to build and test.
To make it a first-class DKubeX application that **any user can install from the App Store**, you
package it as a Helm chart, publish that chart to a repository, and register the repository with
DKubeX.

A coding agent's **package-app skill** creates the **Helm chart** for your app — wiring in any
platform resources it uses, such as PostgreSQL or MinIO, and packaging the chart (the Helm repository
index and the `.tgz` package). Building and pushing the container images and publishing the chart to a
Helm repository are separate steps you run through the agent, below. This section continues with the
same **document data-extraction app** as the worked example.

### Before you publish

- An app built and tested in your workspace — the build-and-host steps above.
- A coding agent open in your workspace **Terminal**.
- A **GitHub account** and a container registry — GitHub Container Registry (GHCR) or Docker Hub.
- **Authenticate GitHub in the terminal.** In the workspace Terminal, sign in and refresh your token
  so it can push packages (this gives the token read and write permission to packages):

  ```bash
  gh auth login --web
  gh auth refresh -h github.com -s write:packages,read:packages
  ```

### Step 1 — Package the app

With the app built and GitHub authenticated, package it with the package-app skill. Prompt the agent:

```
/package-app package this app
```

The package-app skill creates the Helm chart and packages it — it generates the Helm repository index
(`index.yaml`) and the packaged chart (`.tgz`), wiring in any platform resources the app uses. It does
not build or push the container images; you do that next.

#### Build and push the container images

Prompt the agent to build and push the images to your registry:

```
build and push the docker images using gh to my ghcr
```

#### Create the code repo and the Helm repo branch

Prompt the agent to publish the code and the Helm chart:

```
Also create a github repo and push this code. create a separate branch for helm repo index with the helm package.tgz file
```

This creates the code repository and a **`helm-repo`** branch that holds the Helm repository index
(`index.yaml`) and the packaged chart (`.tgz`) file.

### Step 2 — Copy the Helm repo raw URL

1. In GitHub, open the app's repository and switch to the **`helm-repo`** branch — for example,
   `https://github.com/<your-github-username>/document-extraction/tree/helm-repo`.
2. Convert it to its **raw** URL. It must start with `https://raw.githubusercontent.com/…`, **not**
   `https://github.com/…`, and you must **remove the `tree` segment** from the path — for example:

   ```
   https://raw.githubusercontent.com/<your-github-username>/document-extraction/helm-repo
   ```

```{note}
Drop `tree` when you build the raw URL. The browser address has `.../tree/helm-repo`, but the raw URL
removes it and reads `.../document-extraction/helm-repo`. Leaving `tree` in the URL stops DKubeX from
resolving the repository.
```

### Step 3 — Create a classic token for DKubeX

DKubeX uses a token to download and install the chart, so create a **classic** personal access token
with **`repo`** and **`read:packages`** access (GitHub → **Settings → Developer settings → Personal
access tokens → Tokens (classic)**).

### Step 4 — Add the repository in DKubeX

1. In the admin console, open **Applications → Manage Repositories → Add Repository**.
2. Fill in:
   | Field | Value |
   |---|---|
   | **Name** | A name using lowercase letters, digits, and hyphens (used as the Helm repo name). |
   | **Repository URL** | The **raw** `helm-repo` URL from Step 2. |
   | **Token / Password** | The classic token from Step 3. |
   | **This repo's charts use private images** | Check this if your container images are private. |
3. Click **Add & Verify**.

Your application now appears in the App Store under **Browse Catalog**, tagged with this repository.

### Step 5 — Install the application

1. In the admin console → **Applications → Browse Catalog**, find your app and click **Install**
   (installing is an administrator action). DKubeX handles the port and adds the app's tile.
2. Track the install on the **Applications** tab until it is **Ready**.

### Step 6 — Give users access

1. On the **Applications** tab, open **Actions** on the installed app → **Manage Users & Roles**.
2. Assign users and choose each user's role (**User** or **Admin**).

The app is listed in the **App Store** (Browse Catalog) for everyone regardless of these assignments —
the App Store shows every available app. Assigning users and roles is what makes the app appear on
those users' **Apps** page in their workspace: a user sees it there only after an admin grants them
access.
