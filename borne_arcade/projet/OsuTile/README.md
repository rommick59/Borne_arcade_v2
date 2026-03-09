```markdown
# OsuTile - Documentation Technique

## Aperçu Général
OsuTile est un projet Python conçu pour la gestion et la lecture de cartes Osu. Il inclut des fonctionnalités de lecture de map, de gestion d'audio et d'interface graphique basique. Le projet est structuré en plusieurs modules et ressources, notamment des map OSU, des sons, et des scripts de gestion.

## Installation
1. **Dépendances** : 
   - Python 3.10+
   - Bibliothèque `pygame` (via `pip install pygame`)
   - Bibliothèque `osu` (via `pip install osu`)
2. **Procédure** :
   - Cloner le dépôt
   - Exécuter `pip install -r requirements.txt`
   - Lancer `main.py` pour lancer l'application

## Utilisation
1. **Lancement** :
   - Exécuter `main.py` pour démarrer l'interface de menu
   - Sélectionner une carte via le menu principal
   - Appuyer sur le bouton "Jouer" pour lancer la lecture de la carte
2. **Fonctionnalités Clés** :
   - Lecture de cartes Osu (supporte Camellia_Ghost, Megalovania, Yoasobi_Kaibutsu)
   - Lecture de sons associés (Camellia_Ghost.mp3, Megalovania.mp3, Yoasobi_Kaibutsu.mp3)
   - Gestion de l'export des map via `export_map.py`

## Structure du Projet
```
assets/
    Camellia_Ghost.mp3
    Megalovania.mp3
    Yoasobi_Kaibutsu.mp3
beatmaps/
    Camellia_Ghost.osu
    Megalovania.osu
    Yoasobi_Kaibutsu.osu
bouton.txt
config.py
description.txt
game.py
main.py
map_parser.py
maps/
    Camellia_Ghost.py
    Megalovania.py
    Yoasobi_Kaibutsu.py
menu.py
photo_small.png
tile.py
tools/
    export_map.py
```

## Configuration
Le fichier `config.py` permet de personnaliser :
- Réglages audio (volume, boucle)
- Chemins des ressources
- Options de rendu graphique
Exemple de configuration :
```python
CONFIG = {
    "volume": 0.8,
    "loop_audio": True,
    "resource_path": "assets/",
    "fullscreen": False
}
```

## Contributions
- **Signaler des bugs** : Utiliser le système d'issues GitHub
- **Proposer des améliorations** : Soumettre des PR avec tests unitaires
- **Documentation** : Ajouter des commentaires dans les scripts et mettre à jour la documentation

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour les détails.

## Historique des Changements
- **FORCED_UPDATE** : Mise à jour forcée des ressources et scripts (2023-10-15)
- **Ajouts récents** : Support des nouvelles cartes, optimisation des performances, correction de bugs de lecture audio
```