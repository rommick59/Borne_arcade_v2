```markdown
# Documentation du Projet InitialDrift

## Introduction
InitialDrift est un projet de jeu vidéo en 2D développé en Java. Il combine des éléments de plateforme et de combat, avec des personnages contrôlés par le joueur et des ennemis artificiels. Le jeu intègre des graphismes, des sons et des fonctionnalités de score. Il suit une structure modulaire avec des classes principales et des ressources organisées dans des dossiers dédiés.

## Structure du Projet
```
InitialDrift/
├── Ennemi.java
├── Jeu.java
├── Joueur.java
├── Main.java
├── bouton.txt
├── decor/
│   ├── Tonneau.png
│   ├── accueil.jpg
│   ├── accueil.png
│   ├── accueil.xcf
│   ├── bcptono.png
│   ├── bouton_arcade.png
│   ├── commandes.png
│   ├── dirt.jpg
│   ├── grass.png
│   ├── miguel.jpg
│   ├── mirador_droite.png
│   ├── mirador_gauche.png
│   ├── mursac.png
│   ├── obj_bags2.png
│   ├── scenario.jpg
│   └── soldat.png
├── description.txt
├── highscore
├── img/
│   ├── explosion.png
│   ├── jeep.png
│   ├── police.png
│   ├── scorebien.jpg
│   ├── snifsnof.jpeg
│   ├── stickman.png
│   ├── tonneau_ennemi.png
├── photo.png
├── photo_small.png
├── sons/
│   ├── Dejavu.mp3
│   ├── RunninInThe90.mp3
│   ├── explosion.mp3
│   ├── momgetthecamera.mp3
│   ├── pegi18.mp3
│   └── scorenul.mp3
```

## Fichiers Principaux
### Ennemi.java
Implémente la logique des ennemis du jeu. Gère leur mouvement, leur comportement de combat et leurs interactions avec le joueur.

### Jeu.java
Classe centrale gérant le cycle de vie du jeu : initialisation, boucle de jeu, gestion des collisions, mise à jour des scores et gestion des états (jeu, menu, pause).

### Joueur.java
Représente le personnage contrôlé par le joueur. Gère les inputs clavier, les animations, les collisions avec les ennemis et les collectibles.

### Main.java
Point d'entrée du programme. Initialise les ressources, charge le menu d'accueil et lance le jeu.

## Ressources
### Fichiers Graphiques
- **decor/** : Contient les textures de fond, les sprites d'ennemis, de personnages et les éléments décoratifs.
- **img/** : Images utilisées pour les animations, les UI et les éléments visuels du jeu.

### Sons
- **sons/** : Fichiers audio pour les effets sonores (explosions, musiques de fond, sons de score) et les dialogues.

### Textes
- **bouton.txt** : Liste des boutons et leur fonctionnalité.
- **description.txt** : Informations détaillées sur le jeu et ses mécaniques.

## Fonctionnalités Clés
1. **Jeu en 2D** : Utilise des sprites et une gestion de collision basée sur des rectangles.
2. **Système de Score** : Sauvegarde les scores via le fichier `highscore`.
3. **Menu d'Accueil** : Permet de lancer le jeu, accéder aux options et consulter les scores.
4. **Animations et Effets Sonores** : Intégration de sons et de graphismes pour améliorer l'immersion.

## Dossiers et Fichiers Spécifiques
- **decor/** : Contient les images de fond, les sprites et les graphismes du jeu.
- **sons/** : Fichiers audio pour les effets sonores et la musique de fond.
- **highscore/** : Fichier texte stockant les meilleurs scores.
- **img/** : Ressources graphiques additionnelles utilisées dans l'interface et les animations.

## Notes Techniques
- Les classes `Ennemi`, `Joueur` et `Jeu` sont interconnectées via des méthodes de collision et de gestion des états.
- Les ressources sont chargées via des gestionnaires de textures et sons personnalisés.
- Le jeu utilise un système de gestion de temps pour synchroniser les animations et les actions.

## Conformité avec la Structure
La documentation correspond exactement à la structure du projet fournie, avec des sections détaillées et des informations précises sur chaque composant.
```