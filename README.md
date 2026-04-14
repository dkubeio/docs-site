# DKubeX Documentation

<p align="right">
  <a href="#developer-cheatsheet">
    <img alt="Developer Cheatsheet" src="https://img.shields.io/static/v1?label=&message=Developer%20Cheatsheet&color=0A66C2&style=for-the-badge" />
  </a>
</p>

This repository hosts the DKubeX documentation site, built on Sphinx and sphinx-multiversion.

## Overview

The current workflow is tags-only multiversion:
- Keep documentation source files at repository root.
- Build one output per matching Git tag as `docs-vX.Y.Z`.
- Copy the latest semantic version to `docs/`.
- Publish generated output to the `site-files` branch through GitHub Actions.

## Architecture

1. Single source model:
- Source content is maintained directly at repository root (`*.md`, `applications/`, `images/`, `_static/`, `_templates/`).

2. Shared configuration model:
- Root `conf.py` is the single combined Sphinx configuration.
- sphinx-multiversion includes tags matching `vX.Y.Z` only.

3. Output model:
- Versioned build outputs are generated as `docs-v*`.
- The latest semantic version is copied to `docs/`.
- Primary reader entry point remains `docs/index.html`.

## Repository Structure

- `.github/workflows/build.yml`: build and publishing workflow.
- `conf.py`: active Sphinx configuration entrypoint.
- `*.md`, `applications/**`, `images/**`, `_static/**`, `_templates/**`: source files.
- `docs-v*/`: generated per-tag HTML outputs.
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

2. Build multiversion documentation from tags:

```bash
git fetch --tags && bash build_docs.sh
```

The script uses `.venv-docs/bin/python` by default. If you want to use a different compatible Python environment, set `BUILD_PYTHON` first.

3. Validate the homepage first:
- `docs/index.html`

4. Open the generated site:
- `docs/index.html`

## CI Workflow Summary

Workflow file: `.github/workflows/build.yml`

Current implemented behavior on push to any branch (for docs/workflow changes):
1. Install dependencies.
2. Build tag-matched versions to `docs-v*` using sphinx-multiversion.
3. Copy latest semantic version to `docs`.
4. Upload site artifact.
5. Publish generated output to `site-files` branch.

Pages and custom domain delivery:
- This workflow does not execute a separate GitHub Pages deploy action.
- Delivery is expected through repository Pages configuration using `site-files` as the published source.

## Troubleshooting

1. `sphinx-build: command not found`:
- Activate the virtual environment.
- Alternatively use `python -m sphinx ...` commands.

2. No versioned output generated:
- Ensure local repository has matching tags (example: `v2.0.1`).
- Run `git fetch --tags` before local build.
- Run `bash build_docs.sh` from the docs virtual environment.
- Confirm `.venv-docs` exists or export `BUILD_PYTHON=/path/to/python`.

3. `Config.read() takes 2 positional arguments but 3 were given`:
- Reinstall dependencies from `requirements.txt`.
- This project pins `Sphinx<8` for `sphinx-multiversion` compatibility.

4. Unexpected version label in navigation:
- Verify the tag names follow `vX.Y.Z` and are fetched locally.
- Confirm you are using the pinned docs virtual environment from this repository.

## Developer Cheatsheet

Setup:

```bash
python3 -m venv .venv-docs && source .venv-docs/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Build multiversion docs:

```bash
bash build_docs.sh
```

Open homepage (`docs`):

```bash
open docs/index.html
```

Create a release tag (example `v2.0.2`):

```bash
git tag v2.0.2 && git push origin v2.0.2
```
