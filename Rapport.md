# Documentation — SAE Borne Arcade

## Sommaire

1. [Vue d'ensemble](#1-vue-densemble)
2. [Automatisation de la documentation](#2-automatisation-de-la-documentation)
   - 2.1 [Modules disponibles](#21-modules-disponibles)
   - 2.2 [Analyse des deprecated](#22-analyse-des-deprecated--verif_deprecatedpy)
   - 2.3 [Gestion des README](#23-gestion-des-readme--verify_and_update_readmepy)
   - 2.4 [Documentation des fichiers sources](#24-documentation-des-fichiers-sources--verify_and_update_docspy)
   - 2.5 [Guide utilisateur](#25-guide-utilisateur--verify_and_update_doc_userpy)
3. [Automatisation de l'installation](#3-automatisation-de-linstallation)
   - 3.1 [Détection d'architecture](#31-détection-darchitecture)
   - 3.2 [Dépendances installées](#32-dépendances-installées)
   - 3.3 [Configuration post-installation](#33-configuration-post-installation)
   - 3.4 [Montée de version](#34-montée-de-version--upgrade_allsh)
4. [Déploiement automatisé via Git](#4-déploiement-automatisé-via-git)
   - 4.1 [Installation du hook](#41-installation-du-hook)
   - 4.2 [Chaîne de déploiement](#42-chaîne-de-déploiement-complète)
   - 4.3 [Comportement différentiel](#43-comportement-différentiel)
5. [Ajout d'un nouveau jeu](#5-ajout-dun-nouveau-jeu)
   - 5.1 [Procédure d'ajout](#51-procédure-dajout)
   - 5.2 [Détection automatique](#52-détection-automatique)
   - 5.3 [Guide pas à pas](#53-guide-pas-à-pas)
6. [Tests et validation](#6-tests-et-validation)
   - 6.1 [Choix du moteur LLM](#61-choix-du-moteur-llm)
   - 6.2 [Résultats des tests](#62-résultats-des-tests)
   - 6.3 [Limites identifiées](#63-limites-identifiées)

---

## 1. Vue d'ensemble

Le système couvre quatre domaines d'automatisation principaux :

- Génération de documentation (README, docstrings, guide utilisateur, rapport de deprecated)
- Installation et montée de version sur Raspberry Pi
- Déploiement continu via git hooks
- Ajout et intégration de nouveaux jeux dans la borne

---

## 2. Automatisation de la documentation

### 2.1 Modules disponibles

| Module | Fichier | Rôle |
|---|---|---|
| `DeprecatedAnalyzer` | `verif_deprecated.py` | Analyse les logs de compilation Java et génère un rapport Markdown des warnings/erreurs de dépréciation |
| `ReadmeManager` | `verify_and_update_readme.py` | Audite et met à jour les README de chaque projet selon des critères stricts |
| `DocsManager` | `verify_and_update_docs.py` | Ajoute/met à jour les docstrings dans les fichiers sources `.py`, `.java`, `.lua` |
| `UserDocManager` | `verify_and_update_doc_user.py` | Génère le guide utilisateur global de la borne arcade |

---

### 2.2 Analyse des deprecated — `verif_deprecated.py`

Ce module lit le fichier `borne_arcade/logs/compilation.log`, l'envoie au LLM avec un prompt structuré, et écrit le rapport dans `borne_arcade/logs/deprecated.md`.

**Format du rapport généré (4 sections obligatoires) :**

| Section | Contenu |
|---|---|
| **Problème** | Résumé en une phrase du ou des problèmes détectés |
| **Compilations concernées** | Liste structurée par jeu, fichier et ligne |
| **Solution** | Explication de la correction à apporter |
| **Exemple de correction** | Blocs de code `AVANT` / `APRÈS` |

---

### 2.3 Gestion des README — `verify_and_update_readme.py`

Ce module inspecte chaque projet dans `borne_arcade/projet/` et décide si le README doit être régénéré selon deux modes :

- **Mode normal** : le projet contient des fichiers modifiés depuis HEAD (`git diff --name-only HEAD`)
- **Mode forcé (`--force`)** : tous les projets sont traités systématiquement

**Critères de validation — le LLM répond `DOC_OK` uniquement si :**

- La documentation est écrite en français impeccable
- La structure obligatoire est respectée
- Chaque section contient un contenu précis et exploitable
- Le contenu correspond réellement à la structure du projet
- Le contenu n'est ni vague, ni minimal, ni marketing
- Aucune section n'est vide

---

### 2.4 Documentation des fichiers sources — `verify_and_update_docs.py`

Ce module parcourt récursivement les fichiers source de chaque projet modifié et enrichit leur documentation inline. Trois langages sont supportés :

| Extension | Langage | Style de documentation généré |
|---|---|---|
| `.py` | Python | Docstrings Google Style (`Args:`, `Returns:`, `Raises:`) |
| `.java` | Java | Javadoc avec `@param`, `@return`, `@throws` |
| `.lua` | Lua | Commentaires LuaDoc (`---`, `@param`, `@return`) |

> **Mécanisme de nettoyage** — La méthode `strip_markdown_fences()` supprime les balises ` ``` ` que le LLM peut introduire en début et fin de réponse, garantissant un fichier source propre sans artefacts Markdown.

---

### 2.5 Guide utilisateur — `verify_and_update_doc_user.py`

Ce module génère le fichier `borne_arcade/docs/USER_GUIDE.md`, destiné aux utilisateurs finaux non techniques.

**La régénération est déclenchée uniquement dans les cas suivants :**

- Un README de projet est ajouté ou supprimé (nouveau jeu ou jeu retiré)
- Un script `.sh` est ajouté ou supprimé à la racine de `borne_arcade/`
- Le mode forcé est activé

---

## 3. Automatisation de l'installation

Le script `install.sh` orchestre l'installation complète de la borne sur une machine vierge. Il détecte l'architecture matérielle et adapte les versions des dépendances en conséquence.

### 3.1 Détection d'architecture

La variable `ARCH` est déterminée via `dpkg --print-architecture` et conditionne la version de Python installée :

| Architecture | Description | Version Python |
|---|---|---|
| `i386` / `armhf` | Raspberry Pi 32 bits | Python 3.11.11 |
| `amd64` / `arm64` | 64 bits | Python 3.13.1 |

---

### 3.2 Dépendances installées

| Dépendance | Méthode d'installation | Vérification |
|---|---|---|
| Java (JDK) | `apt install default-jdk` | `java -version` |
| Python 3 | Compilation depuis les sources si absent | `python3 --version` |
| Pygame | `pip install pygame` | `import pygame` |
| Lua 5.4 | `apt install lua5.4` | `lua -v` |
| MG2D | `git clone` depuis GitHub | Présence du dossier `~/MG2D` |

---

### 3.3 Configuration post-installation

Après l'installation des dépendances, le script exécute les étapes suivantes dans l'ordre :

1. Copie la configuration clavier personnalisée vers `/usr/share/X11/xkb/symbols/borne`
2. Configure les git hooks via `setup-hooks.sh`
3. Lance la borne arcade (`lancerBorne.sh`)
4. Exécute `manager.py --force` pour générer toute la documentation initiale

> **Démarrage automatique** — `lancerBorne.sh` est configuré pour se lancer automatiquement au démarrage de la borne. À chaque mise sous tension, la borne démarre directement sur l'interface de sélection des jeux, sans intervention manuelle.

---

### 3.4 Montée de version — `upgrade_all.sh`

Le script `upgrade_all.sh` automatise la montée de version complète du système en 6 étapes séquentielles :

| Étape | Commande | Action |
|---|---|---|
| 1 | `apt-get update` | Synchronisation des dépôts |
| 2 | `apt-get upgrade` | Mise à jour des paquets installés |
| 3 | `dist-upgrade` | Mise à niveau complète avec changements de dépendances |
| 4 | `autoremove --purge` | Suppression des paquets devenus inutiles |
| 5 | `clean` + `autoclean` | Nettoyage du cache APT |
| 6 | `-f install` | Vérification et réparation des paquets cassés |

---

## 4. Déploiement automatisé via Git

L'automatisation du déploiement repose sur un hook git `post-merge` qui se déclenche automatiquement après chaque `git pull` réussi.

### 4.1 Installation du hook

Le script `setup-hooks.sh` copie le fichier `post-merge` dans le répertoire `.git/hooks/` et lui attribue les droits d'exécution. Cette installation est déclenchée automatiquement par `install.sh`.

---

### 4.2 Chaîne de déploiement complète

```
git pull
  └─→ post-merge hook
        └─→ manager.py
              └─→ verif_deprecated.py
              └─→ ReadmeManager
              └─→ DocsManager
              └─→ UserDocManager
                    └─→ Documentation à jour automatiquement
```

---

### 4.3 Comportement différentiel

Le système ne traite que ce qui a changé, ce qui le rend performant sur Raspberry Pi.

| Mode | Déclencheur | Portée |
|---|---|---|
| **Normal** (post-merge) | `git pull` avec modifications | Uniquement les projets/fichiers modifiés |
| **Forcé** (`--force`) | Lancement manuel ou première installation | Tous les projets sans exception |

---

## 5. Ajout d'un nouveau jeu

### 5.1 Procédure d'ajout

1. Créer un dossier dans `borne_arcade/projet/<nom_du_jeu>/`
2. Y placer les fichiers sources du jeu (`.py`, `.java`, `.lua` selon le langage)
3. Committer et pousser sur le dépôt git
4. Sur la borne, effectuer un `git pull`

---

### 5.2 Détection automatique

Le système détecte l'ajout d'un nouveau jeu via `git diff --name-status HEAD`. Si un fichier `README.md` apparaît sous `borne_arcade/projet/<nom>/`, le projet est considéré comme nouveau et l'ensemble de la documentation associée est générée automatiquement.

---

### 5.3 Guide pas à pas

#### Étape 1 — Créer le dossier du jeu

```bash
mkdir -p projet/MonJeu
```

> Utilise un nom simple, sans espace. Ce nom apparaîtra dans le menu de la borne.

---

#### Étape 2 — Ajouter les fichiers minimum

Dans `projet/MonJeu/`, ajouter au moins :

- `description.txt` — description du jeu
- `bouton.txt` — mapping des contrôles
- Les fichiers sources du jeu (`main.py`, `Main.java`, etc.)

**Format de `bouton.txt`** — une ligne avec 7 champs séparés par `:` :

```
Joystick:BoutonA:BoutonB:BoutonC:BoutonX:BoutonY:BoutonZ
```

Exemple :

```
Deplacement:Tirer:Sauter:Pause:Menu:Option1:Option2
```

> **`highscore` (optionnel)** — si le jeu gère des scores, ajouter un fichier `highscore`. Sinon, le menu affichera `/`.

---

#### Étape 3 — Créer le script de lancement

Le menu lance `./NomDuJeu.sh` depuis la racine `borne_arcade/`. Si le dossier est `projet/MonJeu/`, créer `MonJeu.sh` à la racine.

**Exemple Python :**

```bash
#!/bin/bash
cd projet/MonJeu || exit 1
python3 main.py
```

**Exemple Java :**

```bash
#!/bin/bash
cd projet/MonJeu || exit 1
javac -cp .:../..:$HOME *.java
java -cp .:../..:$HOME Main
```

Rendre le script exécutable :

```bash
chmod +x MonJeu.sh
```

---

#### Étape 4 — Lancer la borne

```bash
./lancerBorne.sh
```

Le jeu doit apparaître automatiquement dans la liste. Il faut être dans le dossier `borne_arcade` (cd borne_arcade).

> **Note** — `lancerBorne.sh` se lance automatiquement au démarrage de la borne. Il n'est donc nécessaire de l'exécuter manuellement que lors du développement ou après un redémarrage en dehors du contexte normal d'utilisation.

---

#### Dépannage rapide

| Symptôme | Vérification |
|---|---|
| Le jeu n'apparaît pas dans le menu | Le dossier est bien dans `projet/` |
| Le jeu ne se lance pas | `MonJeu.sh` existe à la racine et a le droit `+x` |
| Les contrôles ne s'affichent pas | `bouton.txt` contient bien 7 champs séparés par `:` |

---

## 6. Tests et validation

Les procédures automatisées ont été testées directement sur la borne arcade.

### 6.1 Choix du moteur LLM

L'outil **ReadmeAI** (`eli64s`) avait été envisagé pour la génération automatique des README. Son installation sur Raspberry Pi s'est révélée impossible en raison de contraintes de compatibilité avec l'architecture ARM.

**Solution adoptée** : Ollama avec le modèle **Qwen3:8b**, disponible localement sur la borne. Cette solution est plus lente mais fonctionne entièrement hors-ligne, sans aucune dépendance externe.

---

### 6.2 Résultats des tests

| Fonctionnalité testée | Résultat | Observations |
|---|---|---|
| Génération README (projets simples) | ✅ Fonctionnel | Documentation conforme aux critères |
| Docstrings Python (fichiers < 200 lignes) | ✅ Fonctionnel | Google Style correctement appliqué |
| Docstrings Python (fichiers > 400 lignes) | ⚠️ Partiel | Le LLM peut supprimer du code lors de la génération |
| Analyse des deprecated Java | ✅ Fonctionnel | Rapport structuré en 4 sections généré |
| Guide utilisateur | ✅ Fonctionnel | Mise à jour déclenchée sur ajout/suppression de projet |
| Hook post-merge | ✅ Fonctionnel | Exécution automatique après `git pull` confirmée |
| `install.sh` sur Raspberry Pi | ✅ Fonctionnel | Détection d'architecture et installation adaptée |
| `upgrade_all.sh` | ✅ Fonctionnel | Montée de version sans intervention manuelle |

---

### 6.3 Limites identifiées

#### Limite 1 — Fichiers sources volumineux

Lorsqu'un fichier source est très volumineux (ex. `ball-blast/game.py`), le LLM peut supprimer une partie du code dans sa réponse au lieu de le compléter. Ce comportement est dû à la fenêtre de contexte limitée du modèle et à sa tendance à résumer plutôt qu'à restituer intégralement le contenu.

#### Limite 2 — Performances sur Raspberry Pi

`Qwen3:8b` est significativement plus lent sur Raspberry Pi que sur une machine de bureau. La génération d'un README peut prendre plusieurs minutes. En mode forcé sur de nombreux projets, le temps total peut devenir très long.

#### Limite 3 — Absence de tests fonctionnels réels

Les vérifications automatisées se limitent à contrôler l'existence de fichiers après exécution. Ce type de vérification ne constitue pas un test fonctionnel : il ne valide pas que le contenu généré est correct, ni que les fonctions du code se comportent comme attendu.