from entity.entity import Entity
from core.position import Position
import pygame

class Item(Entity):
    def __init__(self, position: Position, name: str, size: int = 20, color: tuple = (255, 0, 0)):
        super().__init__(position)
        self.size  = size
        self.color = color
        self.name  = name

    def draw(self, screen: pygame.Surface):
        self._render(screen, int(self.position.x), int(self.position.y))

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        """Draw the item centered at (cx, cy). Override in subclasses."""
        pygame.draw.rect(screen, self.color,
                         (cx - self.size // 2, cy - self.size // 2, self.size, self.size),
                         border_radius=4)
