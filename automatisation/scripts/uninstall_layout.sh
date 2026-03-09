#!/usr/bin/env bash
# Desinstalle le layout clavier personnalise "borne" de XKB.

set -euo pipefail

SYSTEM_XKB_DIR="/usr/share/X11/xkb/symbols"
TARGET_FILE="$SYSTEM_XKB_DIR/borne"

if [[ ! -e "$TARGET_FILE" ]]; then
    echo "Layout borne deja absent: $TARGET_FILE"
    exit 0
fi

echo "Suppression du layout clavier borne..."
sudo rm -f "$TARGET_FILE"

# Debian/Ubuntu: recharge la base xkb-data si disponible.
if command -v dpkg-reconfigure >/dev/null 2>&1; then
    sudo dpkg-reconfigure -f noninteractive xkb-data >/dev/null 2>&1 || true
fi

echo "Layout desinstalle: OK"
