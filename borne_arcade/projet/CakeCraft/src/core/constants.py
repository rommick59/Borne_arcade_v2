import pygame
import os as _os

# Project root = two levels above this file (CakeCraft/src/core/ → CakeCraft/)
_PROJECT_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

def _asset(*parts) -> str:
    return _os.path.join(_PROJECT_ROOT, 'assets', *parts)

# SCREEN
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 1024

# IMAGE
ICON_PATH = _asset('icon', 'icon.png')

# MENU
MENU_BG_COLOR        = (245, 222, 179)
MENU_TITLE_COLOR     = (101, 56, 27)
MENU_TITLE_FONT_SIZE = 160
MENU_TITLE_Y_OFFSET  = 300

MENU_BTN_COLOR         = (183, 110, 75)
MENU_BTN_HOVER_COLOR   = (210, 140, 100)
MENU_BTN_TEXT_COLOR    = (255, 248, 240)
MENU_BTN_SHADOW_COLOR  = (120, 60, 30)
MENU_BTN_FONT_SIZE     = 56
MENU_BTN_WIDTH         = 360
MENU_BTN_HEIGHT        = 80
MENU_BTN_BORDER_RADIUS = 20
MENU_BTN_SHADOW_OFFSET = 5
MENU_BTN_SPACING       = 110

# MAP
MAP_BG_COLOR         = (255, 255, 255)
MAP_SEPARATOR_COLOR  = (0, 0, 0)
MAP_SEPARATOR_WIDTH  = 4

MAP_KITCHEN_RATIO        = 0.55
MAP_INGREDIENT_BOX_RATIO = 0.70
MAP_CUSTOMER_GAP_RATIO   = 0.35
MAP_COMPTOIR_HEIGHT      = 20
MAP_COMPTOIR_COLOR       = (180, 120, 60)

# PLAYER
PLAYER_SIZE    = 30
PLAYER_SPEED   = 300  # px/s (frame-rate independent)
PLAYER_1_COLOR = (220, 50, 50)
PLAYER_2_COLOR = (50, 100, 220)

PLAYER_SPRITE_PATH  = _asset('sprites', 'player.png')
PLAYER_SPRITE_SCALE = 56
PLAYER_ANIM_FPS     = 8
PLAYER_COLLISION_H  = 14  # hitbox height at feet level

FONT_TITLE_PATH = _asset('fonts', 'Pacifico-Regular.ttf')
FONT_BODY_PATH  = _asset('fonts', 'Nunito-Regular.ttf')

FPS                     = 60
TIME_FAST_FORWARD_SCALE = 10

PLAYER_1_KEYS    = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}
PLAYER_2_KEYS    = {"up": pygame.K_o, "down": pygame.K_l, "left": pygame.K_k, "right": pygame.K_m}
PLAYER_1_INTERACT = pygame.K_6
PLAYER_2_INTERACT = pygame.K_e
PLAYER_1_QUIT    = pygame.K_3
PLAYER_2_QUIT    = pygame.K_d

# CUSTOMER
CUSTOMER_SIZE              = 20
CUSTOMER_SPEED             = 80
CUSTOMER_COLOR             = (100, 180, 100)
CUSTOMER_ANGRY_COLOR       = (200, 80, 80)
CUSTOMER_PATIENCE_BAR_W    = 60
CUSTOMER_PATIENCE_BAR_H    = 8
CUSTOMER_LABEL_FONT_SIZE   = 22
CUSTOMER_SPAWN_INTERVAL    = 8.0
CUSTOMER_MAX_COUNT         = 3

# ITEM
ITEM_SIZE = 30

# DIFFICULTY / GAME
MAX_FAILED_CUSTOMERS = 3
DIFFICULTY_SPEED     = 0.005   # patience multiplier decreases by 0.5% per second
MIN_PATIENCE_RATIO   = 0.45    # patience never drops below ~20s on shortest recipe (45s * 0.45)
MIN_SPAWN_INTERVAL   = 3.0     # fastest spawn rate (seconds)
