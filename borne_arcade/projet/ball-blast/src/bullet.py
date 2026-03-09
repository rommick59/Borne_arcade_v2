"""Module contenant la classe Bullet pour représenter des balles dans un jeu."""

import pygame
from constantes import RED

class Bullet(pygame.sprite.Sprite):
    """Classe représentant une balle dans un jeu, héritant de pygame.sprite.Sprite.
    
    Attributes:
        image (pygame.Surface): Surface de la balle (rouge).
        rect (pygame.Rect): Rectangle de la balle, positionné au centre x et bas y.
        speed_y (int): Vitesse verticale de la balle (vers le haut).
    """
    def __init__(self, x: int, y: int):
        """Initialise une nouvelle balle.
        
        Args:
            x (int): Coordonnée x du centre de la balle.
            y (int): Coordonnée y du bas de la balle.
        
        Returns:
            None
        
        Raises:
            None
        """
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y: int = 10

    def update(self):
        """Met à jour la position de la balle.
        
        La balle se déplace vers le haut à la vitesse speed_y. Si la balle sort du haut de l'écran, elle est supprimée.
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        self.rect.y -= self.speed_y
        if self.rect.bottom < 0:
            self.kill()