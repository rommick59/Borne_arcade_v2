import random
import sys
from pathlib import Path

import pygame

# Key mappings compatible with the borne XKB layout (like Babble_Shot)
KEY_LEFT = {"q", "a", "k"}
KEY_RIGHT = {"d", "m"}
KEY_UP = {"z", "w", "o"}
KEY_DOWN = {"s", "l"}
KEY_SHOOT = {"r"}
KEY_VALIDATE = {"r"}
KEY_MENU = {"f"}

from lane_bot import Robot, TypeRobot
from lane_player import Joueur
from menu_state import EtatMenu


class Jeu:
    LARGEUR, HAUTEUR = 1280, 1024
    FPS = 30
    FULLSCREEN = True

    NB_VOIES = 5
    JOUEUR_Y = 510

    APPARITION_BASE_MS = 520
    APPARITION_MIN_MS = 220
    VITESSE_BASE = 4
    VITESSE_MAX = 10

    DELAI_TIR_MS = 180
    VITESSE_PROJECTILE = 12
    DELAI_DEPLACEMENT_MS = 120

    VIES_MAX = 3
    INVULNERABILITE_MS = 900

    OBJECTIF_SCORE = 180
    OBJECTIF_KILLS = 20

    TYPES_ROBOTS = (
        TypeRobot("normal", 55, (48, 52), 1, 1.0, 5),
        TypeRobot("swift", 25, (42, 46), 1, 1.35, 7),
        TypeRobot("tank", 20, (60, 62), 2, 0.82, 12),
    )
    HIGHSCORE_FILE = Path(__file__).with_name("highscore")
    HIGHSCORE_NAME = "PLYR"

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.joystick.init()

        # adapt to the actual display size and optionally use fullscreen
        info = pygame.display.Info()
        self.LARGEUR = info.current_w if info.current_w > 0 else self.LARGEUR
        self.HAUTEUR = info.current_h if info.current_h > 0 else self.HAUTEUR
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if self.FULLSCREEN:
            flags |= pygame.FULLSCREEN
        self.ecran = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR), flags)
        pygame.display.set_caption("Lane Runner")
        pygame.mouse.set_visible(False)
        self.horloge = pygame.time.Clock()

        self.police = pygame.font.SysFont("verdana", 24)
        self.petite_police = pygame.font.SysFont("verdana", 18)
        self.grande_police = pygame.font.SysFont("verdana", 48, bold=True)

        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self._initialiser_audio()

        self.menu = EtatMenu()
        self.centres_voies = self._centres_voies()
        self.joueur = Joueur(self.centres_voies, self.JOUEUR_Y, self.DELAI_DEPLACEMENT_MS, self.DELAI_TIR_MS)

        self.etat = "menu"  # menu, jeu, saisie_nom, perdu, victoire
        self.meilleur_score = self._charger_meilleur_score()
        self.nom_saisie = list(self.HIGHSCORE_NAME)
        self.index_nom = 0
        self.etat_fin = "perdu"
        self.score_enregistre = False

        self.reinitialiser_partie()

    def _initialiser_audio(self):
        self.audio_actif = False
        self.sons = {}
        self.dernier_son_ms = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.audio_actif = True
        except pygame.error as erreur:
            print(f"[audio] mixeur indisponible: {erreur}")
            return

        base_dir = Path(__file__).resolve().parent
        root_dir = base_dir.parent.parent
        dossier_sons = base_dir / "sounds"
        fallback_bip = root_dir / "sound" / "bip.mp3"

        candidats = {
            "menu_move": [
                dossier_sons / "menu_move.wav",
                dossier_sons / "menu_move.ogg",
                dossier_sons / "menu_move.mp3",
                fallback_bip,
            ],
            "menu_validate": [
                dossier_sons / "menu_validate.wav",
                dossier_sons / "menu_validate.ogg",
                dossier_sons / "menu_validate.mp3",
                fallback_bip,
            ],
            "shoot": [
                dossier_sons / "shoot.wav",
                dossier_sons / "shoot.ogg",
                dossier_sons / "shoot.mp3",
                fallback_bip,
            ],
            "enemy_destroyed": [
                dossier_sons / "enemy_destroyed.wav",
                dossier_sons / "enemy_destroyed.ogg",
                dossier_sons / "enemy_destroyed.mp3",
                fallback_bip,
            ],
            "player_hit": [
                dossier_sons / "player_hit.wav",
                dossier_sons / "player_hit.ogg",
                dossier_sons / "player_hit.mp3",
                fallback_bip,
            ],
            "game_over": [
                dossier_sons / "game_over.wav",
                dossier_sons / "game_over.ogg",
                dossier_sons / "game_over.mp3",
                fallback_bip,
            ],
            "victory": [
                dossier_sons / "victory.wav",
                dossier_sons / "victory.ogg",
                dossier_sons / "victory.mp3",
                fallback_bip,
            ],
        }

        for nom, chemins in candidats.items():
            self.sons[nom] = self._charger_premier_son_disponible(chemins)

    def _charger_premier_son_disponible(self, chemins):
        for chemin in chemins:
            if not chemin.exists():
                continue
            try:
                return pygame.mixer.Sound(str(chemin))
            except pygame.error:
                continue
        return None

    def _jouer_son(self, nom: str, cooldown_ms: int = 0):
        if not self.audio_actif:
            return
        son = self.sons.get(nom)
        if son is None:
            return

        maintenant = pygame.time.get_ticks()
        if cooldown_ms > 0:
            dernier_ms = self.dernier_son_ms.get(nom, -cooldown_ms)
            if maintenant - dernier_ms < cooldown_ms:
                return
            self.dernier_son_ms[nom] = maintenant

        try:
            son.play()
        except pygame.error:
            pass

    @staticmethod
    def _normaliser_nom(nom: str):
        lettres = [c for c in nom.upper() if "A" <= c <= "Z"]
        nom4 = "".join(lettres)[:4]
        return nom4.ljust(4, "A")

    def _lire_highscores(self):
        scores = []
        if not self.HIGHSCORE_FILE.exists():
            return scores
        try:
            lignes = self.HIGHSCORE_FILE.read_text(encoding="utf-8").splitlines()
            for ligne in lignes:
                ligne = ligne.strip()
                if not ligne or "-" not in ligne:
                    continue
                nom, score_str = ligne.split("-", 1)
                try:
                    score = int(score_str.strip())
                except ValueError:
                    continue
                nom = self._normaliser_nom(nom.strip() or self.HIGHSCORE_NAME)
                scores.append((nom, max(0, score)))
        except OSError:
            return []
        scores.sort(key=lambda item: item[1], reverse=True)
        return scores[:10]

    def _charger_meilleur_score(self):
        scores = self._lire_highscores()
        return scores[0][1] if scores else 0

    def _enregistrer_score(self, nom: str):
        scores = self._lire_highscores()
        scores.append((self._normaliser_nom(nom), self.score))
        scores.sort(key=lambda item: item[1], reverse=True)
        scores = scores[:10]
        contenu = "\n".join(f"{nom}-{score}" for nom, score in scores)
        if contenu:
            contenu += "\n"
        try:
            self.HIGHSCORE_FILE.write_text(contenu, encoding="utf-8")
        except OSError:
            pass
        self.meilleur_score = scores[0][1] if scores else self.meilleur_score

    def _terminer_partie(self, etat_final: str):
        self.nom_saisie = list(self.HIGHSCORE_NAME)
        self.index_nom = 0
        self.etat_fin = etat_final
        self.score_enregistre = False
        self.etat = "saisie_nom"
        self._jouer_son("victory" if etat_final == "victoire" else "game_over")

    def _deplacer_selection_nom(self, delta: int):
        self.index_nom = max(0, min(3, self.index_nom + delta))

    def _changer_lettre_nom(self, delta: int):
        courant = self.nom_saisie[self.index_nom]
        code = ord(courant) - ord("A")
        code = (code + delta) % 26
        self.nom_saisie[self.index_nom] = chr(ord("A") + code)

    def _valider_nom(self):
        if self.score_enregistre:
            return
        self._enregistrer_score("".join(self.nom_saisie))
        self.score_enregistre = True
        self.etat = self.etat_fin
        self._jouer_son("menu_validate")

    def _centres_voies(self):
        gauche, droite = 90, self.LARGEUR - 90
        pas = (droite - gauche) // self.NB_VOIES
        return [gauche + i * pas + pas // 2 for i in range(self.NB_VOIES)]

    def reinitialiser_partie(self):
        self.score = 0
        self.kills = 0
        self.vies = self.VIES_MAX
        self.vitesse = float(self.VITESSE_BASE)

        self.joueur.reinitialiser()
        self.robots: list[Robot] = []
        self.projectiles = []

        self.derniere_apparition = pygame.time.get_ticks()
        self.frame = 0

    def _spawn_robot(self):
        type_robot = random.choices(self.TYPES_ROBOTS, [t.poids for t in self.TYPES_ROBOTS], k=1)[0]
        voie = random.randint(0, self.NB_VOIES - 1)
        x = self.centres_voies[voie] - type_robot.taille[0] // 2
        self.robots.append(Robot(type_robot, x))

    def _joystick_x(self):
        if not self.joystick:
            return 0
        if self.joystick.get_numhats() > 0:
            x, _ = self.joystick.get_hat(0)
            if x:
                return x
        if self.joystick.get_numaxes() > 0:
            x = self.joystick.get_axis(0)
            if x > 0.5:
                return 1
            if x < -0.5:
                return -1
        return 0

    def _direction_voie(self):
        touches = pygame.key.get_pressed()
        direction = 0
        if touches[pygame.K_LEFT] or touches[pygame.K_q] or touches[pygame.K_a] or touches[pygame.K_k]:
            direction -= 1
        if touches[pygame.K_RIGHT] or touches[pygame.K_d] or touches[pygame.K_m]:
            direction += 1
        direction_joystick = self._joystick_x()
        return direction if direction != 0 else direction_joystick

    def _tirer(self):
        projectile = self.joueur.tirer(pygame.time.get_ticks())
        if projectile is not None:
            self.projectiles.append(projectile)
            self._jouer_son("shoot", cooldown_ms=40)

    def _demarrer_jeu(self):
        self.reinitialiser_partie()
        self.etat = "jeu"

    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.etat == "menu":
                if evenement.type == pygame.KEYDOWN:
                    # support cabinet keys via event.unicode (like Babble_Shot)
                    try:
                        key_char = evenement.unicode.lower()
                    except Exception:
                        key_char = ""

                    if key_char in KEY_UP or evenement.key in (pygame.K_z, pygame.K_w, pygame.K_o, pygame.K_UP):
                        self.menu.haut()
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_DOWN or evenement.key in (pygame.K_s, pygame.K_l, pygame.K_DOWN):
                        self.menu.bas()
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_VALIDATE or evenement.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                        self._jouer_son("menu_validate")
                        if self.menu.jouer_selectionne:
                            self._demarrer_jeu()
                        else:
                            pygame.quit()
                            sys.exit()
                    elif key_char in KEY_MENU or evenement.key in (pygame.K_ESCAPE, pygame.K_f):
                        pygame.quit()
                        sys.exit()

                if evenement.type == pygame.JOYBUTTONDOWN and evenement.button in (0, 7):
                    self._jouer_son("menu_validate")
                    if self.menu.jouer_selectionne:
                        self._demarrer_jeu()
                    else:
                        pygame.quit()
                        sys.exit()

            elif self.etat == "saisie_nom":
                if evenement.type == pygame.KEYDOWN:
                    try:
                        key_char = evenement.unicode.lower()
                    except Exception:
                        key_char = ""

                    if key_char in KEY_LEFT or evenement.key in (pygame.K_LEFT, pygame.K_q, pygame.K_a, pygame.K_k):
                        self._deplacer_selection_nom(-1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_RIGHT or evenement.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_m):
                        self._deplacer_selection_nom(1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_UP or evenement.key in (pygame.K_UP, pygame.K_z, pygame.K_w, pygame.K_o):
                        self._changer_lettre_nom(1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_DOWN or evenement.key in (pygame.K_DOWN, pygame.K_s, pygame.K_l):
                        self._changer_lettre_nom(-1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif key_char in KEY_SHOOT or evenement.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                        self._valider_nom()
                    elif key_char in KEY_MENU or evenement.key in (pygame.K_ESCAPE, pygame.K_f):
                        self._valider_nom()

                if evenement.type == pygame.JOYHATMOTION:
                    x, y = evenement.value
                    if x < 0:
                        self._deplacer_selection_nom(-1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif x > 0:
                        self._deplacer_selection_nom(1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    if y > 0:
                        self._changer_lettre_nom(1)
                        self._jouer_son("menu_move", cooldown_ms=70)
                    elif y < 0:
                        self._changer_lettre_nom(-1)
                        self._jouer_son("menu_move", cooldown_ms=70)

                if evenement.type == pygame.JOYBUTTONDOWN and evenement.button in (0, 7):
                    self._valider_nom()

            elif self.etat in ("perdu", "victoire"):
                if evenement.type == pygame.KEYDOWN and evenement.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                    self._jouer_son("menu_validate")
                    self.etat = "menu"
                if evenement.type == pygame.JOYBUTTONDOWN and evenement.button in (0, 7):
                    self._jouer_son("menu_validate")
                    self.etat = "menu"

            elif self.etat == "jeu":
                if evenement.type == pygame.KEYDOWN:
                    try:
                        key_char = evenement.unicode.lower()
                    except Exception:
                        key_char = ""

                    if key_char in KEY_MENU or evenement.key in (pygame.K_ESCAPE, pygame.K_f):
                        self.etat = "menu"
                    elif key_char in KEY_SHOOT or evenement.key in (pygame.K_SPACE, pygame.K_r):
                        self._tirer()
                if evenement.type == pygame.JOYBUTTONDOWN and evenement.button == 0:
                    self._tirer()

    def _gerer_collisions(self, maintenant_ms: int):
        robots_morts = set()
        projectiles_utilises = set()

        for i_projectile, projectile in enumerate(self.projectiles):
            for i_robot, robot in enumerate(self.robots):
                if projectile.rect.colliderect(robot.rect):
                    projectiles_utilises.add(i_projectile)
                    if robot.prendre_tir():
                        robots_morts.add(i_robot)
                        self.score += robot.type.points
                        self.kills += 1
                        self._jouer_son("enemy_destroyed", cooldown_ms=30)
                    break

        if projectiles_utilises:
            self.projectiles = [p for i, p in enumerate(self.projectiles) if i not in projectiles_utilises]
        if robots_morts:
            self.robots = [r for i, r in enumerate(self.robots) if i not in robots_morts]

        for robot in self.robots:
            if robot.rect.colliderect(self.joueur.rect) and self.joueur.peut_prendre_hit(maintenant_ms, self.INVULNERABILITE_MS):
                self.joueur.enregistrer_hit(maintenant_ms)
                self.vies -= 1
                self.robots.remove(robot)
                self._jouer_son("player_hit", cooldown_ms=100)
                if self.vies <= 0:
                    self._terminer_partie("perdu")
                break

    def mettre_a_jour(self):
        if self.etat != "jeu":
            return

        maintenant = pygame.time.get_ticks()
        self.joueur.mettre_a_jour_repetition(self._direction_voie(), maintenant)

        delai_spawn = max(self.APPARITION_MIN_MS, self.APPARITION_BASE_MS - int(self.score * 1.7))
        if maintenant - self.derniere_apparition >= delai_spawn:
            self.derniere_apparition = maintenant
            self._spawn_robot()

        self.frame += 1
        if self.frame % 5 == 0:
            self.score += 1

        self.vitesse = min(float(self.VITESSE_MAX), self.VITESSE_BASE + self.score / 75.0)

        for robot in self.robots:
            robot.mettre_a_jour(self.vitesse)
        for projectile in self.projectiles:
            projectile.mettre_a_jour(self.VITESSE_PROJECTILE)

        self.robots = [r for r in self.robots if r.rect.top < self.HAUTEUR + 20]
        self.projectiles = [p for p in self.projectiles if p.rect.bottom > 0]

        self._gerer_collisions(maintenant)

        if self.score >= self.OBJECTIF_SCORE and self.kills >= self.OBJECTIF_KILLS:
            self._terminer_partie("victoire")

    def _texte_centre(self, texte: str, y: int, police: pygame.font.Font, couleur: tuple[int, int, int]):
        surface = police.render(texte, True, couleur)
        self.ecran.blit(surface, surface.get_rect(center=(self.LARGEUR // 2, y)))

    def dessiner_menu(self):
        self.ecran.fill((14, 20, 34))
        self._texte_centre("LANE RUNNER", 150, self.grande_police, (240, 246, 255))
        self._texte_centre("Jouer" if self.menu.jouer_selectionne else "  Jouer", 290, self.police, (255, 235, 130))
        self._texte_centre("Quitter" if not self.menu.jouer_selectionne else "  Quitter", 340, self.police, (255, 200, 190))
        self._texte_centre("Haut/Bas: naviguer  |  R: valider  |  F: quitter", 470, self.petite_police, (170, 190, 220))

    def dessiner_jeu(self):
        self.ecran.fill((8, 12, 20))

        for x in self.centres_voies:
            pygame.draw.line(self.ecran, (40, 62, 98), (x, 0), (x, self.HAUTEUR), 2)

        for robot in self.robots:
            robot.dessiner(self.ecran)

        for projectile in self.projectiles:
            projectile.dessiner(self.ecran)

        self.joueur.dessiner(self.ecran)

        self.ecran.blit(self.petite_police.render(f"Score: {self.score}", True, (235, 245, 255)), (14, 10))
        self.ecran.blit(self.petite_police.render(f"Best: {self.meilleur_score}", True, (180, 245, 190)), (14, 32))
        self.ecran.blit(self.petite_police.render(f"Vies: {self.vies}", True, (255, 210, 170)), (14, 54))
        self.ecran.blit(self.petite_police.render(f"Kills: {self.kills}", True, (255, 230, 170)), (14, 76))

        objectif = f"Objectif: {self.OBJECTIF_SCORE} pts + {self.OBJECTIF_KILLS} kills"
        self.ecran.blit(self.petite_police.render(objectif, True, (170, 185, 210)), (180, 10))
        self.ecran.blit(self.petite_police.render("R tirer  |  F menu", True, (170, 185, 210)), (350, 34))

    def dessiner_fin(self, victoire: bool):
        self.ecran.fill((16, 14, 18) if victoire else (22, 10, 12))
        self._texte_centre("VICTOIRE" if victoire else "GAME OVER", 170, self.grande_police, (190, 255, 215) if victoire else (255, 220, 205))
        self._texte_centre(f"Score: {self.score}", 245, self.police, (236, 246, 255))
        self._texte_centre(f"Kills: {self.kills}", 285, self.police, (236, 246, 255))
        self._texte_centre("R pour revenir au menu", 410, self.petite_police, (180, 200, 220))

    def dessiner_saisie_nom(self):
        victoire = self.etat_fin == "victoire"
        self.ecran.fill((16, 14, 18) if victoire else (22, 10, 12))
        self._texte_centre("VICTOIRE" if victoire else "GAME OVER", 140, self.grande_police, (190, 255, 215) if victoire else (255, 220, 205))
        self._texte_centre(f"Score: {self.score}", 220, self.police, (236, 246, 255))
        self._texte_centre("Entre ton nom (4 lettres)", 300, self.police, (236, 246, 255))

        base_x = self.LARGEUR // 2 - 120
        y = 390
        for i, lettre in enumerate(self.nom_saisie):
            x = base_x + i * 80
            couleur = (255, 240, 150) if i == self.index_nom else (236, 246, 255)
            pygame.draw.rect(self.ecran, (35, 45, 70), pygame.Rect(x - 28, y - 34, 56, 68), border_radius=6)
            pygame.draw.rect(self.ecran, couleur, pygame.Rect(x - 28, y - 34, 56, 68), 2, border_radius=6)
            surface = self.grande_police.render(lettre, True, couleur)
            self.ecran.blit(surface, surface.get_rect(center=(x, y)))

        self._texte_centre("Gauche/Droite: position  |  Haut/Bas: lettre", 500, self.petite_police, (180, 200, 220))
        self._texte_centre("R pour valider", 535, self.petite_police, (180, 200, 220))

    def dessiner(self):
        if self.etat == "menu":
            self.dessiner_menu()
        elif self.etat == "jeu":
            self.dessiner_jeu()
        elif self.etat == "saisie_nom":
            self.dessiner_saisie_nom()
        elif self.etat == "victoire":
            self.dessiner_fin(True)
        else:
            self.dessiner_fin(False)
        pygame.display.flip()

    def run(self):
        while True:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(self.FPS)
