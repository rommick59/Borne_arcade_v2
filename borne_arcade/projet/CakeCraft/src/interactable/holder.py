import pygame
from interactable.interactable import Interactable
from core.position import Position

class Holder(Interactable):
    """Station de stockage temporaire — le joueur peut y déposer et reprendre un item."""

    def __init__(self, position: Position, collision_size: int, text: str,
                 activate_key: int = None, player=None):
        super().__init__(position, collision_size=collision_size,
                         text=text, activate_keys=activate_key)
        self.player       = player
        self.activate_key = activate_key
        self.held_item    = None

    def hold_item(self) -> bool:
        if self.in_range and self.player.has_item():
            self.held_item = self.player.remove_item()
            self.held_item.position = Position(self.position.x, self.position.y)
            return True
        return False

    def retrieve_item(self) -> bool:
        if self.in_range and self.held_item and not self.player.has_item():
            self.player.give_item(self.held_item)
            self.held_item = None
            return True
        return False

    def draw(self, screen: pygame.Surface):
        color = (140, 100, 60) if self.held_item else (180, 150, 110)
        rect  = self.get_collision_rect()
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, (80, 50, 20), rect, 2, border_radius=6)

        font  = pygame.font.Font(None, 18)
        label = font.render("Stockage", True, (255, 240, 220))
        screen.blit(label, label.get_rect(center=rect.center))

        if self.held_item:
            self.held_item._render(screen, int(self.position.x), int(self.position.y) - self.collision_size // 2 - 18)

        self.draw_help(screen)

    def handle_keydown(self, key):
        if key == self.activate_key:
            if self.held_item:
                self.retrieve_item()
            else:
                self.hold_item()

    def handle_movement(self):
        pass
