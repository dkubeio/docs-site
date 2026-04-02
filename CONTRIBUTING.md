# Contributing Component Documentation

This guide explains how to publish documentation from your component repo to the central docs-site.

## Prerequisites

- The docs GitHub App credentials (App ID and Private Key) are provided to you by the platform team
- Your component repo is on GitHub
- You have admin access to add secrets to your repo

## Step 1: Add Secrets to Your Component Repo

In your component repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DOCS_APP_ID` | Provided by the platform team |
| `DOCS_APP_PRIVATE_KEY` | Provided by the platform team |

## Step 2: Add GitHub Action to Your Component Repo

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
        uses: dkubeio/docs-site/.github/actions/push-docs@main
        with:
          component-slug: "my-component"
          public-docs-dir: "docs/public"
          public-media-dir: "docs/public/media"
          docs-target-repo: "https://github.com/dkubeio/docs-site"
          app-id: ${{ secrets.DOCS_APP_ID }}
          app-private-key: ${{ secrets.DOCS_APP_PRIVATE_KEY }}
          pr-enabled: "false"
```

## Step 3: Organize Your Docs

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
