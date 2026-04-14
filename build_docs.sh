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
rm -rf .multiversion

if [ ! -f docs/index.html ]; then
  echo "Build failed: docs/index.html was not generated."
  exit 1
fi