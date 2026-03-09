```markdown
# Documentation JavaSpace

## Introduction
JavaSpace est un projet de jeu arcade développé en Java, comprenant une structure de fichiers et d'assets organisés pour permettre un développement modulaire et une gestion visuelle optimisée. Le projet inclut des classes principales pour la logique du jeu, des assets graphiques pour l'interface et des mécanismes de score et de vie.

## Architecture
Le projet suit une architecture modulaire avec les composants suivants :

### Classes Principales
- **Bonus.java** : Gère la logique des bonus collectables par le joueur.
- **Boss.java** : Implémente le comportement du boss principal du jeu.
- **ClavierBorneArcade.java** : Gère l'input des touches de la borne arcade.
- **Ennemi.java** : Contrôle le mouvement et les actions des ennemis.
- **Jeu.java** : Contient la boucle principale du jeu et la gestion des états.
- **Joueur.java** : Gère le joueur principal, y compris les dégâts et les vies.
- **Main.java** : Point d'entrée de l'application.
- **Tir.java** : Gère les projectiles lancés par le joueur et les ennemis.

### Assets
- **img** : Dossier contenant toutes les images du jeu.
  - **background** : Images de fond pour les scènes principales.
  - **bonus** : Sprites des bonus collectables.
  - **boss** : Sprites du boss.
  - **ennemie** : Sprites des ennemis.
  - **intersection** : Images pour les collisions.
  - **laser** : Sprites des lasers.
  - **life** : Images des vies du joueur.
  - **player** : Sprite du joueur.
  - **score** : Numéros pour l'affichage du score.
  - **title** : Image de fond de l'écran de titre.

- **fonts** : Fichiers de police utilisés pour l'affichage du texte.
- **bouton.txt** : Configuration des boutons de l'interface.
- **description.txt** : Texte des descriptions des éléments du jeu.
- **highscore** : Fichier de sauvegarde des scores records.
- **font.ttf** : Police principale du jeu.
- **photo.png** : Image de présentation du projet.
- **photo_small.png** : Version réduite de l'image de présentation.

## Classes
### Bonus.java
Implémente la logique de détection et de collecte des bonus, avec des animations et des effets de collision.

### Boss.java
Gère le comportement du boss, y compris ses attaques, ses mouvements et sa gestion de vie.

### ClavierBorneArcade.java
Permet la gestion des entrées clavier pour la borne arcade, avec des mappings spécifiques aux touches.

### Ennemi.java
Contrôle le mouvement et les actions des ennemis, y compris leurs collisions et dégâts.

### Jeu.java
Contient la boucle de jeu, la gestion des états (menu, jeu, pause, fin de partie), et la mise à jour des objets.

### Joueur.java
Gère le joueur principal, y compris son mouvement, ses vies, ses dégâts et la gestion des projectiles.

### Main.java
Point d'entrée de l'application, initialisant le jeu et l'interface graphique.

### Tir.java
Gère les projectiles lancés par le joueur et les ennemis, avec des collisions et des effets d'explosion.

## Assets
### Images
- **background/** : 3 images de fond pour les scènes principales.
- **bonus/** : 4 sprites de bonus collectables.
- **boss/** : 2 sprites du boss.
- **ennemie/** : 2 sous-dossiers pour les ennemis (boss et ennemie1).
- **intersection/** : 2 images pour les collisions (laser et touchey).
- **laser/** : 3 sous-dossiers pour les lasers (boss, ennemie1, player1).
- **life/** : 4 sprites de vie, avec 4 animations de dégâts.
- **player/** : 1 sprite du joueur.
- **score/** : 10 sprites pour les chiffres 0-9 et un sprite pour le "x".
- **title/** : 1 image de fond pour l'écran de titre.

### Fichiers de police
- **font.ttf** : Police utilisée pour l'affichage du texte.

### Fichiers de configuration
- **bouton.txt** : Définit les positions et comportements des boutons.
- **description.txt** : Textes des descriptions des éléments du jeu.

### Sauvegarde
- **highscore** : Fichier texte contenant les records de score.

## Conclusion
JavaSpace est un projet structuré avec une logique de jeu claire et des assets visuels complets. La documentation reflète la structure du projet, permettant une maintenance et une évolution efficaces.
```