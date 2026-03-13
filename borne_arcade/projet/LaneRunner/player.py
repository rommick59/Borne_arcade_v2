import pygame


class Joueur:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.couleur = (80, 240, 140)
        self.vitesse = 3

    def deplacer(self, dx, dy, murs):
        self.rect.x += dx
        for mur in murs:
            if self.rect.colliderect(mur.rect):
                if dx > 0:
                    self.rect.right = mur.rect.left
                if dx < 0:
                    self.rect.left = mur.rect.right

        self.rect.y += dy
        for mur in murs:
            if self.rect.colliderect(mur.rect):
                if dy > 0:
                    self.rect.bottom = mur.rect.top
                if dy < 0:
                    self.rect.top = mur.rect.bottom

    def dessiner(self, ecran):
        centre = self.rect.center
        rayon = self.rect.width // 2
        pygame.draw.circle(ecran, (20, 30, 20), (centre[0], centre[1] + 2), rayon)
        pygame.draw.circle(ecran, self.couleur, centre, rayon)
        pygame.draw.circle(ecran, (220, 255, 235), (centre[0] + 3, centre[1] - 4), 3)


# Compatibilite anciens imports
Player = Joueur
