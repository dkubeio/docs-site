# Building and Hosting an App in DKubeX Workspace with a Coding Agent

Once you have a coding agent running in DKubeX Workspace, you can have it build a web app and host
it straight from the workspace — reachable in the browser through the workspace's built-in reverse
proxy. This tutorial walks through it end to end using a **scientific calculator** as the worked
example, but the same flow builds and hosts any app.

The flow is two steps. First you give the agent the workspace's app-hosting rules **once**, as
standing instructions. Then you describe your app in plain language — the agent applies the hosting
rules for you, so your app prompts stay focused on what the app does, not on how the proxy works.

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

So both sides of your app must be **prefix-aware** — the backend must mount its routes under the
prefix, and the frontend must load its assets and call its APIs under the prefix too. Getting either
side wrong is the single most common reason a newly built app "works when I test it locally but 404s
in the browser."

Rather than restate these rules in every app prompt, you load them once as standing instructions
(Step 2). The full rule set lives in a single file, `APP_HOSTING.md`, that the agent reads and
follows for everything it builds in the workspace.

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

If the workspace can't reach GitHub, open
[`APP_HOSTING.md`](https://raw.githubusercontent.com/dkubeio/docs-site/app-hosting-example/APP_HOSTING.md)
in your browser, copy its full contents, and paste them into the agent with this framing:

```
Here are the app-hosting rules for this workspace. Treat them as your standing
instructions and follow them for every app you build here:

<paste the full contents of APP_HOSTING.md here>
```

:::

::::

The agent now knows how the workspace proxy works. From here on, describe apps in plain language and
it will build them prefix-aware without you having to spell the rules out again.

## Step 3 — Build the app

With the hosting rules loaded, paste the prompt below into the agent. Notice it describes only what
the calculator *does* — no proxy, prefix, or port-binding instructions — because the agent already
has those from Step 2.

```
mkdir -p ~/projects/scientific-calculator && cd ~/projects/scientific-calculator

Build a FastAPI scientific calculator web app. Requirements:

Backend (single app.py):
- GET /api/history — return the last N saved calculations (id, expression,
  result, timestamp), most recent first
- POST /api/history — accepts { expression, result } and appends it to a
  JSON file at ~/.scientific-calculator.json (cap stored history at 200
  entries)
- DELETE /api/history — clear all saved history
- No other backend logic is needed — the calculator itself evaluates
  expressions entirely in the frontend (see below), the backend only
  persists history

Frontend (single inline HTML page):
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
  - Responsive layout: history panel moves below the calculator on narrow
    screens

Serve the app on port 8505.

Add a requirements.txt with fastapi, uvicorn, and pydantic.
```

## Step 4 — Install dependencies and run

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

## Step 5 — Access your app

Open a browser and go to your workspace URL, using the port the app binds to (`8505` for the
calculator):

```
https://<host>/workspace/<your-username>/8505/
```

For example:

```
https://dkubex.example.com/workspace/johndoe/8505/
```

## Step 6 — Try it

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

## Building other apps

The scientific calculator is just the worked example. To build anything else, keep the same
two-step flow: load `APP_HOSTING.md` as standing instructions once (Step 2), then describe your app
in plain language (Step 3). Because the hosting rules already live in the agent's context, your app
prompts stay focused on what the app does — the agent applies the proxy, prefix, port, and asset
rules for you.

To see exactly what those rules are — the nginx prefix, prefix-aware backend and frontend, binding
to `0.0.0.0`, reserved ports, WebSockets, and asset bundling — read
[`APP_HOSTING.md`](https://raw.githubusercontent.com/dkubeio/docs-site/app-hosting-example/APP_HOSTING.md)
directly.

## Troubleshooting

- Nothing loads at the workspace URL: check `app.log` for a "port already in use" error and pick a
  different unreserved port (see the reserved-ports rule in `APP_HOSTING.md`), then update both the
  `port=...` in the app and the URL you visit.
- Works on `localhost:<port>` but 404s in the browser: the backend isn't serving under the workspace
  prefix — re-check that the agent applied Rule 1 from `APP_HOSTING.md`.
- Page loads but styles, scripts, or API calls 404: the frontend isn't prefix-aware — re-check
  Rule 2 from `APP_HOSTING.md`.
