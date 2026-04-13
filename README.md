# DKubeX 2.0 Documentation

<p align="right">
  <a href="#developer-cheatsheet">
    <img alt="Developer Cheatsheet" src="https://img.shields.io/static/v1?label=&message=Developer%20Cheatsheet&color=0A66C2&style=for-the-badge" />
  </a>
</p>

This repository hosts the DKubeX 2.0 multi-version documentation platform, built on Sphinx.

## Overview

The platform provides a structured workflow for versioned documentation delivery:
- Build all documentation sources from folders matching `raw-v*`.
- Generate immutable outputs per version at `docs-vX.Y` (repository root).
- Maintain `docs` (repository root) as the canonical documentation homepage.
- Publish generated artifacts to the `site-files` branch through GitHub Actions.

## Architecture

1. Versioned source model:
- Each source version is maintained in a dedicated top-level folder such as `raw-v0.1`.

2. Shared configuration model:
- Shared Sphinx logic is centralized in `conf_main.py`.
- Each source version keeps a local `conf.py` wrapper that sets only `doc_version`.
- This model preserves per-version identity while minimizing configuration drift.

3. Latest-homepage model:
- The highest semantic version is automatically treated as `Latest`.
- The system builds that version again to `docs`.
- Primary reader entry point: `docs/index.html`.

## Repository Structure

- `.github/workflows/build.yml`: build and publishing workflow.
- `conf_main.py`: shared configuration builder.
- `raw-v*/***.md`: documentation source pages.
- `raw-v*/conf.py`: per-version source configuration wrappers.
- `docs-v*/`: generated per-version HTML output at repository root.
- `docs/`: generated latest HTML output at repository root.

## Prerequisites

- Python 3.11 or newer.
- Dependencies installed from `requirements.txt`.

## Local Development Workflow

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Build all versions and refresh latest:

```bash
rm -rf docs 'docs-v*' CNAME && SRC_DIRS="$(find . -maxdepth 1 -type d -name 'raw-v*' -print | sed 's|^\./||' | sort -V)" && [ -n "$SRC_DIRS" ] && printf '%s\n' "$SRC_DIRS" | while IFS= read -r SRC_DIR; do VERSION="${SRC_DIR#raw-}"; python -m sphinx -b html -W --keep-going "$SRC_DIR" "docs-$VERSION"; done && LATEST_SRC="$(printf '%s\n' "$SRC_DIRS" | tail -n1)" && python -m sphinx -b html -W --keep-going "$LATEST_SRC" docs
```

3. Validate the homepage first:
- `docs/index.html`

4. Optional direct version links:
- `docs-v0.1/index.html`

## Adding a New Version

Example: create `v0.2` from `v0.1`.

1. Duplicate an existing version folder:

```bash
cp -R raw-v0.1 raw-v0.2
```

2. Update `doc_version` in `raw-v0.2/conf.py` to `v0.2`.

3. Update content files under `raw-v0.2/`.

4. Re-run the full build.

Expected outcomes:
- `docs-v0.2` is generated.
- `docs` is regenerated from `v0.2`.
- Version navigation marks `v0.2` as latest.

## Removing an Existing Version

To remove specific versions from both source and local generated output, use:

```bash
for VERSION in v0.2 v0.3 v0.4; do rm -rf "raw-$VERSION" "docs-$VERSION"; done
```

## CI Workflow Summary

Workflow file: `.github/workflows/build.yml`

Current implemented behavior on push to `main` (for docs/workflow changes):
1. Install dependencies.
2. Build all `raw-v*` sources to `docs-v*`.
3. Rebuild highest source version to `docs`.
4. Upload site artifact.
5. Publish generated output to `site-files` branch.

Pages and custom domain delivery:
- This workflow does not execute a separate GitHub Pages deploy action.
- Delivery is expected through repository Pages configuration using `site-files` as the published source.

## Troubleshooting

1. `sphinx-build: command not found`:
- Activate the virtual environment.
- Alternatively use `python -m sphinx ...` commands.

2. Unexpected latest version selection:
- Confirm semantic folder naming (for example, `raw-v1.0` > `raw-v0.9`).

3. New version not listed in navigation:
- Confirm folder naming matches `raw-v*` at repository root.
- Rebuild after creating or updating the folder.

## Developer Cheatsheet

Setup:

```bash
python3 -m venv .venv-docs && source .venv-docs/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Build all versions + latest:

```bash
rm -rf docs 'docs-v*' CNAME && SRC_DIRS="$(find . -maxdepth 1 -type d -name 'raw-v*' -print | sed 's|^\./||' | sort -V)" && [ -n "$SRC_DIRS" ] && printf '%s\n' "$SRC_DIRS" | while IFS= read -r SRC_DIR; do VERSION="${SRC_DIR#raw-}"; python -m sphinx -b html -W --keep-going "$SRC_DIR" "docs-$VERSION"; done && LATEST_SRC="$(printf '%s\n' "$SRC_DIRS" | tail -n1)" && python -m sphinx -b html -W --keep-going "$LATEST_SRC" docs
```

Open homepage (`docs`):

```bash
open docs/index.html
```

Add new version (example `v0.2` from `v0.1`):

```bash
cp -R raw-v0.1 raw-v0.2 && sed -i '' 's/doc_version="v0.1"/doc_version="v0.2"/' raw-v0.2/conf.py
```

Remove versions (example remove `v0.2`, `v0.3`, `v0.4`):

```bash
for VERSION in v0.2 v0.3 v0.4; do rm -rf "raw-$VERSION" "docs-$VERSION"; done
```
