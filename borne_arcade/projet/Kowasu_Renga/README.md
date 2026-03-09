# Documentation de Kowasu_Renga

## Aperçu du projet
Kowasu_Renga est une application de jeu de type renga (poésie collaborative) conçue pour permettre aux utilisateurs de créer des poèmes en chaîne. Le projet intègre des fonctionnalités de gestion de scores, une interface graphique et des ressources visuelles pour améliorer l'expérience utilisateur.

## Changements récents
- **FORCED_UPDATE** : Mise à jour obligatoire du code et des ressources

## Structure du projet
```
Kowasu_Renga.java
Kowasu_Renga.java2
bouton.txt
description.txt
font.ttf
highscore
img/
img/0.png
img/1.png
img/2.png
img/3.png
img/4.png
img/5.png
img/6.png
img/7.png
img/8.png
img/9.png
img/background.jpg
photo.png
photo_small.png
```

## Fichiers et dossiers
- **Kowasu_Renga.java** : Fichier principal contenant la logique du jeu
- **Kowasu_Renga.java2** : Fichier de secours ou de gestion des scores
- **bouton.txt** : Fichier de configuration des boutons de l'interface
- **description.txt** : Fichier contenant la description du jeu
- **font.ttf** : Police de caractères utilisée dans l'application
- **highscore** : Fichier de sauvegarde des scores records
- **img/** : Dossier contenant toutes les images du jeu
  - **0.png à 9.png** : Images des chiffres affichés sur l'interface
  - **background.jpg** : Fond d'écran du jeu
- **photo.png** : Image de profil principale
- **photo_small.png** : Version miniature de l'image de profil

## Installation
1. Téléchargez le projet sur votre système de fichiers
2. Installez Java 17 ou supérieur
3. Exécutez `Kowasu_Renga.java` via un compilateur Java
4. Vérifiez les ressources dans le dossier `img/` pour l'interface graphique

## Utilisation
1. Lancez l'application via le fichier principal
2. Utilisez les boutons configurés dans `bouton.txt` pour interagir
3. Consultez les scores via le fichier `highscore`
4. Personnalisez l'interface avec les ressources dans le dossier `img/`

## Détails techniques
- **Dépendances** : Java 17, bibliothèque de gestion de fichiers
- **Technologies** : Java Swing pour l'interface graphique, gestion de threads pour les animations
- **Configuration** : Le fichier `font.ttf` doit être placé dans le répertoire racine pour être chargé correctement
- **Optimisations** : Les images sont compressées pour réduire la taille du projet tout en maintenant une qualité visuelle acceptable

## Contributions
- Les développeurs peuvent contribuer en améliorant la gestion des scores ou en ajoutant des fonctionnalités de personnalisation
- Les designers peuvent modifier les ressources visuelles dans le dossier `img/`
- Les développeurs peuvent optimiser la performance du jeu en réduisant la latence des animations