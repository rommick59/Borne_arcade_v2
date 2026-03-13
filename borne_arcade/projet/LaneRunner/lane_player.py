import pygame

from lane_bullet import Projectile


class Joueur:
    LARGEUR = 56
    HAUTEUR = 56

    def __init__(self, centres_voies: list[int], y: int, delai_deplacement_ms: int, delai_tir_ms: int):
        self.centres_voies = centres_voies
        self.delai_deplacement_ms = delai_deplacement_ms
        self.delai_tir_ms = delai_tir_ms

        self.rect = pygame.Rect(0, y, self.LARGEUR, self.HAUTEUR)
        self.voie = len(centres_voies) // 2
        self.dernier_tir = 0
        self.dernier_hit = 0
        self.prochain_deplacement = 0
        self.direction_maintenue = 0
        self.definir_voie(self.voie)

    def reinitialiser(self):
        self.voie = len(self.centres_voies) // 2
        self.dernier_tir = 0
        self.dernier_hit = 0
        self.prochain_deplacement = 0
        self.direction_maintenue = 0
        self.definir_voie(self.voie)

    def definir_voie(self, voie: int):
        self.voie = max(0, min(len(self.centres_voies) - 1, voie))
        self.rect.centerx = self.centres_voies[self.voie]

    def deplacer_voie(self, direction: int):
        self.definir_voie(self.voie + direction)

    def mettre_a_jour_repetition(self, direction: int, maintenant_ms: int):
        if direction == 0:
            self.direction_maintenue = 0
            return

        pas = -1 if direction < 0 else 1
        if direction != self.direction_maintenue or maintenant_ms >= self.prochain_deplacement:
            self.deplacer_voie(pas)
            self.prochain_deplacement = maintenant_ms + self.delai_deplacement_ms
        self.direction_maintenue = direction

    def tirer(self, maintenant_ms: int) -> Projectile | None:
        if maintenant_ms - self.dernier_tir < self.delai_tir_ms:
            return None
        self.dernier_tir = maintenant_ms
        return Projectile(self.rect.centerx, self.rect.top + 10)

    def peut_prendre_hit(self, maintenant_ms: int, invulnerabilite_ms: int) -> bool:
        return maintenant_ms - self.dernier_hit > invulnerabilite_ms

    def enregistrer_hit(self, maintenant_ms: int):
        self.dernier_hit = maintenant_ms

    def dessiner(self, ecran: pygame.Surface):
        flash = (pygame.time.get_ticks() - self.dernier_hit) < 180
        couleur = (255, 205, 120) if flash else (120, 230, 170)
        pygame.draw.rect(ecran, couleur, self.rect, border_radius=8)
        pygame.draw.rect(ecran, (210, 255, 225), self.rect, 1, border_radius=8)
