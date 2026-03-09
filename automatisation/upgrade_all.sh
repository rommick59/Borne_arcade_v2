#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Sync dépôts"
sudo apt-get update

echo "[2/6] Mise à jour des paquets (upgrade)"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y upgrade

echo "[3/6] Mise à niveau complète (dist-upgrade)"
sudo DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade

echo "[4/6] Suppression paquets inutiles"
sudo apt-get -y autoremove --purge

echo "[5/6] Nettoyage cache APT"
sudo apt-get -y clean
sudo apt-get -y autoclean

echo "[6/6] Vérification paquets cassés (optionnel)"
sudo apt-get -y -f install

echo "OK - système à jour."
echo "Conseil: redémarre si le kernel/libc ont été mis à jour: sudo reboot"