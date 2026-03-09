#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/projet/balapy"
PYTHON_BIN="$SCRIPT_DIR/../.venv/bin/python"

cd "$PROJECT_DIR" || exit 1

if [ -x "$PYTHON_BIN" ]; then
  "$PYTHON_BIN" main.py
else
  python3 main.py
fi