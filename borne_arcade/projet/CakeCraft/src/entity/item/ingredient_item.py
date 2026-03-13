import pygame
from entity.item.item import Item
from core.position import Position
from core.enums import Ingredient
from core.constants import _asset

# (background, text) colors per ingredient
_COLORS = {
    Ingredient.FLOUR:      ((248, 242, 228), (112, 86,  52)),
    Ingredient.EGG:        ((255, 222, 85),  (112, 78,  0)),
    Ingredient.BUTTER:     ((255, 200, 8),   (112, 78,  0)),
    Ingredient.SUGAR:      ((255, 182, 202), (152, 48,  85)),
    Ingredient.CREAM:      ((244, 226, 212), (105, 76,  50)),
    Ingredient.CHOCOLATE:  ((88,  42,  12),  (255, 225, 192)),
    Ingredient.STRAWBERRY: ((222, 56,  76),  (255, 236, 240)),
    Ingredient.VANILLA:    ((198, 178, 228), (78,  50,  110)),
}

_SPRITE_FILES = {
    Ingredient.FLOUR:      'flour.png',
    Ingredient.EGG:        'egg.png',
    Ingredient.BUTTER:     'butter.png',
    Ingredient.SUGAR:      'sugar.png',
    Ingredient.CREAM:      'cream.png',
    Ingredient.CHOCOLATE:  'chocolate.png',
    Ingredient.STRAWBERRY: 'strawberrie.png',
    Ingredient.VANILLA:    'vanille.png',
}

_sprite_cache: dict[Ingredient, pygame.Surface | None] = {}


def get_ingredient_sprite(ingredient: Ingredient, size: int) -> pygame.Surface | None:
    key = (ingredient, size)
    if key not in _sprite_cache:
        fname = _SPRITE_FILES.get(ingredient)
        try:
            surf = pygame.image.load(_asset('sprites', 'ingredients', fname)).convert_alpha()
            surf = pygame.transform.smoothscale(surf, (size, size))
        except Exception:
            surf = None
        _sprite_cache[key] = surf
    return _sprite_cache[key]


class IngredientItem(Item):
    def __init__(self, position: Position, ingredient_type: Ingredient):
        bg, _ = _COLORS.get(ingredient_type, ((200, 200, 200), (0, 0, 0)))
        super().__init__(position, name=ingredient_type.value, size=30, color=bg)
        self.ingredient_type = ingredient_type

    def _render(self, screen: pygame.Surface, cx: int, cy: int):
        sprite = get_ingredient_sprite(self.ingredient_type, self.size)
        if sprite:
            screen.blit(sprite, sprite.get_rect(center=(cx, cy)))
        else:
            bg, fg = _COLORS.get(self.ingredient_type, ((200, 200, 200), (0, 0, 0)))
            rect = pygame.Rect(cx - self.size // 2, cy - self.size // 2, self.size, self.size)
            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, fg, rect, 2, border_radius=6)
