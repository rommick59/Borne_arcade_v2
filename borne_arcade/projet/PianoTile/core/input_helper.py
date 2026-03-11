"""Input helper to track key state from normalized events for PianoTile.

This mirrors the approach used in ball-blast: some devices send characters
in `event.unicode` while SDL's key state may not reflect the expected
`pygame.K_*` constants. We keep a synthetic pressed set that the game can
query if needed.
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
    try:
        if int(key) in _pressed:
            return True
    except Exception:
        pass
    try:
        return pygame.key.get_pressed()[key]
    except Exception:
        return False
