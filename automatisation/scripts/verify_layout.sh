#!/usr/bin/env bash
# Verifie la structure minimale du fichier layout XKB "borne".

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAYOUT_FILE="$WORKSPACE_ROOT/borne_arcade/borne"

if [[ ! -f "$LAYOUT_FILE" ]]; then
    echo "Erreur: layout introuvable: $LAYOUT_FILE" >&2
    exit 1
fi

if ! grep -Eq '^[[:space:]]*xkb_symbols[[:space:]]+"[^"]+"[[:space:]]*\{' "$LAYOUT_FILE"; then
    echo "Erreur: aucune section xkb_symbols valide detectee dans $LAYOUT_FILE" >&2
    exit 1
fi

if ! grep -Eq '^[[:space:]]*key[[:space:]]*<' "$LAYOUT_FILE"; then
    echo "Avertissement: aucune definition de touche (key <...>) detectee" >&2
fi

echo "Verification layout: OK"
