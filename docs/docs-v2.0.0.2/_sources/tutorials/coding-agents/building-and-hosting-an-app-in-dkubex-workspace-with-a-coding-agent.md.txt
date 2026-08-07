# Building and Hosting an App in DKubeX Workspace with a Coding Agent

Once you have a coding agent running in DKubeX Workspace, you can have it build an app and host
it straight from the workspace — reachable in the browser through the workspace's built-in reverse
proxy. This tutorial walks through it end to end using a **data-analysis workbench** as the worked
example, but the same flow builds and hosts any app.

The flow is two steps. First you give the agent the workspace's app-hosting rules **once**, as
standing instructions. Then you describe your app in plain language — the agent applies the hosting
rules for you, so your app prompts stay focused on what the app does, not on how the proxy works.

To get a coding agent set up first, see
[Using Claude Code in DKubeX Workspace with a Claude subscription](./using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md)
or
[Using Claude Code in DKubeX Workspace with DKubeX or cloud provider models](./using-claude-code-in-dkubex-workspace-with-dkubex-or-cloud-provider-models.md).

## Prerequisites

- A running DKubeX Workspace.
- A coding agent set up in the workspace — Claude Code, Codex, OpenCode, Copilot CLI, Antigravity,
  Mistral Vibe, or Hermes. See the two tutorials linked above.

## How app hosting works

Every workspace has an **nginx reverse proxy**. When you start a web server on a port inside the
workspace, it becomes reachable at:

```
https://<host>/workspace/<username>/<port>/
```

One thing determines whether your app works through that URL:

:::{note}
**nginx does *not* strip the `/workspace/<username>/<port>` prefix before forwarding.** It proxies
straight to `127.0.0.1:<port>` with the full path intact — your app receives requests for
`/workspace/<username>/<port>/...`, not `/...`. An app that only knows how to serve `/` will 404 on
every request through the public URL, even though `curl localhost:<port>/` works fine from inside
the workspace.

So both sides of your app must be **prefix-aware** — the backend must mount its routes under the
prefix, and the frontend must load its assets and call its APIs under the prefix too. Getting either
side wrong is the single most common reason a newly built app "works when I test it locally but 404s
in the browser."

Rather than restate these rules in every app prompt, you load them once as standing instructions
(Step 2). The full rule set lives in a single file, `APP_HOSTING.md`, that the agent reads and
follows for everything it builds in the workspace.
:::

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

## Step 2 — Load the app-hosting rules as standing instructions

Give the agent the workspace's app-hosting rules before you ask it to build anything. Fetch the file
with `wget`, or paste its contents in directly if the workspace can't reach GitHub.

::::{tab-set}

:::{tab-item} Download with wget

Run this in the workspace terminal — or ask the agent to run it for you — to pull the rules file into
your home directory:

```bash
wget https://raw.githubusercontent.com/dkubeio/docs-site/app-hosting-example/APP_HOSTING.md
```

Then tell the agent to adopt it as standing instructions:

```
Read the file APP_HOSTING.md in my home directory. Treat it as your standing
instructions for hosting apps in this workspace — follow these rules for every
app you build here.
```

:::

:::{tab-item} Copy and paste

Paste the following directly into the agent — the framing line followed by the full rules:

````
Here are the app-hosting rules for this workspace. Treat them as your standing
instructions and follow them for every app you build here:

# Hosting Apps in Your DKubeX Workspace

This guide covers how app hosting works in this workspace, and the rules any
app needs to follow to work behind the workspace's reverse proxy — regardless
of which app you're building or which coding agent you use to build it.

## Prerequisites

- A running DKubeX Workspace
- A coding model deployed via SecureLLM (the platform configures agents automatically)

## How App Hosting Works

Every workspace has an nginx reverse proxy. When you start any web server on a
port inside the workspace, it becomes accessible at:

```
https://<host>/workspace/<username>/<port>/
```

**Important: nginx does NOT strip that prefix before forwarding to your app.**
It proxies straight to `127.0.0.1:<port>` with the full path intact — your app
receives requests for `/workspace/<username>/<port>/...`, not `/...`. An app
that only knows how to serve `/` will 404 on every real request through the
public URL, even though `curl localhost:<port>/` works fine from inside the
workspace.

This means both the **backend** and the **frontend** must be prefix-aware:

- **Backend:** All API routes and the HTML-serving route must be mounted
  under the prefix path so the server recognizes incoming requests — see
  Rule 1.
- **Frontend:** The HTML page must load all assets (stylesheets, scripts,
  images) and navigate to other pages using the correct prefix — see
  Rule 2. A single inline page with no external assets may work with just
  relative URLs, but multi-page apps or apps that load separate asset files
  will break without proper prefix configuration.

Getting either side wrong is the single most common reason a newly built app
"works when I test it locally but 404s in the browser."

---

## Step-by-Step: Build and Host Any App

### Step 1 — Open a Coding Agent

From the workspace launcher, click any agent card:

| Agent | Best for |
|-------|----------|
| **Claude Code** | Full-stack apps, complex logic |
| **Codex** | Quick prototyping, OpenAI models |
| **OpenCode** | Open-source model workflows |
| **Copilot** | GitHub-integrated development |
| **Antigravity** | Google model exploration |
| **Vibe** | Mistral-powered coding |
| **Hermes** | Nous Research models |

### Step 2 — Ask the Agent to Build Your App

Create a project directory first, then give the agent a prompt describing
your app. **Always include the rules below** in your prompt so the agent
builds something that actually works behind the proxy.

### Step 3 — Install Dependencies and Run

The agent will typically include install instructions. If not:

```bash
# Python apps
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python app.py

# Node.js apps
npm install
node server.js
```

Keep it running after closing the agent terminal:

```bash
nohup ./.venv/bin/python app.py > app.log 2>&1 &
disown
```

### Step 4 — Access Your App

Open a browser and go to:

```
https://<host>/workspace/<your-username>/<port>/
```

For example, if your app runs on port 8501:
```
https://dkubex.example.com/workspace/johndoe/8501/
```

---

## Rules for Workspace-Compatible Apps

These rules ensure your app works behind the workspace's nginx proxy. **Include
them in your prompt to the coding agent** so it builds the app correctly.

1. **Mount backend routes under the workspace prefix — nginx doesn't strip
   it.** Every request your app receives arrives with the full path:
   `/workspace/<user>/<port>/api/data`, not `/api/data`. Your backend must
   expect routes at that prefix.

   For FastAPI, use `APIRouter(prefix=...)` instead of defining routes
   directly on the app:

   ```python
   import os
   from fastapi import FastAPI, APIRouter

   # Build prefix from workspace env vars (pre-configured by the platform)
   PATH_PREFIX = "/workspace/{}/{}".format(
       os.environ.get("USERNAME", "user"),
       os.environ.get("APP_PORT", "8501"),
   )

   app = FastAPI()
   router = APIRouter(prefix=PATH_PREFIX)

   @router.get("/api/data")
   async def get_data():
       return {"items": []}

   # Serve the HTML page under the prefix too
   @router.get("/")
   async def index():
       return HTMLResponse(html_content)

   app.include_router(router)
   ```

   This way the app natively serves at `/workspace/<user>/<port>/...` with
   no custom middleware. For Express, use `app.use(PATH_PREFIX, router)`;
   for Flask, use `Blueprint` with `url_prefix`. Tell your coding agent to
   use this pattern explicitly — it's easy to skip if you only test against
   `localhost:<port>` directly, since that always works regardless.

2. **Frontend must also be prefix-aware.** Your app's UI is served from
   `/workspace/<username>/<port>/`, not `/`. Every URL the browser loads —
   stylesheets, scripts, images, page navigations, API calls — must resolve
   under that prefix. There are two approaches:

   **Option A — `<base href>` tag (simplest for single-file / inline apps):**

   Set a `<base href>` in your HTML `<head>` so the browser resolves all
   relative URLs from the prefix path:

   ```html
   <base href="/workspace/johndoe/8501/">
   ```

   Then use relative URLs everywhere — `fetch('api/data')`, `<link
   href="style.css">`, `<img src="logo.png">`, `<a href="about">`.

   For a FastAPI app, inject the prefix dynamically so it works for any
   user/port:

   ```python
   html_content = f"""
   <html>
   <head><base href="{PATH_PREFIX}/"></head>
   <body>
     <link href="style.css" rel="stylesheet">
     <script src="app.js"></script>
     <img src="images/logo.png">
   </body>
   </html>
   """
   ```

   **Option B — Framework prefix config (for React, Vue, Vite, etc.):**

   | Framework | Setting |
   |-----------|---------|
   | Vite | `base: '/workspace/user/port/'` in `vite.config.js` |
   | React Router | `<BrowserRouter basename="/workspace/user/port">` |
   | Vue Router | `createRouter({ history: createWebHistory('/workspace/user/port') })` |
   | Next.js | `basePath: '/workspace/user/port'` in `next.config.js` |

   **What breaks without prefix configuration:**

   | What | Wrong (absolute) | Right (relative, with base href or prefix) |
   |------|-------------------|---------------------------------------------|
   | API fetch | `fetch('/api/data')` | `fetch('api/data')` |
   | Stylesheet | `<link href="/style.css">` | `<link href="style.css">` |
   | Script | `<script src="/app.js">` | `<script src="app.js">` |
   | Image | `<img src="/logo.png">` | `<img src="logo.png">` |
   | Navigation | `<a href="/about">` | `<a href="about">` |
   | CSS asset | `url('/fonts/icon.woff')` | `url('fonts/icon.woff')` |

   A single inline page (all HTML/CSS/JS in one file, no external assets)
   may work with just relative `fetch()` calls. But the moment your app
   loads a separate stylesheet, script, image, or has multi-page navigation,
   you need one of the prefix approaches above.

3. **Bind to `0.0.0.0`**, not `localhost` or `127.0.0.1` — nginx proxies from
   within the same pod but as a separate process.

4. **Avoid reserved ports.** These are already in use:
   - `8080` — nginx (the public entry point)
   - `9100` — app loader
   - `9001` — supervisord API
   - `17681–17688` — built-in terminal apps
   - `18443` — VS Code
   - `18888` — JupyterLab
   - `19000` — FileBrowser
   - `28789` — OpenClaw

   Safe choices: `3000`, `5000`, `8000`, `8501`–`8510`, `9000`, or anything above `30000`.

5. **WebSockets work.** nginx passes `Upgrade`/`Connection` headers, so
   real-time apps (chat, live dashboards, hot-reload) work natively — no
   special handling needed beyond rule 1 applying to the WebSocket path too.

6. **Bundle all assets.** Inline CSS/JS or install packages locally. Don't rely
   on external CDNs if the cluster is behind a firewall.

---

## Iterating with the Agent

Once the app is running, use the same agent to extend it — describe the new
feature in plain language, e.g. "Add a search bar that filters tasks by
title." The agent edits files in place. Restart the server to pick up
changes (`Ctrl+C` then re-run), or use a framework with hot-reload.
````

:::

::::

The agent now knows how the workspace proxy works. From here on, describe apps in plain language and
it will build them prefix-aware without you having to spell the rules out again.

## Step 3 — Build the app

With the hosting rules loaded, prompt and converse with your coding agent to build your app —
describe what you want in plain language and iterate as you go. Because the agent already has the
hosting rules from Step 2, your prompts stay focused on what the app does, not on the proxy, prefix,
or port. For example, this prompt builds a DuckDB data-analysis workbench:

```
mkdir -p ~/projects/data-workbench && cd ~/projects/data-workbench

Build a FastAPI data-analysis workbench web app powered by DuckDB. Requirements:

Backend (single app.py, using an in-process DuckDB database):
- Dataset upload: accept a CSV or Parquet file upload and load it into a
  DuckDB table named "dataset" (replacing any previous one), using DuckDB's
  native read_csv_auto / read_parquet. Save the uploaded file under
  ~/.data-workbench/datasets/ so it can be reloaded later. Return the inferred
  schema (column names + types) and the row count.
- Recent datasets: list previously uploaded datasets from that folder and
  allow reloading one by name.
- Schema: return the current dataset's columns and DuckDB types.
- Profiling: for the current dataset, compute per-column stats via SQL —
  data type, non-null count, null %, distinct count; for numeric columns also
  min / max / mean / stddev / median (approx quantile); for text columns the
  top 5 most frequent values with counts.
- Correlation: compute a Pearson correlation matrix across the numeric
  columns (DuckDB corr()), returned as a matrix for heatmap rendering.
- SQL query: accept an arbitrary SQL string, run it against the DuckDB
  database, and return column names + rows. Cap returned rows at 500 and also
  return the total row count. Return any SQL error as a normal JSON field
  (do NOT return a 500) so the UI can show it inline.
- Chart data: given a chart type (histogram, scatter, or line) and the
  relevant column(s), return the aggregated data points computed in DuckDB —
  equal-width bins + counts for a histogram, x/y pairs for scatter, ordered
  x/y for a line chart.
- Query history: persist executed queries (text + timestamp) to a JSON file
  at ~/.data-workbench/history.json (cap 200), with endpoints to list and
  clear it.
- CSV export: return the current query's result set as a downloadable CSV.

Frontend (single inline HTML page):
- Panels: a Dataset panel (drag-and-drop upload for CSV/Parquet, current
  schema, and a list of recent datasets to reload); a SQL console (multiline
  editor + Run button, results in a sortable, paginated table, inline error
  display, and an Export CSV button); a Profile view (per-column stats table);
  a Correlation view (numeric-column heatmap); and a Chart builder (pick chart
  type + columns and render the returned data).
- Render every chart and the correlation heatmap as HAND-WRITTEN inline SVG —
  do NOT load any charting library or external CDN.
- Ctrl/Cmd+Enter runs the SQL query.
- A query-history panel listing recent queries; clicking one loads it back
  into the editor; a Clear button empties the history.
- Show friendly errors (bad SQL, unsupported file) inline without crashing
  the page.
- Dark/light theme via prefers-color-scheme; responsive layout.

Serve the app on port 8506.

Add a requirements.txt with fastapi, uvicorn, duckdb, pyarrow, and
python-multipart.
```

:::{admonition} If the app isn't running
:class: note

The agent installs and starts the app for you in most cases. If not, run it yourself:

```bash
cd ~/projects/data-workbench
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python app.py
```

To keep it running after you close the agent terminal:

```bash
nohup ./.venv/bin/python app.py > app.log 2>&1 &
disown
```
:::

## Step 4 — Access your app

Open a browser and go to your workspace URL, using the port the app binds to (`8506` for the
workbench):

```
https://<host>/workspace/<your-username>/<port>/
```

For example:

```
https://dkubex.example.com/workspace/johndoe/8506/
```
