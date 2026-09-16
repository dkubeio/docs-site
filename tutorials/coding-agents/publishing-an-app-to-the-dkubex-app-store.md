# Publishing an App to the DKubeX App Store

[Building and hosting an app](./building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md)
gets your app running in the workspace as a tile — a fast way to build and test. To make it a
first-class DKubeX application that **any user can install from the App Store**, you package it as a
Helm chart, publish that chart to a repository, and register the repository with DKubeX.

A coding agent's **package-app skill** automates the packaging — it creates the Helm chart, wires in
the platform resources your app uses (PostgreSQL, Redis, MinIO), packages the chart, and publishes it
to a Helm repository.

## Prerequisites

- An app built and tested in your workspace (see the tutorial linked above).
- A **GitHub account** and a container registry — GitHub Container Registry (GHCR) or Docker Hub.
- A coding agent open in your workspace **Terminal**.

## Step 1 — Create a GitHub token

You need a GitHub token to push container images and publish the Helm chart.

1. In GitHub, go to **Settings → Developer settings → Personal access tokens → Tokens (classic)**.
2. Click **Generate new token (classic)**, give it a name, and set an expiry.
3. Under **Select scopes**, enable **`repo`** and **`write:packages`** (this also enables
   `read:packages`).
4. Generate the token and copy it — you will not be able to see it again.

## Step 2 — Authenticate in the terminal

In the workspace Terminal, sign in to GitHub and refresh your token so it can push packages:

```bash
gh auth login
gh auth refresh -h github.com -s write:packages,read:packages
```

## Step 3 — Build and push the container images

Have the agent build your app's container images and push them to your registry (GHCR or Docker Hub).
For example, prompt the agent:

```
Build and push the Docker images for this app to my GitHub Container Registry (GHCR).
```

## Step 4 — Package the app with the package-app skill

Have the agent package the app. It creates the **Helm chart** (with the `dkubex` chart annotation,
base-path routing, the identity-header auth contract, and provisioning for any platform resources the
app uses), packages it, and publishes the chart to a **Helm repository**.

The standard layout is **two separate repositories** (or a separate branch) — one for the application
**code**, and one for the **Helm repository**, which holds an `index.yaml` and the packaged chart
(`.tgz`) files. Prompt the agent, for example:

```
Package this app as a DKubeX application. Create a GitHub repo and push the code, and create a
separate Helm repository (index.yaml + packaged chart) so it can be added to the DKubeX app store.
```

The agent publishes the Helm repository (for example, to a `gh-pages` branch) and prints the repository
URL.

## Step 5 — Add the repository in DKubeX

1. In the admin console, open **Applications → Manage Repositories → Add Repository**.
2. Fill in:
   | Field | Value |
   |---|---|
   | **Name** | A name using lowercase letters, digits, and hyphens (used as the Helm repo name). |
   | **Repository URL** | The **raw** GitHub URL of the Helm repository — it must start with `https://raw.githubusercontent.com/…`, **not** `https://github.com/…`. |
   | **Token / Password** | Your classic token from Step 1 (needed for a private repository). |
   | **This repo's charts use private images** | Check this if your container images are private. |
3. Click **Add & Verify**.

Your application now appears in the App Store under **Browse Catalog**, tagged with this repository.

## Step 6 — Install the application

1. **Stop the development version** of the app first — if you are still running it from the workspace,
   stop it so it does not conflict with the installed app on the same port.
2. In the admin console → **Applications → Browse Catalog**, find your app and click **Install**
   (installing is an administrator action).
3. Track the install on the **Applications** tab until it is **Ready**.

## Step 7 — Give users access

1. On the **Applications** tab, open **Actions** on the installed app → **Manage Users & Roles**.
2. Assign users and choose each user's role (**User** or **Admin**).

The application then appears on each assigned user's **App Store** page; the user installs it from
there, and it appears on their **Apps** page.
