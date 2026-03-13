import pygame
import random
import os
from entity.item.item import Item
from core.position import Position
from core.enums import CakeType
from core.constants import _asset

_COLORS = {
    CakeType.VANILLA_CAKE:     ((230, 168, 10),  (85,  58,  0)),
    CakeType.CHOCOLATE_CAKE:   ((88,  42,  12),  (255, 228, 200)),
    CakeType.STRAWBERRY_CAKE:  ((202, 38,  85),  (255, 238, 244)),
    CakeType.CREAM_PUFF:       ((210, 175, 125), (72,  46,  16)),
    CakeType.CHEWING_GUM_CAKE: ((220, 80,  180), (255, 220, 240)),
    CakeType.BUTTER_BOMB:      ((255, 210, 0),   (120, 80,  0)),
    CakeType.EGG_SURPRISE:     ((255, 240, 100), (140, 100, 0)),
    CakeType.RAINBOW_MESS:     ((180, 80,  220), (255, 255, 180)),
    CakeType.CURSED_TART:      ((40,  20,  60),  (180, 100, 255)),
    CakeType.CLOUD_CAKE:       ((220, 235, 255), (80,  100, 160)),
}

_cake_sprite_paths: list[str] = []
_cake_sprite_paths_loaded = False
_sprite_cache: dict[tuple, pygame.Surface] = {}
_white_cache: dict[tuple, pygame.Surface] = {}


def _ensure_paths_loaded():
    global _cake_sprite_paths, _cake_sprite_paths_loaded
    if _cake_sprite_paths_loaded:
        return
    _cake_sprite_paths_loaded = True
    cakes_dir = _asset('sprites', 'cakes')
    try:
        for fname in os.listdir(cakes_dir):
            if fname.lower().endswith('.png'):
                _cake_sprite_paths.append(os.path.join(cakes_dir, fname))
    except Exception:
        pass


def _get_sprite(path: str, size: int) -> pygame.Surface | None:
    key = (path, size)
    if key not in _sprite_cache:
        try:
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.smoothscale(surf, (size, size))
        except Exception:
            surf = None
        _sprite_cache[key] = surf
    return _sprite_cache[key]


def _get_white(path: str, size: int) -> pygame.Surface | None:
    key = (path, size)
    if key not in _white_cache:
        orig = _get_sprite(path, size)
        if orig is None:
            _white_cache[key] = None
        else:
            w = orig.copy()
            w.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
            _white_cache[key] = w
    return _white_cache[key]


class CakeItem(Item):

    cooked: float = 0.0

    def __init__(self, position: Position, cake_type: CakeType):
        bg, _ = _COLORS.get(cake_type, ((200, 200, 200), (0, 0, 0)))
        super().__init__(position, name=cake_type.value, size=34, color=bg)
        self.cake_type = cake_type
        _ensure_paths_loaded()
        self._sprite_path = random.choice(_cake_sprite_paths) if _cake_sprite_paths else None
        self._blend_surf: pygame.Surface | None = None  # reusable scratch, avoids alloc each frame

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        self._draw_cooked(screen, cx, cy, self.size)

    def render_in_oven(self, screen: pygame.Surface, cx: int, cy: int, size: int):
        self._draw_cooked(screen, cx, cy, size)

    def _draw_cooked(self, screen: pygame.Surface, cx: int, cy: int, size: int):
        if not self._sprite_path:
            self._draw_fallback(screen, cx, cy, size)
            return

        orig = _get_sprite(self._sprite_path, size)
        if orig is None:
            self._draw_fallback(screen, cx, cy, size)
            return

        c = self.cooked

        if c <= 0.0:
            drawn = _get_white(self._sprite_path, size)
        elif c < 1.0:
            white = _get_white(self._sprite_path, size)
            if self._blend_surf is None or self._blend_surf.get_size() != orig.get_size():
                self._blend_surf = white.copy()
            else:
                self._blend_surf.blit(white, (0, 0))
            orig.set_alpha(int(c * 255))
            self._blend_surf.blit(orig, (0, 0))
            orig.set_alpha(None)
            drawn = self._blend_surf
        elif c <= 1.0:
            drawn = orig
        else:
            t = min(1.0, c - 1.0)
            v = int((1.0 - t) * 255)
            if self._blend_surf is None or self._blend_surf.get_size() != orig.get_size():
                self._blend_surf = orig.copy()
            else:
                self._blend_surf.blit(orig, (0, 0))
            self._blend_surf.fill((v, v, v, 255), special_flags=pygame.BLEND_RGBA_MULT)
            drawn = self._blend_surf

        screen.blit(drawn, drawn.get_rect(center=(cx, cy)))

    def _draw_fallback(self, screen: pygame.Surface, cx: int, cy: int, size: int):
        bg, fg = _COLORS.get(self.cake_type, ((200, 200, 200), (0, 0, 0)))
        c = self.cooked
        if c <= 1.0:
            t = max(0.0, c)
            color = (int(255 + (bg[0] - 255) * t), int(255 + (bg[1] - 255) * t), int(255 + (bg[2] - 255) * t))
        else:
            t = min(1.0, c - 1.0)
            color = (int(bg[0] * (1.0 - t)), int(bg[1] * (1.0 - t)), int(bg[2] * (1.0 - t)))
        rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, fg, rect, 2, border_radius=8)
