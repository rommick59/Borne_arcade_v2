# TronGame - Documentation Développeur

## Projet
TronGame est un jeu d'arcade inspiré du film Tron, développé avec Pygame. Il s'agit d'une implémentation moderne du jeu "Light Cycles" avec des fonctionnalités de gestion de parties, de menus et de sonorisation.

## Structure du Projet
```
├── main.py              # Point d'entrée principal
├── config.py            # Configuration globale
├── direction.py         # Énumération des directions
├── player.py            # Gestion des joueurs
├── ai.py                # Logique de l'IA
├── game_main.py         # Logique du jeu
├── menu_main.py         # Menu principal
├── options_main.py      # Menu des options
├── score_screen.py      # Écran de fin de partie
├── assets/              # Ressources
│   ├── images/          # Images du jeu
│   │   ├── key_f.png    # Image de la touche F
│   │   ├── key_r.png    # Image de la touche R
│   │   └── tron_logo.png # Logo du jeu
│   ├── sounds/          # Sons du jeu
│   │   ├── crash.wav    # Son de collision
│   │   ├── move.wav     # Son de déplacement
│   │   ├── music_game.wav # Musique de jeu
│   │   ├── music_menu.wav # Musique du menu
│   │   ├── navigate.wav # Son de navigation
│   │   └── select.wav    # Son de sélection
│   └── photo_small.png  # Photo de l'application
├── utils/               # Utilitaires
│   ├── create_empty_sounds.py # Génération de sons vides
│   ├── create_logo.py      # Création du logo
│   └── generate_sounds.py  # Génération de sons
├── bouton.txt           # Fichier de configuration des boutons
├── description.txt      # Fichier de description
├── requirements.txt     # Dépendances Python
└── README.md            # Fichier de présentation
```

## Modules Principaux

### `config.py`
Contient les paramètres globaux du jeu :
- Dimensions de l'écran (width, height)
- Vitesse de déplacement
- Paramètres sonores (volume, boucle)
- Configuration des contrôles (touche de pause, de redémarrage)

### `direction.py`
Définit l'énumération des directions possibles :
```python
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
```

### `player.py`
Gère les attributs des joueurs :
- Position (x, y)
- Direction actuelle
- Traînée (liste de coordonnées)
- Vitesse de déplacement
- Statut (actif, mort)

### `ai.py`
Implémente l'intelligence artificielle pour le mode solo :
- Algorithme de choix de direction
- Gestion des niveaux de difficulté
- Stratégie de fuite

### `game_main.py`
Contient la logique principale :
- Gestion des collisions
- Mise à jour des traînées
- Gestion du temps de jeu
- Calcul des scores
- Gestion des états de jeu (joue, pause, fin)

## Ressources

### Sons
- `crash.wav` : Son de collision
- `move.wav` : Son de déplacement
- `music_game.wav` : Musique de jeu
- `music_menu.wav` : Musique du menu
- `navigate.wav` : Son de navigation
- `select.wav` : Son de sélection

### Images
- `key_f.png` : Image de la touche F
- `key_r.png` : Image de la touche R
- `tron_logo.png` : Logo du jeu
- `photo_small.png` : Photo de l'application

## Contrôles
**Joueur 1 :** Flèches directionnelles  
**Joueur 2 :** WASD  
**Général :** P (pause), ESPACE (redémarrage), ÉCHAP (menu)

## Documentation Complémentaire
📖 **[Guide Utilisateur](GUIDE_UTILISATEUR.md)** - Instructions détaillées pour jouer  
🛠️ **[Documentation Développeur](DOCUMENTATION_DEVELOPPEUR.md)** - Architecture et développement  
📄 **[Fichier de Description](description.txt)** - Informations complémentaires sur le projet  
📝 **[Fichier de Dépendances](requirements.txt)** - Liste des packages Python requis

## Notes Techniques
- Le jeu utilise Pygame 2.0 pour la gestion graphique et sonore
- Les traînées sont stockées dans des listes de tuples (x, y)
- Les collisions sont détectées via des vérifications de chevauchement
- Le système de sonorisation est géré via le module `pygame.mixer`