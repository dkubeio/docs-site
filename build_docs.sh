#!/usr/bin/env bash

# Fail fast on errors, unset variables, and pipeline failures.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="${BUILD_PYTHON:-$SCRIPT_DIR/.venv-docs/bin/python}"

# Accept both absolute Python paths and PATH-resolved commands.
if [ -f "$PYTHON_BIN" ] && [ -x "$PYTHON_BIN" ]; then
  :
elif command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  :
else
  echo "Docs Python interpreter not found: $PYTHON_BIN"
  echo "Create .venv-docs or set BUILD_PYTHON to a compatible Python executable."
  exit 1
fi

# Require sphinx-multiversion in selected interpreter.
if ! "$PYTHON_BIN" -m sphinx_multiversion --help >/dev/null 2>&1; then
  echo "sphinx-multiversion is not available in: $PYTHON_BIN"
  echo "Install requirements.txt into that environment first."
  exit 1
fi

# Require at least one tag for versioned output generation.
MATCHING_TAGS="$(git tag --list)"
if [ -z "$MATCHING_TAGS" ]; then
  echo "No tags found. Create at least one tag to generate versioned docs."
  exit 1
fi

# Reset prior build outputs.
rm -rf docs
find . -maxdepth 1 -type d -name 'docs-*' -exec rm -rf {} +
rm -rf .multiversion

SPHINX_FLAGS=(--keep-going)
if [ "${STRICT_WARNINGS:-0}" = "1" ]; then
  SPHINX_FLAGS=(-W --keep-going)
fi

# Build all tagged versions via sphinx-multiversion.
"$PYTHON_BIN" -m sphinx_multiversion . .multiversion "${SPHINX_FLAGS[@]}"

if [ ! -d .multiversion ]; then
  echo "sphinx-multiversion did not create .multiversion output."
  exit 1
fi

# Copy generated version folders to repository root.
find .multiversion -maxdepth 1 -type d -name 'docs-*' -exec cp -R {} . \;

# Use the newest semantic version as the homepage source.
LATEST_VERSION_DIR="$(find . -maxdepth 1 -type d -name 'docs-v*' -print | sed 's|^\./||' | sort -V | tail -n1)"
if [ -z "$LATEST_VERSION_DIR" ]; then
  echo "No versioned output directories were generated. Check that matching tags exist."
  exit 1
fi

# Create docs/ alias from latest version for homepage routing.
cp -R "$LATEST_VERSION_DIR" docs

LATEST_TAG="${LATEST_VERSION_DIR#docs-}"
export LATEST_VERSION_DIR
export LATEST_TAG

"$PYTHON_BIN" - <<'PY'
from pathlib import Path
import os
import re

root = Path(".")
latest_dir = os.environ["LATEST_VERSION_DIR"]
latest_tag = os.environ["LATEST_TAG"]
latest_root = root / latest_dir

if not latest_root.exists():
  raise SystemExit(0)

def rewrite_latest_path_refs(text: str) -> str:
  # Rewrite refs like ../docs-vX.Y.Z/... to ../docs/...
  return re.sub(
    rf'((?:\.\./)*){re.escape(latest_dir)}/',
    r'\1docs/',
    text,
  )

def rewrite_latest_self_link(file_path: Path, text: str) -> str:
  # On latest-version pages, point latest tag link to docs/<same-page>.
  # In docs-v<latest> pages, make latest tag link point to docs/<same-page>.
  rel_from_latest = file_path.relative_to(latest_root)
  docs_target = (root / "docs" / rel_from_latest).as_posix()
  href_to_docs = Path(os.path.relpath(docs_target, file_path.parent.as_posix())).as_posix()

  pattern = re.compile(
    rf'(<a href=")([^"]*)(">\s*{re.escape(latest_tag)}\s*</a>)'
  )
  return pattern.sub(rf'\1{href_to_docs}\3', text)

def rewrite_version_labels(file_path: Path, text: str) -> str:
  # Keep footer/version labels aligned with rendered directory version.
  parts = file_path.parts
  if parts and parts[0] == "docs":
    version_label = latest_tag
  else:
    version_dir = next((part for part in parts if part.startswith("docs-")), None)
    if not version_dir:
      return text
    version_label = version_dir.removeprefix("docs-")

  text = re.sub(
    r'(<div class="sy-foot-copyright"><p>.*?Documentation version: )[^<]+(</p>)',
    rf'\1{version_label}\2',
    text,
    flags=re.S,
  )
  text = re.sub(
    r'(<em>Version\s+)[^<]+(</em>)',
    rf'\1{version_label}\2',
    text,
  )
  return text

html_files = [p for p in root.glob("docs*/**/*.html") if p.is_file()]
for html in html_files:
  content = html.read_text(encoding="utf-8")
  updated = rewrite_latest_path_refs(content)
  if latest_root in html.parents:
    updated = rewrite_latest_self_link(html, updated)
  updated = rewrite_version_labels(html, updated)

  if updated != content:
    html.write_text(updated, encoding="utf-8")
PY

# Remove temporary multiversion staging directory.
rm -rf .multiversion

if [ ! -f docs/index.html ]; then
  echo "Build failed: docs/index.html was not generated."
  exit 1
fi