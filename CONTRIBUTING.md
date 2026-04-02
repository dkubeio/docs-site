# Contributing Component Documentation

This guide explains how to connect a component repo to the central docs-site so that its documentation is automatically published.

## Prerequisites

- Your component repo is on GitHub
- You have admin access to install the GitHub App

## Step 1: Create a GitHub App

1. Go to **Settings → Developer settings → GitHub Apps → New GitHub App**
2. Configure:
   - **Name**: `Docs Publisher` (or similar)
   - **URL**: URL of your docs site
   - **Webhook**: Uncheck "Active" (not needed)
   - **Permissions → Repository permissions**:

     | Permission | Access |
     |------------|--------|
     | Contents   | Read & Write |

   - **Where can this GitHub App be installed?**: Check "Any account"

3. After creating the app, note:
   - **App ID** (from settings page)
   - **Private Key** — click "Generate a private key" and download the `.pem` file

4. **Install the app** on the `docs-site` repo

## Step 2: Add Secrets to Your Component Repo

In your component repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DOCS_APP_ID` | The App ID from Step 1 |
| `DOCS_APP_PRIVATE_KEY` | Contents of the `.pem` file (include the full key with `BEGIN`/`END` lines) |

## Step 3: Add GitHub Action to Your Component Repo

Create `.github/workflows/push-docs.yml` in your component repo:

```yaml
name: Push Component Docs

on:
  push:
    branches: [main]
    paths:
      - "docs/public/**"

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Push docs
        uses: your-org/docs-site/.github/actions/push-docs@main
        with:
          component-slug: "my-component"
          public-docs-dir: "docs/public"
          public-media-dir: "docs/public/media"
          docs-target-repo: "https://github.com/your-org/docs-site"
          app-id: ${{ secrets.DOCS_APP_ID }}
          app-private-key: ${{ secrets.DOCS_APP_PRIVATE_KEY }}
          pr-enabled: "false"
```

## Step 4: Organize Your Docs

Only files under `docs/public/` are published. Keep private or internal docs elsewhere (e.g., `docs/internal/`).

```
docs/
├── public/                    # Published to docs-site
│   ├── getting-started.md
│   ├── api-reference.md
│   └── media/
│       ├── screenshot-1.png
│       └── diagram.svg
└── internal/                  # Never published
    ├── architecture-notes.md
    └── runbook.md
```

In markdown, reference media with relative paths from the doc file:

```markdown
![Screenshot](./media/screenshot-1.png)
```

The action copies `.md` files from `docs/public/` to `docs/components/<slug>/` and media files to `public/media/<slug>/`, preserving subdirectory structure.

## Notes

- **`component-slug`**: Must be unique across all component repos (kebab-case recommended, e.g., `auth-service`, `ui-button`)
- **`pr-enabled`**: Set to `"true"` if you want the action to open a PR for review instead of pushing directly to `main`
- **Only `docs/public/` is published** — anything outside that directory stays private in your repo
- Changes are pushed to the docs-site repo's `main` branch, which triggers an automatic deploy to GitHub Pages
