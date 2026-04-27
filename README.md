# DKubeX Documentation

<p align="right">
  <a href="#developer-cheatsheet">
    <img alt="Developer Cheatsheet" src="https://img.shields.io/static/v1?label=&message=Developer%20Cheatsheet&color=0A66C2&style=for-the-badge" />
  </a>
</p>

This repository contains the DKubeX documentation system. It is built with Sphinx and `sphinx-multiversion`, and it is designed for tag-based versioned publishing.

## At a Glance

| Item | Value |
| --- | --- |
| Primary homepage | `docs/index.html` |
| Source site entry | `https://dkubex2.dkube.io/` |
| Versioning model | Git tags via `sphinx-multiversion`; newest semantic version becomes the homepage |
| Build entrypoint | `build_docs.sh` |
| Config entrypoint | `conf.py` |
| Publish target | `site-files` branch |


## How This System Works

The documentation system follows a strict source/build/publish split:

1. Source of truth
- Editable content lives in the repository root (`*.md`, `applications/**`, `images/**`, `_static/**`, `_templates/**`).
- Generated directories (`docs/`, `docs-*`) are build outputs and should not be edited directly.

2. Versioning
- Documentation versions are derived from Git tags.
- Each tag is rendered into its own output directory (`docs-<tag>`).
- The newest semantic version tag is copied to `docs/` to serve as the default homepage.

3. Build execution
- `build_docs.sh` validates the Python environment.
- It requires `sphinx-multiversion` and at least one tag.
- It removes stale generated output, rebuilds all tagged versions, and then post-processes the HTML for latest-version routing and labels.

4. Configuration
- `conf.py` resolves the active `doc_version` from the checked-out tag.
- The same configuration is reused for each version build so every tag is rendered consistently.

5. CI/CD
- GitHub Actions runs the build on docs-related changes, tag events, and manual dispatch.
- The workflow creates a `CNAME`, publishes the generated snapshot to `site-files`, and force-updates that branch.
- Repository Pages is expected to serve from `site-files`; the workflow itself does not run a separate deploy action.

## Where to Edit Content

- Add or update docs pages in the repository root Markdown files, or applications folder if you are a contributor.
- Update build behavior in `build_docs.sh`.
- Update versioning and Sphinx configuration in `conf.py`.

## Repository Structure

- `.github/workflows/build.yml`: build and publish workflow.
- `conf.py`: Sphinx entry point and multiversion configuration.
- `build_docs.sh`: local and CI build orchestration script.
- `*.md`, `applications/**`, `images/**`, `_static/**`, `_templates/**`: editable source files.
- `docs-*/`: generated per-tag HTML outputs.
- `docs/`: generated latest HTML output.

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

`build_docs.sh` uses `.venv-docs/bin/python` by default. Set `BUILD_PYTHON` first if you want a different compatible Python interpreter.

3. Open the homepage:
- `docs/index.html`

## CI Workflow Summary

Workflow file: `.github/workflows/build.yml`

Current behavior on pushes and tag events:
1. Install dependencies.
2. Build tag-matched versions to `docs-*` using `sphinx-multiversion`.
3. Copy the newest semantic version build to `docs/` for the homepage.
4. Upload the generated site artifact.
5. Publish the generated snapshot to `site-files`.

Pages and custom domain delivery:
- The workflow writes `CNAME` into generated output.
- Repository Pages is expected to serve from `site-files`.

## Troubleshooting

1. `sphinx-build: command not found`
- Activate the virtual environment.
- Alternatively use `python -m sphinx ...` commands.

2. No versioned output generated
- Ensure the repository contains tags.
- Run `git fetch --tags` before building.
- Run `bash build_docs.sh` from the docs virtual environment.
- Confirm `.venv-docs` exists or export `BUILD_PYTHON=/path/to/python`.

3. `Config.read() takes 2 positional arguments but 3 were given`
- Reinstall dependencies from `requirements.txt`.
- This project pins `Sphinx<8` for `sphinx-multiversion` compatibility.

4. Unexpected version label in navigation
- Verify that tags are fetched locally.
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
