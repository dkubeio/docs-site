# DKubeX Documentation

<p align="right">
  <a href="#developer-cheatsheet">
    <img alt="Developer Cheatsheet" src="https://img.shields.io/static/v1?label=&message=Developer%20Cheatsheet&color=0A66C2&style=for-the-badge" />
  </a>
</p>

This repository hosts the DKubeX documentation site, built on Sphinx.

## Overview

The current workflow is intentionally single-version:
- Keep documentation source files at repository root.
- Build output directly into `docs/`.
- Publish generated output to the `site-files` branch through GitHub Actions.

## Architecture

1. Single source model:
- Source content is maintained directly at repository root (`*.md`, `applications/`, `images/`, `_static/`, `_templates/`).

2. Shared configuration model:
- Root `conf.py` is the single combined Sphinx configuration.

3. Output model:
- Build target is `docs/`.
- Primary reader entry point: `docs/index.html`.

## Repository Structure

- `.github/workflows/build.yml`: build and publishing workflow.
- `conf.py`: active Sphinx configuration entrypoint.
- `*.md`, `applications/**`, `images/**`, `_static/**`, `_templates/**`: source files.
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

2. Build documentation:

```bash
rm -rf docs && python -m sphinx -E -b html -W --keep-going . docs
```

3. Validate the homepage first:
- `docs/index.html`

4. Open the generated site:
- `docs/index.html`

## CI Workflow Summary

Workflow file: `.github/workflows/build.yml`

Current implemented behavior on push to any branch (for docs/workflow changes):
1. Install dependencies.
2. Build repository-root sources to `docs`.
3. Upload site artifact.
4. Publish generated output to `site-files` branch.

Pages and custom domain delivery:
- This workflow does not execute a separate GitHub Pages deploy action.
- Delivery is expected through repository Pages configuration using `site-files` as the published source.

## Troubleshooting

1. `sphinx-build: command not found`:
- Activate the virtual environment.
- Alternatively use `python -m sphinx ...` commands.

2. Unexpected version label in navigation:
- Update `doc_version` in `conf.py`.
- Rebuild using `-E` to clear Sphinx environment cache.

## Developer Cheatsheet

Setup:

```bash
python3 -m venv .venv-docs && source .venv-docs/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Build docs:

```bash
rm -rf docs && python -m sphinx -E -b html -W --keep-going . docs
```

Open homepage (`docs`):

```bash
open docs/index.html
```

Set doc version (example `v2.0.2`):

```bash
sed -i '' 's/doc_version="v2.0.1"/doc_version="v2.0.2"/' conf.py
```
