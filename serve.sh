#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "$SCRIPT_DIR/docs-env/bin/python" ]; then
    MKDOCS_BIN="$SCRIPT_DIR/docs-env/bin/mkdocs"
elif [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    MKDOCS_BIN="$SCRIPT_DIR/.venv/bin/mkdocs"
elif command -v mkdocs >/dev/null 2>&1; then
    MKDOCS_BIN="mkdocs"
else
    echo "Error: mkdocs not found. Please run ./setup_linux.sh first."
    exit 1
fi

echo "Starting MkDocs development server..."
exec "$MKDOCS_BIN" serve "$@"
