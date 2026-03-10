"""Constantes pour le jeu

Ce fichier contient les constantes utilisées dans le jeu, y compris les dimensions de l'écran, les couleurs, les vitesses et les polices d'écriture.
"""

import pygame
import pygame.font
import pygame.freetype as freetype

# Dimensions de l'écran
# Reduced resolution for low-RAM cabinet (improves FPS and memory)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
BALL_EQUIVALENT = 8
FIRERATE = 7

pygame.font.init()
freetype.init()


class FontWrapper:
	"""Wrapper to provide a `render(text, aa, color)` API backed by pygame.freetype.

	It renders at `scale` times the requested size and smoothscales down to improve
	visual quality (anti-aliasing / less visible pixels) on low-resolution displays.
	"""
	def __init__(self, name: str, size: int, scale: int = 2):
		self.size = size
		self.scale = max(1, int(scale))
		# create a freetype font at scaled size
		try:
			self.font = freetype.SysFont(name, int(size * self.scale))
		except Exception:
			self.font = freetype.SysFont(None, int(size * self.scale))

	def render(self, text: str, aa: bool, color):
		# freetype returns (surface, rect)
		surf, _ = self.font.render(text, fgcolor=color, size=int(self.size * self.scale))
		if self.scale > 1:
			try:
				w, h = surf.get_size()
				surf = pygame.transform.smoothscale(surf, (w // self.scale, h // self.scale))
			except Exception:
				pass
		return surf


# Polices d'écriture (use FontWrapper to improve quality)
FONT = FontWrapper('DejaVu Sans', 30, scale=2)
FONT_SCORE = FontWrapper('DejaVu Sans', 18, scale=2)

# Mapping utilisé par Ball-Blast :
# Navigation : flèches gauche/droite uniquement
LEFT_KEYS = (pygame.K_LEFT,)
RIGHT_KEYS = (pygame.K_RIGHT,)
# Actions : Valider = R, Retour = F, Pause = T
SELECT_KEY = pygame.K_r
BACK_KEY = pygame.K_f
PAUSE_KEY = pygame.K_t
 
# Afficher un compteur FPS à l'écran (utile pour debugging/perf)
FPS_ENABLED = True

# Optionnel: chemin pour logger les FPS si besoin
FPS_LOG_FILE = "logs/ball_blast_fps.log"