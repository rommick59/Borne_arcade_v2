"""Input helper to track key state from normalized events.

Some controllers/keyboard layouts send characters in `event.unicode` but
the SDL key state may not reflect the expected `pygame.K_*` constants.
We normalize events in __main__.py and update this helper so game code
can query `is_pressed(key)` and get reliable results.
"""
import pygame

_pressed = set()

def on_keydown(key: int):
    try:
        _pressed.add(int(key))
    except Exception:
        pass

def on_keyup(key: int):
    try:
        _pressed.discard(int(key))
    except Exception:
        pass

def is_pressed(key: int) -> bool:
    # First check our synthetic pressed set, then fallback to pygame state
    try:
        if int(key) in _pressed:
            return True
    except Exception:
        pass
    try:
        return pygame.key.get_pressed()[key]
    except Exception:
        return False
