"""Constantes pour le jeu

Ce fichier contient les constantes utilisées dans le jeu, y compris les dimensions de l'écran, les couleurs, les vitesses et les polices d'écriture.
"""

import pygame.font

# Dimensions de l'écran
SCREEN_WIDTH = 1240  #1024 
SCREEN_HEIGHT = 1023  #768 

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Vitesse de déplacement du joueur
PLAYER_SPEED = 10

# Vitesse de la balle
BALL_SPEED_X = 2
BALL_SPEED_FALL = 0.15
BALL_TOP_BOUNCE = -17
BALL_BOTTOM_BOUNCE = -14
BALL_EQUIVALENT = 14
FIRERATE = 7

pygame.font.init()

# Polices d'écriture
FONT = pygame.font.SysFont('Comic Sans MS', 30)
FONT_SCORE = pygame.font.SysFont('Comic Sans MS', 18)