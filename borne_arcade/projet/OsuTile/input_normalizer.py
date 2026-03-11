"""Normalize pygame events for OsuTile.

Converts event.unicode characters to pygame key codes when possible and
updates `input_helper` so `is_pressed()` reflects event state. Also
contains common char -> logical key mappings for AZERTY/arcade quirks.
"""
import pygame
from input_helper import on_keydown, on_keyup

CHAR_MAP = {
    'é': 'r',   # common AZERTY mappings from arcade keypad
    '"': 't',
    "'": 'y',
    '(': 'f',
    '-': 'g',
    # add more mappings if needed
}

def get_events():
    events = pygame.event.get()
    for event in events:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            uni = getattr(event, 'unicode', '')
            mapped = event.key
            if uni:
                try:
                    if uni in CHAR_MAP:
                        mapped = pygame.key.key_code(CHAR_MAP[uni])
                    else:
                        mapped = pygame.key.key_code(uni)
                    event.key = mapped
                except Exception:
                    mapped = event.key
            try:
                if event.type == pygame.KEYDOWN:
                    on_keydown(mapped)
                else:
                    on_keyup(mapped)
            except Exception:
                pass
    return events
