import pygame


class Projectile:
    LARGEUR = 8
    HAUTEUR = 16

    def __init__(self, centre_x: int, bas_y: int):
        self.rect = pygame.Rect(0, 0, self.LARGEUR, self.HAUTEUR)
        self.rect.centerx = centre_x
        self.rect.bottom = bas_y

    def mettre_a_jour(self, vitesse: int):
        self.rect.y -= vitesse

    def dessiner(self, ecran: pygame.Surface):
        pygame.draw.rect(ecran, (255, 240, 120), self.rect, border_radius=3)
