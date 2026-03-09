# Documentation du Projet Snake_Eater

## Introduction
Snake_Eater est un jeu de type "Snake" développé en Java, comprenant une interface graphique, un système de score et des éléments de design visuel. Le projet intègre des classes pour gérer le serpent, la nourriture, le clavier, le score et des ressources graphiques. Il suit une structure modulaire et est conçu pour être exécutable de manière autonome.

## Structure du Projet
```
ClavierBorneArcade.java
HighScore.java
LigneHighScore.java
Nourriture.java
Pomme.java
Serpent.java
Snake_Eater.java
bouton.txt
description.txt
highscore/
img/
img/background.jpg
photo.png
photo_small.png
```

## Classes Principales
### ClavierBorneArcade.java
Gère l'interaction clavier pour le jeu. Implémente les méthodes de gestion des touches directionnelles et des actions spéciales (pause, quitter).

### Serpent.java
Représente le serpent principal. Contient :
- Logique de déplacement
- Gestion de la croissance
- Collision avec les bords et la nourriture
- Méthodes pour dessiner le serpent sur l'écran

### Nourriture.java
Gère la création et la gestion des éléments nutritifs. Contient :
- Position aléatoire sur le terrain
- Méthodes pour vérifier les collisions avec le serpent
- Réinitialisation après consommation

### Pomme.java
Classe spécifique pour la nourriture (fruit) avec :
- Position unique sur le terrain
- Méthodes de collision et de réinitialisation

### HighScore.java
Gère le système de score. Contient :
- Liste des scores highscore
- Méthodes pour ajouter, sauvegarder et charger les scores
- Comparaison avec le score actuel

### LigneHighScore.java
Représente une ligne individuelle du tableau des scores. Contient :
- Nom du joueur
- Score obtenu
- Méthodes d'affichage et de comparaison

## Ressources
### bouton.txt
Fichier texte contenant les étiquettes des boutons (start, pause, quit).

### description.txt
Fichier texte contenant une brève description du projet et des instructions d'utilisation.

### highscore/
Dossier contenant les fichiers Java pour le système de score.

### img/
Dossier contenant les ressources graphiques :
- background.jpg : fond d'écran du jeu
- photo.png : image principale du jeu
- photo_small.png : version miniaturisée de l'image

## Changements Récents
**FORCED_UPDATE** : Mise à jour obligatoire du projet incluant :
- Réorganisation des classes pour une meilleure modularité
- Ajout de ressources graphiques supplémentaires
- Amélioration du système de score

## Conclusion
Snake_Eater est un projet complet avec une architecture bien structurée, des fonctionnalités clés (jeu, score, interface) et des ressources visuelles. La documentation détaillée permet une compréhension et une maintenance efficaces du projet.