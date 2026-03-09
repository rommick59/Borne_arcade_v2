## Documentation du projet Columns

### Introduction

Ce document décrit le jeu Columns, un jeu de puzzle développé pour la borne d'arcade. Le joueur doit faire tomber des gemmes colorées dans des colonnes afin de les aligner par trois et les faire disparaître. 

Le jeu comporte plusieurs niveaux avec une difficulté croissante. Le but est de marquer le plus de points possible en éliminant les gemmes.


### Fonctionnalités

* **Jeu de puzzle**: Le joueur doit aligner des gemmes colorées pour les faire disparaître.
* **Différents niveaux**: La difficulté du jeu augmente au fur et à mesure que l'on avance dans les niveaux.
* **Gestion des commandes**: Le jeu utilise le clavier d'arcade pour contrôler les mouvements des gemmes. 
* **Interface utilisateur**: Un menu permet de choisir un niveau et de quitter le jeu.


### Architecture

Le projet Columns est structuré en plusieurs classes Java:

**Classes principales:**

* `ClavierBorneArcade.java`: Gère les entrées du clavier d'arcade.
* `Colone.java`: Représente une colonne dans le jeu, contenant les gemmes.
* `Controles.java`: Contrôle les actions du joueur (rotation des gemmes).
* `Gemme.java`: Représente une gemme avec sa couleur et son positionnement.
* `Main.java`: Point d'entrée du programme.
* `Menu.java`: Gère l'interface utilisateur du menu principal.
* `Partie.java`: Contrôle la partie en cours (score, niveau, etc.).
* `Puits.java`: Simule le puits dans lequel tombent les gemmes.

**Fichiers externes:**

* `bouton.txt`: Contient les configurations des boutons de l'arcade.
* `description.txt`:  Description du jeu et instructions pour le joueur.
* `fonts`: Dossier contenant les polices d'écriture utilisées dans le menu et les informations de score.
    * `Norse-Bold.ttf`: Police utilisée pour le titre et les éléments importants du menu.
* `highscore`: Fichiers contenant les scores élevés.

**Dossiers d'images:**

* `img`: Contient les images du jeu.
    * `game`: Images de jeu, comme le fond de la scène de jeu et les gemmes.
    * `menu`: Images du menu principal, comme l'arrière-plan et le titre.


### Démarrage du jeu

Pour démarrer le jeu Columns, il faut exécuter le fichier `Main.java`. Le menu principal s'affichera, permettant au joueur de choisir un niveau ou de quitter le jeu.