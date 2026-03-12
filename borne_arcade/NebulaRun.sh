#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"

if ! command -v python3.12 >/dev/null 2>&1; then
  echo "python3.12 introuvable. Installez Python 3.12." >&2
  exit 1
fi

cd "$REPO_ROOT/projet/NebulaRun"
python3.12 main.py
