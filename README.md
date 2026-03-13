# Borne Arcade

**Turbé Keylian, Siame Romain.**

---
## Installation

L'installation permet de setup l'environnement, puis de lancer la borne pour avoir les logs et enfins faire les analyses IAs.
Si le serveur est en Wayland, le changer en X11 pour que les jeux puissent se lancer (nécessaire pour xdotool).
```bash
sudo raspi-config
# Aller dans "advenced options" puis xwayland et enfin selectionner x11 et redémarrer le raspberry pi puis changer la date et l'heure
sudo date -s "2024-06-01 12:00:00"

```
```bash
git clone https://github.com/rommick59/borne_arcade.git
cd borne_arcade
./automatisation/install.sh
```

---

## Lancer la borne indépendamment

```bash
cd borne_arcade
./lancerBorne.sh
```
