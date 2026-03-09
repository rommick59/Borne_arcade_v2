#!/usr/bin/env bash
# Installe le layout clavier personnalise "borne" dans XKB.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LAYOUT_FILE="$WORKSPACE_ROOT/borne_arcade/borne"
SYSTEM_XKB_DIR="/usr/share/X11/xkb/symbols"
TARGET_FILE="$SYSTEM_XKB_DIR/borne"

if [[ ! -f "$LAYOUT_FILE" ]]; then
    echo "Erreur: layout introuvable: $LAYOUT_FILE" >&2
    exit 1
fi

echo "Installation du layout clavier borne..."
sudo install -m 0644 "$LAYOUT_FILE" "$TARGET_FILE"

# Debian/Ubuntu: recharge la base xkb-data si disponible.
if command -v dpkg-reconfigure >/dev/null 2>&1; then
    sudo dpkg-reconfigure -f noninteractive xkb-data >/dev/null 2>&1 || true
fi

echo "Layout installe: OK"
echo "Cible: $TARGET_FILE"
