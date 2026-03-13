import pygame
from core.constants import _asset

_SIZE = 32  # display size in px

_cache: dict[str, pygame.Surface | None] = {}


def _load(name: str) -> pygame.Surface | None:
    if name in _cache:
        return _cache[name]
    try:
        surf = pygame.image.load(_asset('button', name)).convert_alpha()
        surf = pygame.transform.smoothscale(surf, (_SIZE, _SIZE))
    except Exception:
        surf = None
    _cache[name] = surf
    return surf


def get_button_image(activate_key: int) -> pygame.Surface | None:
    """Return the button image for a given pygame key constant, or None."""
    import pygame as _pg
    _KEY_MAP = {
        _pg.K_3: 'b_6.png',
        _pg.K_4: 'b_4.png',
        _pg.K_5: 'b_5.png',
        _pg.K_6: 'b_3.png',
        _pg.K_1: 'b_1.png',
        _pg.K_2: 'b_2.png',
        _pg.K_e: 'r_3.png',
        _pg.K_q: 'r_4.png',
        _pg.K_s: 'r_5.png',
        _pg.K_d: 'r_6.png',
        _pg.K_a: 'r_1.png',
        _pg.K_z: 'r_2.png',
    }
    fname = _KEY_MAP.get(activate_key)
    return _load(fname) if fname else None
