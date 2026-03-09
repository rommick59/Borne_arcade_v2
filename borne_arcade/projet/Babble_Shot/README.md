# Babble Shot

Jeu **Bubble Shooter** en Python + Pygame, avec style visuel néon (dégradés, glow, particules, HUD moderne).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer le jeu

```bash
python3 main.py
```

## Contrôles

- `←/→` ou `f/y` : viser
- `r` : tirer
- `t` : démarrer
- `g` : rejouer
- `h` : quitter
- `Alt+F4` : quitter immédiatement

### Saisie HighScore

- `←/→` : changer de case lettre
- `↑/↓` : changer la lettre sélectionnée
- `r` : confirmer le nom

## Gameplay

- Aligne 3 bulles (ou plus) de même couleur pour les faire exploser.
- Les bulles flottantes non connectées au haut tombent aussi.
- Toutes les `6` bulles tirées sans explosion majeure, une nouvelle ligne apparaît.
- Tu gagnes quand tout est vidé, et tu perds si les bulles atteignent la ligne rouge.
