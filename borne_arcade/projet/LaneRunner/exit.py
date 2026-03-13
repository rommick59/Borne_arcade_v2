import pygame


class Sortie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.couleur_base = (255, 85, 85)

    def dessiner(self, ecran, pulsation=0):
        halo = 8 + int(4 * pulsation)
        externe = self.rect.inflate(halo, halo)
        pygame.draw.rect(ecran, (120, 20, 20), externe, border_radius=9)
        pygame.draw.rect(ecran, self.couleur_base, self.rect, border_radius=7)
        pygame.draw.rect(ecran, (255, 225, 225), self.rect, 2, border_radius=7)


# Compatibilite anciens imports
Exit = Sortie
