import pygame
from interactable.interactable import Interactable
from core.position import Position
from core.constants import _asset

_sprite: pygame.Surface | None = None


def _load_sprite():
    global _sprite
    if _sprite is not None:
        return
    try:
        _sprite = pygame.image.load(_asset('trash_can.png')).convert_alpha()
    except Exception:
        _sprite = None


class Deletor(Interactable):
    """Poubelle — supprime l'item que le joueur porte."""

    def __init__(self, position: Position, collision_size: int, text: str,
                 activate_key: int = None, player=None):
        super().__init__(position, collision_size=collision_size,
                         text=text, activate_keys=activate_key)
        self.player       = player
        self.activate_key = activate_key
        self._scaled: pygame.Surface | None = None
        self._scaled_size: tuple = (0, 0)

    def delete_item(self) -> bool:
        if self.in_range and self.player.has_item():
            self.player.remove_item()
            return True
        return False

    def draw(self, screen: pygame.Surface):
        _load_sprite()
        rect = self.get_collision_rect()

        if _sprite:
            if self._scaled is None or self._scaled_size != (rect.width, rect.height):
                self._scaled = pygame.transform.smoothscale(_sprite, (rect.width, rect.height))
                self._scaled_size = (rect.width, rect.height)
            screen.blit(self._scaled, rect)
        else:
            pygame.draw.rect(screen, (180, 60, 60), rect, border_radius=6)
            pygame.draw.rect(screen, (100, 20, 20), rect, 2, border_radius=6)

        self.draw_help(screen)

    def handle_keydown(self, key):
        if key == self.activate_key:
            self.delete_item()

    def handle_movement(self):
        pass
