# Publishing an App to the DKubeX App Store

[Building and hosting an app](./building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md)
gets your app running in the workspace as a tile — a fast way to build and test. To make it a
first-class DKubeX application that **any user can install from the App Store**, you package it as a
Helm chart, publish that chart to a repository, and register the repository with DKubeX.

A coding agent's **package-app skill** does the packaging — it creates the Helm chart (wiring in the
platform resources your app uses, such as PostgreSQL), builds and pushes the container images, and
publishes the chart to a Helm repository. This tutorial uses a **todo-list app that stores its data in
PostgreSQL** as the worked example.

## Prerequisites

- A coding agent open in your workspace **Terminal**.
- A **GitHub account** and a container registry — GitHub Container Registry (GHCR) or Docker Hub.

## Step 1 — Build the app

Have the agent build the app. For the example, prompt it:

```
create a dkubex app called todo list app which uses postgress to store the data
```

The agent builds and hosts the app in your workspace as a tile so you can test it. For the details of
this step, see
[Building and hosting an app](./building-and-hosting-an-app-in-dkubex-workspace-with-a-coding-agent.md).

## Step 2 — Package the app

Once the app works, package it. Start by prompting the agent:

```
package this app
```

Packaging pushes images and publishes a chart to GitHub, so authenticate first, then run the remaining
prompts.

### Authenticate GitHub in the terminal

In the workspace Terminal, sign in and refresh your token so it can push packages (this creates a
token with read and write permission to packages):

```bash
gh auth login --web
gh auth refresh -h github.com -s write:packages,read:packages
```

### Build and push the container images

Prompt the agent to build and push the images to your registry:

```
build and push the docker images using gh to my ghcr
```

### Create the code repo and the Helm repo branch

Prompt the agent to publish the code and the Helm chart:

```
Also create a github repo and push this code. create a separate branch for helm repo index with the helm package.tgz file
```

This creates the code repository and a **`helm-repo`** branch that holds the Helm repository index
(`index.yaml`) and the packaged chart (`.tgz`) file.

## Step 3 — Copy the Helm repo raw URL

1. In GitHub, open the app's repository and switch to the **`helm-repo`** branch — for example,
   `https://github.com/<your-github-username>/todo-list-app/tree/helm-repo`.
2. Take its **raw** URL. It must start with `https://raw.githubusercontent.com/…`, **not**
   `https://github.com/…` — for example:

   ```
   https://raw.githubusercontent.com/<your-github-username>/todo-list-app/helm-repo
   ```

## Step 4 — Create a classic token for DKubeX

DKubeX uses a token to download and install the chart, so create a **classic** personal access token
with **`repo`** and **`read:packages`** access (GitHub → **Settings → Developer settings → Personal
access tokens → Tokens (classic)**).

## Step 5 — Add the repository in DKubeX

1. In the admin console, open **Applications → Manage Repositories → Add Repository**.
2. Fill in:
   | Field | Value |
   |---|---|
   | **Name** | A name using lowercase letters, digits, and hyphens (used as the Helm repo name). |
   | **Repository URL** | The **raw** `helm-repo` URL from Step 3. |
   | **Token / Password** | The classic token from Step 4. |
   | **This repo's charts use private images** | Check this if your container images are private. |
3. Click **Add & Verify**.

Your application now appears in the App Store under **Browse Catalog**, tagged with this repository.

## Step 6 — Install the application

1. **Stop the development version** of the app first — if it is still running from the workspace, stop
   it so it does not conflict with the installed app on the same port.
2. In the admin console → **Applications → Browse Catalog**, find your app and click **Install**
   (installing is an administrator action).
3. Track the install on the **Applications** tab until it is **Ready**.

## Step 7 — Give users access

1. On the **Applications** tab, open **Actions** on the installed app → **Manage Users & Roles**.
2. Assign users and choose each user's role (**User** or **Admin**).

The application then appears on each assigned user's **App Store** page; the user installs it from
there, and it appears on their **Apps** page.
