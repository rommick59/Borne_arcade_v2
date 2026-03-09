# minesweeper_borne_iut

Jeu du Minesweeper pour la borne d'arcade de l'IUTLCO. Projet de 3ème année de BUT Info.

## Description

Le jeu Minesweeper est un jeu de réflexion où le joueur doit identifier les cases contenant des bombes sur un plateau. Le but est de dévoiler toutes les cases sans déclencher une bombe. Le jeu dispose de plusieurs niveaux de difficulté et de fonctionnalités de personnalisation.

## Fonctionnalités

- **Difficultés** : Niveaux facile, moyen et difficile avec des tailles de plateau et des nombres de bombes adaptés
- **Interface** : Interface graphique avec curseur et boutons tactile
- **Son** : Effets sonores et musique d'ambiance
- **Score** : Sauvegarde des scores et tableau des meilleurs temps
- **Règles** : Affichage des règles du jeu
- **Menu** : Accès aux options, au débriefing et au retour au menu principal

## Installation

1. Cloner le repository : `git clone [URL]`
2. Installer les dépendances nécessaires
3. Compiler le projet avec le Makefile : `make`
4. Exécuter le jeu : `./minesweeper`

## Structure du projet

```
Basic.java
Board.java
Bomb.java
Button.java
Classic.java
ClavierBorneArcade.java
ConstanteEasy.java
ConstanteHard.java
ConstanteMedium.java
Constants.java
Cursor.java
DarkClassic.java
Dig.java
Easy.java
Empty.java
Flag.java
Hard.java
KeyboardArcade.java
Level.java
MainGraphic.java
Makefile
Medium.java
Menu.java
Minesweeper.java
MinesweeperView.java
README.md
Score.java
ScoreData.java
Theme.java
Tile.java
bouton.txt
description.txt
highscore
highscores.txt
img/
sounds/
```

## Composants

- **Basic.java** : Classe de base pour les objets du jeu
- **Board.java** : Gestion du plateau de jeu
- **Bomb.java** : Représentation des bombes
- **Button.java** : Gestion des boutons tactiles
- **Classic.java** : Mode de jeu classique
- **ClavierBorneArcade.java** : Gestion du clavier de la borne
- **ConstanteEasy/Medium/Hard.java** : Constantes pour les niveaux de difficulté
- **Constants.java** : Constantes globales
- **Cursor.java** : Gestion du curseur
- **DarkClassic.java** : Thème sombre
- **Dig.java** : Gestion de la détection des bombes
- **Easy/Medium/Hard.java** : Classes pour les niveaux de difficulté
- **Empty.java** : Case vide
- **Flag.java** : Gestion des drapeaux
- **KeyboardArcade.java** : Gestion du clavier
- **Level.java** : Gestion des niveaux
- **MainGraphic.java** : Fenêtre principale
- **Makefile** : Fichier de compilation
- **Menu.java** : Menu principal
- **Minesweeper.java** : Classe principale
- **MinesweeperView.java** : Vue du jeu
- **Score.java** : Gestion des scores
- **ScoreData.java** : Données des scores
- **Theme.java** : Gestion des thèmes
- **Tile.java** : Case du plateau
- **bouton.txt** : Descriptions des boutons
- **description.txt** : Description du projet
- **highscore** : Fichier de sauvegarde des scores
- **highscores.txt** : Fichier des meilleurs scores
- **img/** : Ressources graphiques
- **sounds/** : Fichiers audio

## Documentation

- **API** : Documentation des classes et méthodes
- **Manuel utilisateur** : Instructions détaillées pour jouer
- **Guide de développement** : Explications techniques pour les contributeurs

## Crédits

Musique : https://gooseninja.itch.io/space-music-pack  
Effets sonores : https://jdwasabi.itch.io/8-bit-16-bit-sound-effects-pack

## Licence

Ce projet est mis à disposition sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.