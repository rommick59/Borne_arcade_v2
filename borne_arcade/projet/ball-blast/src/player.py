import pygame
from constantes import RED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, LEFT_KEYS, RIGHT_KEYS

"""Module contenant la logique du joueur et de ses roues dans le jeu

Ce module gère la représentation et le comportement du joueur ainsi que
des roues dans le jeu. Il inclut la logique de mouvement, de collision
et de rotation des éléments.
"""

class Player(pygame.sprite.Sprite):
    """Classe représentant le joueur contrôlé par le joueur
    
    Attributes:
        canon: Image du canon du joueur (33x66 pixels)
        rect: Rectangle de collision du joueur
        image: Image actuelle du joueur
        speed_x: Vitesse horizontale du joueur (en pixels par frame)
        score: Score actuel du joueur
        wheelL: Roue gauche du joueur (instance de Wheel)
        wheelR: Roue droite du joueur (instance de Wheel)
    """
    
    def __init__(self):
        """Initialise le joueur avec son canon, position et roues
        
        Paramètres:
            Aucun paramètre requis
            
        Initialisation:
            - Charge l'image du canon et ajuste sa taille
            - Positionne le joueur au centre du bas de l'écran
            - Crée les deux roues avec des décalages respectifs
            - Initialise la vitesse horizontale à 0
            - Initialise le score à 0
        """
        super().__init__()
        self.canon = pygame.transform.scale(pygame.image.load("assets/canon.png"),(33,66))
        self.rect = self.canon.get_rect()
        self.image = self.canon
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        
        self.wheelL = Wheel(-20)
        self.wheelR = Wheel(20)
        
        self.speed_x = 0
        
        self.score = 0

    def update(self):
        """Met à jour la position du joueur et de ses roues
        
        Paramètres:
            Aucun paramètre requis
            
        Logique:
            - Lit les touches clavier pour déterminer la vitesse
            - Met à jour la position horizontale du joueur
            - Déplace et tourne les roues en fonction de la vitesse
            - Gère les collisions avec les bords de l'écran
        """
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        move_left = any(keys[k] for k in LEFT_KEYS)
        move_right = any(keys[k] for k in RIGHT_KEYS)
        if move_left and not move_right:
            self.speed_x = -PLAYER_SPEED
        elif move_right and not move_left:
            self.speed_x = PLAYER_SPEED
        
        w, h = self.image.get_size()
        
        self.rect.x += self.speed_x
        self.wheelL.translate(self.speed_x)
        self.wheelR.translate(self.speed_x)
        self.wheelL.rotate(self.speed_x*-1.4)
        self.wheelR.rotate(self.speed_x*-1.4)
        
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def kill(self):
        """Supprime le joueur et ses roues
        
        Paramètres:
            Aucun paramètre requis
            
        Action:
            - Supprime les roues en appelant leur méthode kill()
            - Appelle la méthode kill() de la classe parente
        """
        self.wheelL.kill()
        self.wheelR.kill()
        super().kill()
    
    def getWheels(self):
        """Retourne les roues du joueur
        
        Retours:
            tuple: Contient les instances Wheel de la roue gauche et droite
            
        Utilisation:
            Permet d'accéder aux roues pour des opérations spécifiques
        """
        return (self.wheelL,self.wheelR)
            
class Wheel(pygame.sprite.Sprite):
    """Classe représentant une roue du joueur
    
    Attributes:
        original_image: Image originale de la roue (25x25 pixels)
        image: Image actuelle de la roue (peut être rotationnée)
        rect: Rectangle de collision de la roue
        xoffset: Décalage horizontal par rapport au centre du joueur
        angleRotated: Angle de rotation actuel en degrés
    """
    
    def __init__(self,xoffset):
        """Initialise une roue avec son décalage et position
        
        Paramètres:
            xoffset (int): Décalage horizontal par rapport au centre du joueur
            
        Initialisation:
            - Charge l'image de la roue et ajuste sa taille
            - Positionne la roue à côté du joueur
            - Initialise l'angle de rotation à 0
        """
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load("assets/wheel.png"),(25,25))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.xoffset = xoffset
        self.rect.centerx = SCREEN_WIDTH // 2 + xoffset
        self.rect.bottom = SCREEN_HEIGHT - 5
        self.angleRotated = 0
        
    def translate(self,x):
        """Déplace la roue horizontalement
        
        Paramètres:
            x (int): Déplacement horizontal
        
        Logique:
            - Met à jour la position horizontale de la roue
            - Gère les collisions avec les bords de l'écran
            - Le décalage xoffset est utilisé pour positionner correctement
              la roue par rapport au joueur
        """
        self.rect.x += x
        if self.rect.right > SCREEN_WIDTH + self.xoffset:
            self.rect.right = SCREEN_WIDTH + self.xoffset
        if self.rect.left < 0 + self.xoffset:
            self.rect.left = 0 + self.xoffset
    
    def rotate(self,angle):
        """Tourne la roue autour de son centre
        
        Paramètres:
            angle (float): Angle de rotation en degrés
        
        Logique:
            - Met à jour l'angle de rotation
            - Crée une nouvelle image rotationnée
            - Ajuste le rectangle de collision pour maintenir le centre
              de rotation
        """
        self.angleRotated += angle
        rotated_image = pygame.transform.rotate(self.original_image,self.angleRotated)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        
        self.image = rotated_image
        self.rect = rotated_rect