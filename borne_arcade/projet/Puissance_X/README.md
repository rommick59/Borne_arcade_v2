# Documentation du Projet Puissance_X

## 1. Introduction
Le projet Puissance_X est une application de jeu de plateau basé sur le jeu de puissance 4. Il intègre une interface graphique, une gestion des parties, des paramètres de jeu personnalisables, et des fonctionnalités de pause et de fin de partie. Le projet utilise Java avec une architecture modulaire comprenant des classes pour la gestion des éléments graphiques, des joueurs, des parties, et des menus.

## 2. Architecture
### 2.1 Structure de package
- **com.puissanceX.core**: Classes centrales du jeu (Plateau, Joueur, PartieSprite)
- **com.puissanceX.ui**: Gestion de l'interface graphique (Ecran, ElementMenu, BoutonItem)
- **com.puissanceX.config**: Paramétrage des parties et joueurs (ConfigurationPartie, ConfigurationJoueurMenu)
- **com.puissanceX.util**: Outils généraux (GenerateurCouleur, Rendu)

### 2.2 Dépendances
- JavaFX pour l'interface graphique
- Fichiers de ressources (bouton.txt, photo.png) pour l'UI
- Classes de base Java (java.awt, java.util)

## 3. Fichiers Principaux
### 3.1 BoutonItem.java
- **Rôle**: Gère les boutons interactifs dans l'interface
- **Dépendances**: ElementMenu, TexteItem
- **Notes**: Implémente l'interaction utilisateur via clics

### 3.2 Case.java
- **Rôle**: Représente une case du plateau de jeu
- **Dépendances**: Plateau, Point
- **Notes**: Gère l'état de la case (vide, joueur 1, joueur 2)

### 3.3 ChoixValeurItem.java
- **Rôle**: Gère les éléments de sélection de valeur dans les menus
- **Dépendances**: ElementMenu
- **Notes**: Permet de sélectionner des options numériques ou textuelles

### 3.4 ConfigurationJoueurMenu.java
- **Rôle**: Gère la configuration des joueurs dans les menus
- **Dépendances**: ConfigurationPartie, Joueur
- **Notes**: Permet d'ajouter, supprimer ou modifier des joueurs

### 3.5 ConfigurationPartie.java
- **Rôle**: Gère les paramètres de la partie (nombre de joueurs, difficulté, etc.)
- **Dépendances**: MenuParametres, Plateau
- **Notes**: Stocke les paramètres persistants entre les parties

### 3.6 Joueur.java
- **Rôle**: Classe de base pour les joueurs
- **Dépendances**: VraiIA (pour l'intelligence artificielle)
- **Notes**: Interface commune pour JoueurNormal et VraiIA

### 3.7 JoueurNormal.java
- **Rôle**: Implémente un joueur humain
- **Dépendances**: Joueur
- **Notes**: Gère l'input utilisateur pour le placement des pions

### 3.8 Menu.java
- **Rôle**: Gère l'ensemble des menus du jeu
- **Dépendances**: MenuPrincipal, MenuNouvellePartie, MenuFinPartie
- **Notes**: Centralise la navigation entre les écrans

### 3.9 MenuChoixJoueurs.java
- **Rôle**: Permet de sélectionner les joueurs pour une partie
- **Dépendances**: MenuNouvellePartie, ConfigurationJoueurMenu
- **Notes**: Affiche une liste de joueurs disponibles

### 3.10 MenuFinPartie.java
- **Rôle**: Affiche les résultats d'une partie
- **Dépendances**: Menu, PartieSprite
- **Notes**: Permet de relancer une partie ou de quitter

### 3.11 MenuNouvellePartie.java
- **Rôle**: Gère la création d'une nouvelle partie
- **Dépendances**: Menu, ConfigurationPartie
- **Notes**: Permet de paramétrer les options avant de lancer une partie

### 3.12 MenuParametres.java
- **Rôle**: Gère les paramètres généraux du jeu
- **Dépendances**: Menu, ConfigurationPartie
- **Notes**: Permet d'ajuster les paramètres de jeu

### 3.13 MenuPause.java
- **Rôle**: Gère l'écran de pause
- **Dépendances**: Menu, PartieSprite
- **Notes**: Permet de reprendre ou quitter la partie

### 3.14 MenuPrincipal.java
- **Rôle**: Écran d'accueil du jeu
- **Dépendances**: Menu, LogoItem
- **Notes**: Affiche le logo et les options principales

### 3.15 PartieSprite.java
- **Rôle**: Gère l'animation des pions sur le plateau
- **Dépendances**: Plateau, Rendu
- **Notes**: Implémente les effets visuels de placement des pions

### 3.16 Plateau.java
- **Rôle**: Gère la logique du plateau de jeu
- **Dépendances**: Case, Entree, GenerateurCouleur
- **Notes**: Implémente les règles de placement des pions

### 3.17 Point.java
- **Rôle**: Représente une position sur le plateau
- **Dépendances**: Case
- **Notes**: Gère les coordonnées des cases

### 3.18 Rendu.java
- **Rôle**: Gère les rendus graphiques du jeu
- **Dépendances**: Ecran, PartieSprite
- **Notes**: Optimise les performances via des techniques de rendu

### 3.19 VraiIA.java
- **Rôle**: Implémente l'intelligence artificielle pour les joueurs
- **Dépendances**: Joueur
- **Notes**: Utilise un algorithme de sélection de colonnes

## 4. Fichiers de Ressources
### 4.1 bouton.txt
- **Rôle**: Définit les étiquettes des boutons
- **Format**: Lignes de texte correspondant aux boutons (ex: "Nouvelle Partie")
- **Utilisation**: Charge les étiquettes dans l'interface

### 4.2 description.txt
- **Rôle**: Fournit des descriptions détaillées pour les éléments de l'interface
- **Format**: Paires clé-valeur (ex: "bouton_nouvelle_partie: Créer une nouvelle partie")
- **Utilisation**: Utilisé pour afficher des tooltips ou des légendes

### 4.3 photo.png
- **Rôle**: Logo principal du jeu
- **Dimensions**: 512x512 pixels
- **Utilisation**: Affiché dans l'écran principal

### 4.4 photo_small.png
- **Rôle**: Logo réduit pour les menus
- **Dimensions**: 128x128 pixels
- **Utilisation**: Affiché dans les menus secondaires

## 5. Fonctionnalités Clés
### 5.1 Gestion des Parties
- Création de parties via MenuNouvellePartie
- Paramétrage des joueurs (ConfigurationJoueurMenu)
- Sauvegarde/chargement des parties (à implémenter)
- Gestion des erreurs d'entrée utilisateur

### 5.2 Interface Graphique
- Utilisation de JavaFX pour l'affichage
- Support des menus de pause et de fin de partie
- Animation des pions via PartieSprite
- Support des touches de clavier pour la navigation

### 5.3 Intelligence Artificielle
- Implémentation de VraiIA pour les joueurs IA
- Algorithme de sélection de colonnes (à détailler)
- Système de difficulté ajustable (niveau facile, moyen, difficile)

## 6. Notes Techniques
- **Mode Force**: Le mode FORCED_UPDATE active des mises à jour automatiques des ressources
- **Performance**: Optimisation des rendus via Rendu.java
- **Compatibilité**: Testé sur Java 17 avec JavaFX 17
- **Sécurité**: Gestion des exceptions et erreurs d'entrée utilisateur

## 7. Points à Développer
1. Implémenter le système de sauvegarde/chargement
2. Ajouter des effets sonores et animations
3. Développer un système de difficulté pour VraiIA
4. Gérer les erreurs d'entrée utilisateur
5. Ajouter un système de sauvegarde automatique
6. Implémenter un système de reprise de partie
7. Améliorer l'interface graphique avec des effets visuels

## 8. Liens Utiles
- [Documentation JavaFX](https://openjfx.io/)
- [Documentation Java 17](https://docs.oracle.com/en/java/javase/17/)
- [Exemple de jeu de puissance 4](https://github.com/JavaFXExamples/Power4)