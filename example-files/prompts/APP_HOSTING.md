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
