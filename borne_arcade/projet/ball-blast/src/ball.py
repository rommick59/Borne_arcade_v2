import random
import pygame
import math
from constantes import RED, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BALL_SPEED_X, BALL_SPEED_FALL, BALL_TOP_BOUNCE, BALL_BOTTOM_BOUNCE

# Font
pygame.init()
font = pygame.font.SysFont('Arial', 24)

"""
Module ball

Ce module contient la classe Ball qui représente une balle dans un jeu. La balle possède une forme irrégulière, des points de vie, et des mécaniques de collision.
"""

class Ball(pygame.sprite.Sprite):
    """
    Classe représentant une balle dans un jeu. La balle possède une forme irrégulière, des points de vie, et des mécaniques de collision.

    Attributes:
        image: Surface pygame représentant la balle
        level: Niveau de la balle
        life: Nombre de vies restantes
        color: Couleur de la balle
        radius: Rayon de la balle
        points: Points de la forme irrégulière
        life_points: Points de vie affichés
        mask: Masque de collision
        rect: Rectangle de collision
        speed_y: Vitesse verticale
        speed_x: Vitesse horizontale
    """

    def __init__(self, x: int, y: int, radius: int, level: int = 0, color = RED):
        """
        Constructeur de la classe Ball.

        Args:
            x: Position x de la balle
            y: Position y de la balle
            radius: Rayon de la balle
            level: Niveau de la balle (par défaut 0)
            color: Couleur de la balle (par défaut RED)
        """
        super().__init__()
        # Créer une surface transparente
        self.image = pygame.Surface((radius*2, radius*3), pygame.SRCALPHA)
        self.level: int = level
        self.life: int = 3
        self.color = color
        self.radius: int = radius
        
        # Générer des points pour créer un polygone irrégulier
        self.points = self._generate_rock_shape()
        
        # Dessiner le polygone sur la surface
        pygame.draw.polygon(self.image, self.color, self.points)
        
        # Dessiner les points de vie
        self.base_life_points:int = random.randint(1, round(radius*0.75))
        self.life_points:int = self.base_life_points
        self.life_points_surface = font.render(str(self.life_points), True, WHITE)
        self.life_points_surface_rect = self.life_points_surface.get_rect()
        self.life_points_surface_rect.center = (self.radius, self.radius)
        self.image.blit(self.life_points_surface, self.life_points_surface_rect)
        
        # Créer un masque de collision pour une détection plus précise
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Vitesse de déplacement
        self.speed_y: int = -2
        self.speed_x: int = random.randint(1*BALL_SPEED_X, 2*BALL_SPEED_X) * (-1)**random.randint(1, 2)
    
    def _generate_rock_shape(self):
        """
        Génère des points pour créer une forme de roche irrégulière.

        Returns:
            Liste de points (x, y) formant la forme irrégulière.
        """
        points = []
        num_points = random.randint(6, 8)  # Nombre de points du polygone
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            # Ajouter une variation aléatoire au rayon
            x = self.radius + self.radius * math.cos(angle)
            y = self.radius + self.radius * math.sin(angle)
            points.append((int(x), int(y)))
            
        return points
    
    def update(self):
        """
        Met à jour la position de la balle et gère les collisions.
        """
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        # Rebond horizontal sur les bords gauche/droite
        self.speed_x = -self.speed_x if (self.rect.left < 0 and self.speed_x < 0) or (self.rect.right > SCREEN_WIDTH and self.speed_x > 0) else self.speed_x

        # Gravité et rebond bas
        self.speed_y = random.randint(BALL_TOP_BOUNCE, BALL_BOTTOM_BOUNCE) if self.rect.bottom > SCREEN_HEIGHT else self.speed_y + BALL_SPEED_FALL

        # Empêcher la balle de dépasser le bord supérieur de l'écran
        if self.rect.top < 0:
            self.rect.top = 0
            # Si la balle se déplaçait vers le haut, forcer une vitesse vers le bas
            if self.speed_y < 0:
                self.speed_y = abs(self.speed_y)
        
    def take_damage(self) -> bool:
        """
        Réduit les points de vie de la balle. Retourne True si la balle est détruite.

        Returns:
            bool: True si la balle est détruite (points de vie == 0), False sinon.
        """
        self.life_points -= 1
        
        self.life_points_surface = font.render(str(self.life_points), True, WHITE)
        self.life_points_surface_rect = self.life_points_surface.get_rect()
        self.life_points_surface_rect.center = (self.radius, self.radius)
        
        self.image = pygame.Surface((self.image.get_rect().width, self.image.get_rect().width), pygame.SRCALPHA)
        
        pygame.draw.polygon(self.image, self.color, self.points)
        self.image.blit(self.life_points_surface, self.life_points_surface_rect)
        
        # Mettre à jour le masque de collision
        self.mask = pygame.mask.from_surface(self.image)
        return self.life_points == 0
        
    def decale(self, decale: int):
        """
        Déplace la balle horizontalement de 'decale' pixels.

        Args:
            decale: Nombre de pixels à déplacer (positif ou négatif)
        """
        self.rect.x += decale
        
        if self.speed_x * decale < 0:
            self.speed_x *= -1
    
    def level(self)->int:
        """
        Retourne le niveau de la balle.

        Returns:
            int: Niveau de la balle
        """
        return self.level
