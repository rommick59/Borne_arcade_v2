#!/bin/bash

print_section() {
    echo ""
    echo "=================================================="
    echo " $1"
    echo "=================================================="
}

# Permet d'exécuter ce script depuis n'importe quel dossier.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VERIFY_LAYOUT_SCRIPT="$WORKSPACE_ROOT/automatisation/scripts/verify_layout.sh"
INSTALL_LAYOUT_SCRIPT="$WORKSPACE_ROOT/automatisation/scripts/install_layout.sh"

cd "$SCRIPT_DIR" || exit 1

print_section "Configuration du mappage clavier"
if [[ -x "$VERIFY_LAYOUT_SCRIPT" && -x "$INSTALL_LAYOUT_SCRIPT" ]]; then
    bash "$VERIFY_LAYOUT_SCRIPT"
    bash "$INSTALL_LAYOUT_SCRIPT"
else
    echo "Avertissement: scripts de layout introuvables ou non executables"
    echo "- $VERIFY_LAYOUT_SCRIPT"
    echo "- $INSTALL_LAYOUT_SCRIPT"
fi

# Remet le clavier en FR lors de la fermeture du script
cleanup() {
    if command -v setxkbmap >/dev/null 2>&1; then
        setxkbmap fr || true
    fi
}
trap cleanup EXIT INT TERM

setxkbmap borne

print_section "Nettoyage des répertoires. Veuillez patienter"
./clean.sh
./compilation.sh

print_section "Lancement du  Menu. Veuillez patienter"

java -cp "$SCRIPT_DIR:$HOME" Main
./clean.sh

#for i in {30..1}
#do
#    echo Extinction de la borne dans $i secondes
#    sleep 1
#done

#sudo halt