# Building and Hosting an App in DKubeX Workspace with a Coding Agent

Once you have a coding agent running in DKubeX Workspace, you can have it build a web app and host
it straight from the workspace — reachable in the browser through the workspace's built-in reverse
proxy. This tutorial walks through it end to end using a **scientific calculator** as the worked
example, but the same flow builds and hosts any app.

You give the agent one prompt, it writes the app, you run it on a port, and you open it at your
workspace URL.

To get a coding agent set up first, see
[Using Claude Code in DKubeX Workspace with a Claude subscription](./using-claude-code-in-dkubex-workspace-with-a-claude-subscription.md)
or
[Using Claude Code in DKubeX Workspace with DKubeX or OpenRouter models](./using-claude-code-in-dkubex-workspace-with-dkubex-or-openrouter-models.md).

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

**nginx does *not* strip the `/workspace/<username>/<port>` prefix before forwarding.** It proxies
straight to `127.0.0.1:<port>` with the full path intact — your app receives requests for
`/workspace/<username>/<port>/...`, not `/...`. An app that only knows how to serve `/` will 404 on
every request through the public URL, even though `curl localhost:<port>/` works fine from inside
the workspace.

So both sides of your app must be **prefix-aware**:

- **Backend** — all API routes and the HTML-serving route must be mounted under the prefix path, so
  the server recognizes incoming requests. See [Rule 1](#rules-for-workspace-compatible-apps).
- **Frontend** — the page must load its assets (stylesheets, scripts, images) and navigate to other
  pages under the prefix. See [Rule 2](#rules-for-workspace-compatible-apps). A single inline page
  with no external assets can get by with relative URLs alone, but multi-page apps or apps that load
  separate asset files break without proper prefix configuration.

Getting either side wrong is the single most common reason a newly built app "works when I test it
locally but 404s in the browser."

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

## Step 2 — Build the app

Paste the prompt below into the agent. It creates the project directory and describes the whole app,
including the workspace-proxy rules the app must follow, so the agent builds something that works
behind the proxy on the first try.

```
mkdir -p ~/projects/scientific-calculator && cd ~/projects/scientific-calculator

Build a FastAPI scientific calculator web app. Requirements:

Backend (single app.py):
- Mount all routes under the workspace prefix — nginx does NOT strip it.
  Build PATH_PREFIX = "/workspace/{USERNAME}/{APP_PORT}" from the USERNAME
  environment variable (pre-configured by the platform) and an APP_PORT
  constant defined at the top of the file (the port you choose for your app),
  create an APIRouter(prefix=PATH_PREFIX), register every route on it (the
  /api/history routes and the HTML "/" route), and call
  app.include_router(router). Do NOT add path-stripping middleware.
- GET /api/history — return the last N saved calculations (id, expression,
  result, timestamp), most recent first
- POST /api/history — accepts { expression, result } and appends it to a
  JSON file at ~/.scientific-calculator.json (cap stored history at 200
  entries)
- DELETE /api/history — clear all saved history
- No other backend logic is needed — the calculator itself evaluates
  expressions entirely in the frontend (see below), the backend only
  persists history

Frontend (single inline HTML page served at /):
- Evaluate expressions with a HAND-WRITTEN recursive-descent parser in
  JavaScript — do NOT use eval() or new Function(). The parser must
  correctly handle:
  - Standard operator precedence: + - lowest, then * / %, then unary +/-,
    then ^ (exponentiation, right-associative, e.g. 2^3^2 = 512), then
    postfix ! (factorial), then parentheses
  - Functions: sin, cos, tan, asin, acos, atan, log (base 10), ln (natural
    log), sqrt, cbrt, abs, exp — each takes one parenthesized argument
  - Constants: pi, e
  - A DEG/RAD toggle that converts trig function arguments (and inverse trig
    results) between degrees and radians
  - Factorial (n!) must reject negative or non-integer input with a clear
    error
- Calculator UI:
  - A display showing the expression being typed and a live-updated result
    preview below it (recomputed on every keypress, best-effort — don't
    error out mid-typing)
  - Button grid: digits 0-9, decimal point, + - * / (as × ÷ symbols), ^
    (x^y), parentheses, %, backspace, clear (C), equals (=)
  - Scientific function buttons: sin, cos, tan, log, ln, sqrt (√), factorial
    (n!), pi (π), e
  - DEG/RAD toggle buttons, visually indicating which is active
  - Memory buttons: M+, M-, MR, MC, with a small indicator showing the
    current memory value when non-zero
  - Full keyboard support: digit and operator keys type into the
    expression, Enter/= evaluates, Backspace deletes the last character,
    Escape clears
  - On evaluating (=), POST the expression and formatted result to
    /api/history, then clear the input
  - A history panel alongside the calculator (or below it on narrow
    screens) showing past calculations, loaded from /api/history on page
    load — clicking a history entry re-inserts its expression into the
    display
  - A "Clear" button on the history panel that calls DELETE /api/history
  - Display errors (e.g. "Expected ')'", division by zero showing Infinity)
    inline in the result area without crashing the page
  - Dark/light theme via prefers-color-scheme
  - Add a <base href="{PATH_PREFIX}/"> tag in the HTML <head> and use
    RELATIVE URLs everywhere (fetch('api/history'), not '/api/history') so
    every request resolves under the workspace prefix
  - Responsive layout: history panel moves below the calculator on narrow
    screens
  - Bind to 0.0.0.0 on port 8505

Add a requirements.txt with fastapi, uvicorn, and pydantic.
```

## Step 3 — Install dependencies and run

The agent installs and starts the app for you in most cases. If not, run it yourself:

```bash
cd ~/projects/scientific-calculator
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python app.py
```

To keep it running after you close the agent terminal:

```bash
nohup ./.venv/bin/python app.py > app.log 2>&1 &
disown
```

## Step 4 — Access your app

Open a browser and go to your workspace URL, using the port the app binds to (`8505` for the
calculator):

```
https://<host>/workspace/<your-username>/8505/
```

For example:

```
https://dkubex.example.com/workspace/johndoe/8505/
```

## Step 5 — Try it

1. Open the calculator at your workspace URL.
2. Type `2^10` and press Enter — it should show `1024`.
3. Switch to DEG mode and type `sin(30)` — it should show `0.5`.
4. Try `5!` — it should show `120`.
5. Click `M+` after a result to store it, then `MR` later to recall it.
6. Click a past entry in the history panel to reinsert and re-run it.

## Extend it

Use the same agent to add features — describe them in plain language and the agent edits the files
in place. Restart the server to pick up changes (`Ctrl+C`, then re-run). For example:

```
Add support for hyperbolic functions (sinh, cosh, tanh)
Add a base conversion mode (binary/octal/hex) with bitwise operators
Add unit conversion (length, weight, temperature) as a second tab
Add a graphing mode that plots f(x) for a typed expression using inline SVG
Export calculation history as CSV
Add scientific notation formatting for very large/small results
```

## Rules for workspace-compatible apps

When you build a **different** app, include these rules in your prompt so the agent produces
something that works behind the workspace proxy.

1. **Mount backend routes under the workspace prefix — nginx doesn't strip it.** Every request your
   app receives arrives with the full path `/workspace/<user>/<port>/api/data`, not `/api/data`, so
   your backend must expect routes at that prefix. For FastAPI, use `APIRouter(prefix=…)` instead of
   defining routes directly on the app:

   ```python
   import os
   from fastapi import FastAPI, APIRouter
   from fastapi.responses import HTMLResponse

   APP_PORT = 8501  # the port your app binds to
   # USERNAME is pre-configured by the platform
   PATH_PREFIX = "/workspace/{}/{}".format(
       os.environ.get("USERNAME", "user"),
       APP_PORT,
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

   The app then natively serves at `/workspace/<user>/<port>/...` with no custom middleware. For
   Express, use `app.use(PATH_PREFIX, router)`; for Flask, use a `Blueprint` with `url_prefix`.

2. **Make the frontend prefix-aware too.** Your UI is served from `/workspace/<username>/<port>/`,
   not `/`, so every URL the browser loads — stylesheets, scripts, images, navigations, API calls —
   must resolve under that prefix. Two approaches:

   **Option A — `<base href>` tag** (simplest for single-file / inline apps). Set a `<base href>` in
   the `<head>` so the browser resolves all relative URLs from the prefix, then use relative URLs
   everywhere:

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

   **Option B — framework prefix config** (React, Vue, Vite, Next.js, etc.):

   | Framework | Setting |
   | --- | --- |
   | Vite | `base: '/workspace/user/port/'` in `vite.config.js` |
   | React Router | `<BrowserRouter basename="/workspace/user/port">` |
   | Vue Router | `createRouter({ history: createWebHistory('/workspace/user/port') })` |
   | Next.js | `basePath: '/workspace/user/port'` in `next.config.js` |

   What breaks without prefix configuration:

   | What | Wrong (absolute) | Right (relative, with base href or prefix) |
   | --- | --- | --- |
   | API fetch | `fetch('/api/data')` | `fetch('api/data')` |
   | Stylesheet | `<link href="/style.css">` | `<link href="style.css">` |
   | Script | `<script src="/app.js">` | `<script src="app.js">` |
   | Image | `<img src="/logo.png">` | `<img src="logo.png">` |
   | Navigation | `<a href="/about">` | `<a href="about">` |
   | CSS asset | `url('/fonts/icon.woff')` | `url('fonts/icon.woff')` |

   A single inline page (all HTML/CSS/JS in one file, no external assets) can work with just relative
   `fetch()` calls. The moment your app loads a separate stylesheet, script, or image, or has
   multi-page navigation, use one of the approaches above.

3. **Bind to `0.0.0.0`**, not `localhost` or `127.0.0.1` — nginx proxies from within the same pod
   but as a separate process.

4. **Avoid reserved ports.** These are already in use: `8080` (nginx), `9100` (app loader), `9001`
   (supervisord), `17681–17688` (terminal apps), `18443` (VS Code), `18888` (JupyterLab), `19000`
   (FileBrowser), `28789` (OpenClaw). Safe choices: `3000`, `5000`, `8000`, `8501`–`8510`, `9000`,
   or anything above `30000`.

5. **WebSockets work.** nginx passes `Upgrade`/`Connection` headers, so real-time apps work
   natively — the prefix handling in rules 1–2 just needs to apply to the WebSocket path too.

6. **Bundle all assets.** Inline CSS/JS or install packages locally; don't rely on external CDNs if
   the cluster is behind a firewall.

## Troubleshooting

- Nothing loads at the workspace URL: check `app.log` for a "port already in use" error and pick a
  different unreserved port (see rule 4), then update both the `port=...` in the app and the URL you
  visit.
- Works on `localhost:<port>` but 404s in the browser: the backend isn't serving under the workspace
  prefix — apply rule 1.
- Page loads but styles, scripts, or API calls 404: the frontend isn't prefix-aware — apply rule 2.
