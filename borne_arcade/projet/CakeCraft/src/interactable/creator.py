import pygame
from interactable.interactable import Interactable
from entity.item.ingredient_item import IngredientItem, _COLORS as _ING_COLORS
from core.position import Position
from core.enums import Ingredient

class Creator(Interactable):
    """Station qui crée un IngredientItem quand le joueur appuie sur F."""

    def __init__(self, position: Position, collision_size: int,
                 ingredient_type: Ingredient, player, activate_key: int = pygame.K_f):
        label = ingredient_type.value
        super().__init__(position, collision_size=collision_size,
                         text=f"Prendre {label}", activate_keys=activate_key)
        self.ingredient_type = ingredient_type
        self.player          = player
        self.activate_key    = activate_key

    def create(self) -> bool:
        if self.in_range and not self.player.has_item():
            item = IngredientItem(Position(self.player.position.x, self.player.position.y),
                                  self.ingredient_type)
            self.player.give_item(item)
            return True
        return False

    def draw(self, screen: pygame.Surface):
        from entity.item.ingredient_item import get_ingredient_sprite
        bg, fg = _ING_COLORS.get(self.ingredient_type, ((200, 200, 200), (0, 0, 0)))
        rect = self.get_collision_rect()
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, fg, rect, 2, border_radius=8)

        sprite = get_ingredient_sprite(self.ingredient_type, rect.width - 8)
        if sprite:
            screen.blit(sprite, sprite.get_rect(center=rect.center))
        else:
            font = pygame.font.Font(None, 18)
            label = font.render(self.ingredient_type.value, True, fg)
            screen.blit(label, label.get_rect(center=rect.center))

        self.draw_help(screen)

    def handle_keydown(self, key):
        if key == self.activate_key:
            self.create()

    def handle_movement(self):
        pass
