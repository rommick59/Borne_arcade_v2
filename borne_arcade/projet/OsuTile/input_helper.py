"""Input helper to track synthetic key state for OsuTile (like Babble_Shot).

Keeps a small set of pressed keys updated from normalized events so
code can query `is_pressed(key)` if needed.
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
