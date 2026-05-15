# Contributing Application Documentation

This is the **central user-facing documentation site** for DKubeX applications. As a contributor, you do **not** edit files in this repository directly. Instead:

- You write and maintain your documentation in **your own component repo**.
- A GitHub Action automatically publishes your public docs to this site on every push to your repo's `main` branch.

This guide walks you through setting that action up and structuring your docs so they render correctly here.

---

## What to publish (scope policy)

This docs site is the **user guide** for DKubeX applications. Only user-facing documentation belongs here.

**Publish these:**

- `index.md` — your application's homepage. Describes what the app is, what it does, and what its main components and features are. Contains a `toctree` that links to the other published pages.
- Tutorials and how-to guides — task-oriented pages explaining how an end user actually uses the application.

**Do not publish these** (keep them in your component repo, outside `docs/public/`):

- API references.
- Developer guides, contributor docs, internal architecture deep-dives.
- Build, deploy, or operations runbooks aimed at engineers, not end users.

Rule of thumb: if an end user reading the product documentation needs the page, publish it. If it's for someone *building or operating* the application internally, keep it out.

---

## Prerequisites

- The docs GitHub App credentials (App ID and Private Key) are provided to you by the platform team.
- Your component repo is on GitHub.
- You have admin access to add secrets to your repo.

---

## Step 1 — Add secrets to your component repo

In your component repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DOCS_APP_ID` | Provided by the platform team |
| `DOCS_APP_PRIVATE_KEY` | Provided by the platform team |

---

## Step 2 — Add the GitHub Action to your component repo

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

Replace `my-component` with your application's slug (kebab-case, unique across all components — e.g. `auth-service`, `mortgage-lite`).

---

## Step 3 — Organize your component repo's docs

Only files under `docs/public/` are published. Keep private, internal, or developer-only docs anywhere else in your repo (e.g. `docs/internal/`, `docs/api/`).

### Folder layout

Keep all of your published markdown files **flat** under `docs/public/`. Do not nest tutorials in a subfolder — it just adds an extra `index.md` step. The only subdirectory inside `docs/public/` is `media/`.

```
docs/
├── public/                    # ← Published to docs-site
│   ├── index.md               # Application homepage (required)
│   ├── getting-started.md     # Tutorial
│   ├── advanced-usage.md      # Tutorial
│   ├── configuration.md       # Tutorial
│   └── media/                 # All binary assets — icons, screenshots, diagrams, videos
│       ├── icon.svg
│       ├── screenshot.png
│       └── demo.mp4
└── internal/                  # Never published
    ├── api-reference.md
    ├── architecture-notes.md
    └── runbook.md
```

### Application homepage (`index.md`)

Your `index.md` is the homepage for your application's section of the docs site. It is required.

It must:

- Use an appropriate top-level heading for your application.
- Describe what the application is, what it does, and what its main components and features are.
- Include a **visible "Tutorials" section** (or similarly named section) with markdown links to every other published page, so users can discover them directly from the page body.
- Include a **hidden `toctree`** that lists those same pages so Sphinx can build the sidebar navigation, breadcrumbs, and previous/next links.

Sample homepage template:

````markdown
# My Application

My Application is a … (one-paragraph description of what the app is and does).

## Key features

- Feature one — short description.
- Feature two — short description.

## Tutorials

- [Getting started](./getting-started.md) — install and run your first workflow.
- [Advanced usage](./advanced-usage.md) — common patterns and tips.
- [Configuration](./configuration.md) — every option you can set.

```{toctree}
:hidden:

getting-started
advanced-usage
configuration
```
````

Notes:

- The visible "Tutorials" section and the hidden `toctree` should list the **same** pages — the visible section is what users click; the hidden toctree is what Sphinx uses to build navigation.
- List pages without `.md` in `toctree` entries.
- Paths in the `toctree` are relative to your `index.md`.

### Images

Put every image into `docs/public/media/` and reference it with a path **relative to the markdown file** where the image appears.

Examples:

```markdown
# From docs/public/index.md
![Architecture](./media/architecture.png)

# From docs/public/advanced-usage.md
![Architecture](./media/architecture.png)
```

If the relative path to `media/` is wrong, the image will not render.

Supported image formats: `.png`, `.jpg`/`.jpeg`, `.svg`, `.webp`, `.gif`.

### Videos and other media

`media/` is **not just for images** — it is the single home for any binary asset referenced by your docs: icons, screenshots, diagrams, and videos.

To embed a video, use the MyST `{video}` directive (provided by `sphinxcontrib-video`, already enabled on this site):

````markdown
```{video} ./media/demo.mp4
:width: 100%
```
````

Supported options include `:autoplay:`, `:loop:`, `:muted:`, `:poster:`, `:width:`, `:height:`, and `:nocontrols:`.

Recommended video formats: `.mp4` (H.264) for broad browser support, or `.webm`.

---

## Where your content lands in docs-site

When the action runs, every component lands in a single, self-contained folder:

| Source in your component repo | Destination in docs-site |
| --- | --- |
| `docs/public/*.md` (and any subdirectories) | `applications/<component-slug>/*.md` |
| `docs/public/media/*` | `applications/<component-slug>/media/*` |

The action **wipes `applications/<component-slug>/` completely before each push**, so removing a file from your `docs/public/` removes it from the published site on the next push.

---

## Notes

- **`component-slug`**: Must be unique across all component repos (kebab-case recommended). New slugs are picked up automatically — as soon as your first push includes an `index.md`, your component appears in the site navigation. No manual registration is required.
- **`pr-enabled`**: Set to `"true"` in your workflow if you want the action to open a PR for review on docs-site instead of pushing directly to `main`.
- **Only `docs/public/` is published** — anything outside that directory stays private in your repo.
- Pushes to docs-site's `main` branch automatically trigger a documentation build and live-site deploy.
