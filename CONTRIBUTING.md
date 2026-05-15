# Contributing Application Documentation

This repository is the **central user-facing documentation site** for DKubeX applications. There are two ways content lands here:

1. **Section 1 — Editing in this repository**: a contributor edits markdown directly under `applications/` and opens a PR.
2. **Section 2 — Publishing from a component repo**: a component team's repo publishes its public docs to this site automatically via a GitHub Action.

Both flows write into the **same** target layout: each application has a single folder under `applications/<your-application>/` with all its markdown files at the top level, and a nested `media/` subfolder containing every binary asset (icons, screenshots, diagrams, videos) referenced by those pages.

---

## Section 1 — Editing docs in this repository

Use this flow if you are editing application documentation directly in this repo (e.g. fixing a typo, restructuring a guide, authoring content that does not come from a component repo).

### Contribution scope

- Add or update docs only inside `applications/`.
- Each application must have its own subfolder.

### Required folder structure

For every application, create this structure first:

```text
applications/
  <your-application>/
    index.md
    media/
```

Example:

```text
applications/
  mortgage-lite/
    index.md
    media/
```

### Image guidelines

- Store all images for your application inside that application's `media/` folder.
- In every markdown file, the image link path must correctly point to your application's `media/` folder.
- The path is always relative to the markdown file where you add the image link.

Examples:

```markdown
# From applications/my-app/index.md
![Architecture](./media/architecture.png)

# From applications/my-app/guides/setup.md
![Architecture](../media/architecture.png)
```

If the path to `media/` is wrong, the image will not render in the docs.

### Videos and other media

`media/` is **not just for images** — it is the single per-application home for any binary asset referenced by the docs: icons, screenshots, diagrams, and videos.

To embed a video, use the MyST `{video}` directive (provided by `sphinxcontrib-video`):

````markdown
```{video} ./media/demo.mp4
:width: 100%
```
````

The directive supports options like `:autoplay:`, `:loop:`, `:muted:`, `:poster:`, `:width:`, `:height:`, and `:nocontrols:`.

Recommended formats:
- Video: `.mp4` (H.264) for broad browser support, or `.webm`.
- Images: `.png`, `.jpg`/`.jpeg`, `.svg`, `.webp`, `.gif`.

### Application homepage requirements

Your `index.md` is the homepage for your application documentation.

It must:

- Use an appropriate top-level heading for your application.
- Describe what the application is, what it does, and what its main components/features are.
- Link to your other documentation pages through a `toctree` on the `index.md` page.

Sample homepage `toctree` template:

````markdown
```{toctree}
:maxdepth: 2
:caption: Contents

getting-started
tutorials/quickstart
tutorials/advanced-usage
```
````

Notes:

- List pages without `.md` in `toctree` entries.
- Paths are relative to your `index.md`.

### Update the applications toctree

After creating your application folder, you must add your app index to the toctree in `applications/index.md`.

Add one line in the toctree block:

```text
<your-application>/index
```

Example:

```text
securellm/index
```

### Checklist before commit

- Application folder exists under `applications/`.
- `index.md` exists in your application folder.
- `media/` folder exists in your application folder.
- All binary assets are stored in your local `media/` folder and linked with correct relative paths.
- Your application `index.md` includes a `toctree` that references your pages.
- `applications/index.md` includes `<your-application>/index`.

---

## Section 2 — Publishing docs from a component repo

Use this flow if you maintain a **component repo** (e.g. `dkubeio/<your-component>`) and want its documentation to be published to this docs site automatically on every push to your repo's `main` branch.

### What to publish (scope policy)

This docs site is the **user guide** for DKubeX applications. Only user-facing documentation belongs here.

**Publish these:**
- `index.md` — your application's homepage. Describes what the app is, what it does, and its main components/features. Contains a `toctree` linking to the other published pages.
- Tutorials and how-to guides — task-oriented pages explaining how an end user actually uses the application.

**Do not publish these** (keep them in your component repo, outside `docs/public/`):
- API references.
- Developer guides, contributor docs, internal architecture deep-dives.
- Build/deploy runbooks aimed at engineers, not end users.

Rule of thumb: if an end user reading the product documentation needs the page, publish it. If it's for someone *building or operating* the application internally, keep it out.

### Prerequisites

- The docs GitHub App credentials (App ID and Private Key) are provided to you by the platform team.
- Your component repo is on GitHub.
- You have admin access to add secrets to your repo.

### Step 1 — Add secrets to your component repo

In your component repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `DOCS_APP_ID` | Provided by the platform team |
| `DOCS_APP_PRIVATE_KEY` | Provided by the platform team |

### Step 2 — Add the GitHub Action workflow to your component repo

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

### Step 3 — Organize your component repo's docs

Only files under `docs/public/` are published. Keep private, internal, or developer-only docs anywhere else in your repo (e.g. `docs/internal/`, `docs/api/`).

```
docs/
├── public/                    # ← Published to docs-site
│   ├── index.md               # Application homepage with toctree
│   ├── getting-started.md     # Tutorial
│   ├── tutorials/
│   │   └── advanced-usage.md
│   └── media/                 # Icons, screenshots, diagrams, videos
│       ├── icon.svg
│       ├── screenshot.png
│       └── demo.mp4
└── internal/                  # Never published
    ├── api-reference.md
    ├── architecture-notes.md
    └── runbook.md
```

In markdown, reference media with relative paths from each doc file:

```markdown
![Screenshot](./media/screenshot.png)
```

For videos, use the `{video}` directive (see Section 1 — "Videos and other media").

### Where your content lands in this repo

When the action runs, it writes to a **single** folder per component:

| Source in your component repo | Destination in docs-site |
| --- | --- |
| `docs/public/*.md` (and subdirectories) | `applications/<component-slug>/*.md` |
| `docs/public/media/*` | `applications/<component-slug>/media/*` |

The action wipes `applications/<component-slug>/` completely before each push, so removing a file from your `docs/public/` removes it from the published site on the next push.

### Notes

- **`component-slug`**: Must be unique across all component repos (kebab-case recommended, e.g. `auth-service`, `mortgage-lite`).
- **`pr-enabled`**: Set to `"true"` if you want the action to open a PR for review instead of pushing directly to `main`.
- **Only `docs/public/` is published** — anything outside that directory stays private in your repo.
- Changes pushed to docs-site's `main` branch automatically trigger a documentation build and deploy.
