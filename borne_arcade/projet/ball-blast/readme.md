# ball-blast

## Contrôles du Joueur

### Joueur 1
**Joystick :**
- j1 (joystick)
- **Haut :** Flèche Haut
- **Bas :** Flèche Bas
- **Gauche :** Flèche Gauche
- **Droite :** Flèche Droite

**Touches :**
- **R :** Tirer une balle
- **T :** Accéder au menu
- **Y :** Mettre en pause
- **F :** Activer le mode rapide
- **G :** Activer la gravité augmentée
- **H :** Afficher les statistiques

### Joueur 2
**Joystick :**
- j2 (joystick)
- **Haut :** Touche O
- **Bas :** Touche L
- **Gauche :** Touche K
- **D-même :** Touche M

**Touches :**
- **A :** Tirer une balle
- **Z :** Accéder au menu
- **E :** Mettre en pause
- **Q :** Activer le mode rapide
- **S :** Activer la gravité augmentée
- **D :** Afficher les statistiques

## Mécaniques de Jeu
- **Objectif :** Éliminer tous les ennemis en lançant des balles
- **Tirs :** Les balles sont lancées vers la zone d'ennemis
- **Explosions :** Les balles déclenchent des explosions en chaîne
- **Vie :** 3 vies disponibles avant la fin du jeu

## Assets Utilisés
- **Arrière-plan :** `bg.jpg` et `bg_pxl.jpg` pour les différents modes visuels
- **Explosions :** `explosion.gif` et les 17 frames dans `explosion_frames`
- **Son :** 
  - `bip.mp3` pour les interactions
  - `explosion.mp3` pour les effets sonores
  - `music1-3.mp3` pour la bande-son
  - `musicdeath.mp3` pour la musique de fin
  - `pop.mp3` pour les collisions
  - `win.mp3` pour la victoire
- **Graphismes :** 
  - `canon.png` pour le canon de tir
  - `wheel.png` pour l'interface de menu
  - `photo_small.png` pour les captures d'écran

## Structure Technique
- **Fichiers principaux :**
  - `__main__.py` : Point d'entrée principal
  - `game.py` : Gestion du cycle de jeu
  - `player.py` : Logique des joueurs
  - `bullet.py` : Gestion des balles
  - `ball.py` : Physique des balles
  - `menu.py` : Interface de menu
  - `constantes.py` : Constantes du jeu
- **Ressources :** 
  - `requirements.txt` : Dépendances Python
  - `readme.md` : Documentation complète
  - `description.txt` : Résumé du projet
  - `highscore` : Sauvegarde des scores

## Fonctionnalités Spécifiques
- **Mode rapide :** Accélère le déroulement du jeu
- **Gravité augmentée :** Modifie la trajectoire des balles
- **Explosions en chaîne :** Les balles déclenchent des explosions qui affectent les ennemis
- **Scores :** Sauvegardés dans le fichier `highscore`

## Notes Techniques
- Les animations d'explosion utilisent les 17 frames de `explosion_frames`
- Les sons sont gérés via le module `pygame.mixer`
- La logique de collision est implémentée dans `bullet.py` et `ball.py`
- Le menu utilise `pygame.sprite.Group` pour gérer les éléments visuels