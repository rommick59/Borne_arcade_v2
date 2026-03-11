"""Normalize pygame events for PianoTile.

Converts event.unicode characters to pygame key codes when possible and
updates `input_helper` so `is_pressed()` reflects real-time state.
"""
import pygame
from .input_helper import on_keydown, on_keyup

def get_events():
    events = pygame.event.get()
    for event in events:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            uni = getattr(event, 'unicode', '')
            mapped = event.key
            # Mapping from characters produced by the arcade hardware / AZERTY
            # layout to the logical pygame keys used by the game.
            char_map = {
                'é': 'r',   # key physically sends 'é' -> treat as 'r'
                '"': 't',  # double quote -> 't'
                "'": 'y',  # single quote -> 'y'
                '(': 'f',   # '(' -> 'f'
                '-': 'g',   # '-' -> 'g'
                # add more mappings here if needed (e.g. 'è': 'h')
            }

            if uni:
                try:
                    # Prefer explicit char_map translation when present
                    if uni in char_map:
                        mapped = pygame.key.key_code(char_map[uni])
                    else:
                        mapped = pygame.key.key_code(uni)
                    # Modify the event in-place so downstream code sees the mapped key
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
