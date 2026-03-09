#!/bin/bash

# Trouve la racine du projet (répertoire contenant ce script) pour rester robuste
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
GAME_DIR="$ROOT_DIR/projet/CursedWare"
LOCAL_LOVE_BIN="$ROOT_DIR/love-11.5/src/.libs/love"
LOCAL_LOVE_LIBDIR="$ROOT_DIR/love-11.5/src/.libs"

cd "$GAME_DIR" || exit 1

# Priorite au runtime local 11.5 (corrige le bug d'alignement observe en 11.3).
# On execute directement le binaire .libs avec son LD_LIBRARY_PATH.
if [[ -x "$LOCAL_LOVE_BIN" ]]; then
	LD_LIBRARY_PATH="$LOCAL_LOVE_LIBDIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
		"$LOCAL_LOVE_BIN" .
	exit $?
fi

# Fallback sur Love2D systeme si le runtime local n'est pas disponible.
if command -v love >/dev/null 2>&1; then
	love .
	exit $?
fi

echo "Erreur: Love2D introuvable pour lancer CursedWare." >&2
echo "Installez le paquet 'love' (ex: sudo apt install -y love)." >&2
exit 1
