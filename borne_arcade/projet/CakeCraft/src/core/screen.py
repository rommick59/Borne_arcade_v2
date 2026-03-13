from core.constants import SCREEN_HEIGHT, SCREEN_WIDTH, ICON_PATH
import pygame

class Screen:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Screen, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.width  = SCREEN_WIDTH
            self.height = SCREEN_HEIGHT
            self.icon   = pygame.image.load(ICON_PATH)
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
            pygame.display.set_icon(self.icon)
            pygame.display.set_caption("CakeCraft")
            self.initialized = True
