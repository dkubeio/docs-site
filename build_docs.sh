#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="${BUILD_PYTHON:-$SCRIPT_DIR/.venv-docs/bin/python}"

# Check if Python executable exists (supports both paths and commands in PATH)
if [ -f "$PYTHON_BIN" ] && [ -x "$PYTHON_BIN" ]; then
  # It's an absolute path that exists and is executable
  :
elif command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  # It's a command that exists in PATH
  :
else
  echo "Docs Python interpreter not found: $PYTHON_BIN"
  echo "Create .venv-docs or set BUILD_PYTHON to a compatible Python executable."
  exit 1
fi

if ! "$PYTHON_BIN" -m sphinx_multiversion --help >/dev/null 2>&1; then
  echo "sphinx-multiversion is not available in: $PYTHON_BIN"
  echo "Install requirements.txt into that environment first."
  exit 1
fi

MATCHING_TAGS="$(git tag --list)"
if [ -z "$MATCHING_TAGS" ]; then
  echo "No tags found. Create at least one tag to generate versioned docs."
  exit 1
fi

rm -rf docs
find . -maxdepth 1 -type d -name 'docs-v*' -exec rm -rf {} +
rm -rf .multiversion

"$PYTHON_BIN" -m sphinx_multiversion . .multiversion -W --keep-going

if [ ! -d .multiversion ]; then
  echo "sphinx-multiversion did not create .multiversion output."
  exit 1
fi

find .multiversion -maxdepth 1 -type d -name 'docs-v*' -exec cp -R {} . \;

LATEST_VERSION_DIR="$(find . -maxdepth 1 -type d -name 'docs-v*' -print | sed 's|^\./||' | sort -V | tail -n1)"
if [ -z "$LATEST_VERSION_DIR" ]; then
  echo "No versioned output directories were generated. Check that matching tags exist."
  exit 1
fi

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
  # Rewrite references like ../docs-vX.Y.Z/.. to ../docs/..
  return re.sub(
    rf'((?:\.\./)*){re.escape(latest_dir)}/',
    r'\1docs/',
    text,
  )

def rewrite_latest_self_link(file_path: Path, text: str) -> str:
  # In docs-v<latest> pages, make latest tag link point to docs/<same-page>.
  rel_from_latest = file_path.relative_to(latest_root)
  docs_target = (root / "docs" / rel_from_latest).as_posix()
  href_to_docs = Path(os.path.relpath(docs_target, file_path.parent.as_posix())).as_posix()

  pattern = re.compile(
    rf'(<a href=")([^"]*)(">\s*{re.escape(latest_tag)}\s*</a>)'
  )
  return pattern.sub(rf'\1{href_to_docs}\3', text)

html_files = [p for p in root.glob("docs*/**/*.html") if p.is_file()]
for html in html_files:
  content = html.read_text(encoding="utf-8")
  updated = rewrite_latest_path_refs(content)
  if latest_root in html.parents:
    updated = rewrite_latest_self_link(html, updated)

  if updated != content:
    html.write_text(updated, encoding="utf-8")
PY

rm -rf .multiversion

if [ ! -f docs/index.html ]; then
  echo "Build failed: docs/index.html was not generated."
  exit 1
fi