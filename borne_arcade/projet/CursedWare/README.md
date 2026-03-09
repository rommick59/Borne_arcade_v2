```markdown
# Documentation CursedWare

## 1. Aperçu Général
CursedWare est un projet de jeu multiminigames développé avec une structure modulaire. Il intègre des assets graphiques, sonores et des systèmes de gestion de screens. Le projet est conçu pour être extensible, avec des minigames et des composants réutilisables.

## 2. Structure du Projet
### 2.1. Fichiers Principaux
- `Logo.png` : Logo principal du jeu
- `README.txt` : Fichier d'introduction
- `conf.lua` : Configuration globale
- `main.lua` : Point d'entrée principal
- `bouton.txt` : Documentation des boutons
- `description.txt` : Description détaillée du projet
- `photo.png` et `photo_small.png` : Images de présentation

### 2.2. Répertoire Assets
Contient tous les ressources graphiques et sonores :
- **Fonts** : Polices utilisées (Comic, DagestaN, Platinum Sign Over, Arial)
- **imgs** : Images (boutons, sprites, barres de couleur, flèches, effets visuels)
- **musics** : Musiques de fond (Stages, transitions)
- **sounds** : Effets sonores (victoire, défaite, UI, etc.)

### 2.3. Minigames
Liste des minigames intégrés :
- **BroForce** : Jeu de réaction avec monstre et pièce
- **DriftDrawer** : Jeu de dessin avec voiture et drapeau
- **PPAP** : Jeu de correspondance d'objets
- **ShotMasterV1** : Jeu de tir avec bouteilles et vin
- **TEST_GAME** : Jeu de test pour validation de sprites

## 3. Assets Détaillés
### 3.1. Fonts
- `Comic.ttf` : Police principale
- `DagestaN.ttf` : Police pour affichage de texte
- `Platinum Sign Over.ttf` : Police d'affichage
- `arial.ttf` : Police de secours

### 3.2. Images
- `Buttons/*.png` : Boutons de navigation (JOUER, CREDIT, etc.)
- `ColorBar.png` : Barre de couleur pour affichage
- `Explode.png` : Effet d'explosion
- `Heart1.png` et `Heart2.png` : Symboles de vie
- `StudioLogo.png` et `StudioLogoNoBG.png` : Logo de studio
- `bomb.png` : Sprite de bombe

### 3.3. Musiques
- `Stages/*.mp3/ogg` : Musiques de niveaux
- `Stairs.mp3` : Musique de transition

### 3.4. Sons
- `LOSE.ogg` : Son de défaite
- `Victory.mp3` : Son de victoire
- `UI/*.ogg` : Sons d'interface (select, confirm, etc.)

## 4. Systèmes de Gestion
### 4.1. Classes Principales
- `Color.lua` : Gestion des couleurs
- `EventConnection.lua` : Gestion des événements
- `Image.lua` : Gestion des images
- `Quad.lua` : Gestion des quads (sprites)
- `Rect.lua` : Gestion des rectangles
- `Signal.lua` : Gestion des signaux
- `TextLabel.lua` : Gestion des textes
- `Vector2.lua` : Gestion des vecteurs 2D

### 4.2. Librairies
- `Classic.lua` : Classes de base
- `Controls.lua` : Gestion des contrôles
- `Debug/LogManager.lua` : Gestion des logs
- `Delay.lua` : Gestion des délais
- `Input.lua` : Gestion des entrées utilisateur
- `Instance.lua` : Gestion des instances
- `Rendering/Renderer.lua` : Rendu graphique
- `Tween.lua` : Animation de transition

## 5. Screens et Écrans
### 5.1. Écrans Principaux
- `Credits.lua` : Écran de crédits
- `GAME.lua` : Écran de jeu principal
- `Pause.lua` : Écran de pause
- `Scores.lua` : Écran des scores
- `Selection.lua` : Écran de sélection de minigames
- `SubmitScore.lua` : Écran de soumission de score
- `Test.lua` : Écran de test
- `Title.lua` : Écran de titre

### 5.2. Écrans de Test
- `SpritesheetTest.lua` : Test des spritesheets
- `TEST_GAME/game.lua` : Jeu de test pour validation

## 6. Highscore
- Fichier `highscore` : Stockage des scores records

## 7. Notes Techniques
- **MODE FORCE : OUI** : Le projet est en mode de mise à jour forcée
- **FORCED_UPDATE** : Tous les assets et configurations sont redéployés à chaque exécution
- **Compatibilité** : Le projet utilise des formats .lua, .png, .mp3, .ogg pour une portabilité
```