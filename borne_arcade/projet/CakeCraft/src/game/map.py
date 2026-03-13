import pygame
from core.screen import Screen
from core.constants import (
    MAP_BG_COLOR, MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO,
    CUSTOMER_SPAWN_INTERVAL, CUSTOMER_MAX_COUNT,
    DIFFICULTY_SPEED, MIN_PATIENCE_RATIO, MIN_SPAWN_INTERVAL,
    _asset,
)
from game.player_zone import PlayerZone
from core.enums import Side
from recipe.catalog import RecipeCatalog

_floor_kitchen: pygame.Surface | None = None
_floor_outside: pygame.Surface | None = None
_tile_cache: dict = {}


def _load_floor_tiles():
    global _floor_kitchen, _floor_outside
    if _floor_kitchen is not None:
        return
    try:
        raw = pygame.image.load(_asset('floor_texture.JPG')).convert()
        tw, th = raw.get_size()
        _floor_kitchen = pygame.transform.scale(raw, (tw // 3, th // 3))
    except Exception:
        _floor_kitchen = None
    try:
        _floor_outside = pygame.image.load(_asset('oldstone.png')).convert()
    except Exception:
        _floor_outside = None


def _tile(screen: pygame.Surface, tile: pygame.Surface, rect: pygame.Rect):
    tw, th = tile.get_size()
    for y in range(rect.top, rect.bottom, th):
        for x in range(rect.left, rect.right, tw):
            screen.blit(tile, (x, y))


class Map:
    def __init__(self, bot_left: bool = False, bot_right: bool = False):
        from game.bot_zone import BotZone
        self.screen     = Screen().screen
        self.running    = True
        self.zone_left  = BotZone(self.screen, Side.LEFT)  if bot_left  else PlayerZone(self.screen, Side.LEFT)
        self.zone_right = BotZone(self.screen, Side.RIGHT) if bot_right else PlayerZone(self.screen, Side.RIGHT)
        self.clock       = pygame.time.Clock()

        # Spawn timer
        self._spawn_timer = CUSTOMER_SPAWN_INTERVAL

        # Difficulty / elapsed time
        self._elapsed     = 0.0
        self._left_lost   = False
        self._right_lost  = False
        self.game_over    = False

    def draw(self):
        _load_floor_tiles()
        w, h = self.screen.get_width(), self.screen.get_height()
        kitchen_y = int(h * MAP_KITCHEN_RATIO)

        # Kitchen floor (top half)
        kitchen_rect = pygame.Rect(0, 0, w, kitchen_y)
        if _floor_kitchen:
            _tile(self.screen, _floor_kitchen, kitchen_rect)
        else:
            pygame.draw.rect(self.screen, MAP_BG_COLOR, kitchen_rect)

        # Outside floor (bottom half — customer area)
        outside_rect = pygame.Rect(0, kitchen_y, w, h - kitchen_y)
        if _floor_outside:
            _tile(self.screen, _floor_outside, outside_rect)
        else:
            pygame.draw.rect(self.screen, MAP_BG_COLOR, outside_rect)

        # Vertical separator
        center_x = w // 2
        pygame.draw.line(self.screen, MAP_SEPARATOR_COLOR,
                         (center_x, 0), (center_x, h),
                         MAP_SEPARATOR_WIDTH)

        # Horizontal separator (kitchen / shop)
        pygame.draw.line(self.screen, MAP_SEPARATOR_COLOR,
                         (0, kitchen_y), (w, kitchen_y),
                         MAP_SEPARATOR_WIDTH)

        self.zone_left.draw()
        self.zone_right.draw()

        pygame.display.flip()

    def update(self, dt: float):
        self._elapsed += dt

        # Difficulty: patience ratio decreases over time (1.0 → MIN_PATIENCE_RATIO)
        difficulty = max(MIN_PATIENCE_RATIO, 1.0 - self._elapsed * DIFFICULTY_SPEED)

        # Spawn interval also shrinks with difficulty
        spawn_interval = max(MIN_SPAWN_INTERVAL, CUSTOMER_SPAWN_INTERVAL * difficulty)

        # Synchronized customer spawning
        self._spawn_timer -= dt
        if self._spawn_timer <= 0:
            if (len(self.zone_left._customers) < CUSTOMER_MAX_COUNT or
                    len(self.zone_right._customers) < CUSTOMER_MAX_COUNT):
                recipe = RecipeCatalog.random()
                self.zone_left.try_spawn(recipe, difficulty)
                self.zone_right.try_spawn(recipe, difficulty)
            self._spawn_timer = spawn_interval

        # Zone updates
        self.zone_left.update(dt)
        self.zone_right.update(dt)

        # Check for individual zone losses
        if not self._left_lost and self.zone_left.has_lost():
            self._left_lost          = True
            self.zone_left.lost_time = self._elapsed

        if not self._right_lost and self.zone_right.has_lost():
            self._right_lost          = True
            self.zone_right.lost_time = self._elapsed

        self.game_over = self._left_lost and self._right_lost
