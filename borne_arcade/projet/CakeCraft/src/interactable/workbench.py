import pygame
from interactable.interactable import Interactable
from entity.item.ingredient_item import IngredientItem, _COLORS as _ING_COLORS
from entity.item.cake_item import CakeItem
from core.position import Position
from core.enums import Ingredient
from core.constants import _asset

_font_label = None
_font_small = None

# Load workbench sprite
_workbench_sprite = None

def _load_workbench_sprite():
    global _workbench_sprite
    if _workbench_sprite is None:
        try:
            _workbench_sprite = pygame.image.load(_asset('sprites', 'furnitures', 'workbench', 'w_default.png')).convert_alpha()
        except Exception:
            _workbench_sprite = None


class Workbench(Interactable):
    """Plan de travail — le joueur y dépose ses ingrédients un par un.
    Quand la recette est complète, un CakeItem est créé et peut être récupéré."""

    def __init__(self, position: Position, collision_size: int, player,
                 activate_key: int = pygame.K_f):
        super().__init__(position, collision_size=collision_size,
                         text="Déposer / Récupérer", activate_keys=activate_key)
        self.player          = player
        self.activate_key    = activate_key
        self.current_recipe  = None     # set by PlayerZone each frame
        self._deposited      = []       # list of Ingredient deposited so far
        self._deposited_items = []       # list of IngredientItem objects (for recovery)
        self._output_item    = None     # CakeItem ready to pick up
        self._ingredient_positions = []  # Store random positions for each ingredient

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self):
        """Vider le plan de travail (nouveau client ou mauvaise livraison)."""
        self._deposited   = []
        self._deposited_items = []
        self._ingredient_positions = []  # Reset positions too
        self._output_item = None

    def get_deposited(self) -> list:
        return list(self._deposited)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def handle_keydown(self, key):
        if key != self.activate_key or not self.in_range:
            return

        # Priority 1: player picks up finished cake OR pick up last ingredient put on the table
        if self._output_item is not None and not self.player.has_item():
            self.player.give_item(self._output_item)
            self._output_item = None
            return
        elif self._output_item is None and self._deposited_items and not self.player.has_item():
            item = self._deposited_items.pop()
            # Also remove the corresponding ingredient from _deposited list
            self._deposited.pop()
            self.player.give_item(item)
            return  # Important: stop here to avoid re-depositing

        # Priority 2: player deposits an ingredient
        if self.player.has_item() and isinstance(self.player.current_item, IngredientItem):
            ingr_item = self.player.current_item
            ingr = ingr_item.ingredient_type
            self.player.remove_item()
            self._deposited.append(ingr)
            self._deposited_items.append(ingr_item)  # Store the actual item for recovery
            
            # Generate and store random position for this ingredient
            import random
            center_x = self.position.x
            center_y = self.position.y - (self.collision_size // 2) + 15   # Move center up
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(4, 7)
            pos_x = center_x + int(distance * (angle / 3.14159))
            pos_y = center_y + int(distance * (angle / 2))
            self._ingredient_positions.append((pos_x, pos_y))
            
            # Check if the recipe is complete
            if self.current_recipe and self._is_complete():
                self._assemble_cake()

    def _is_complete(self) -> bool:
        needed = sorted(i.name for i in self.current_recipe.ingredients)
        have   = sorted(i.name for i in self._deposited)
        return have == needed

    def _assemble_cake(self):
        # Use the same center position as ingredients
        center_x = self.position.x
        center_y = self.position.y - (self.collision_size // 2) + 15
        self._output_item = CakeItem(
            Position(center_x, center_y),
            self.current_recipe.cake_type,
        )
        self._deposited = []
        self._deposited_items = []  # Clear deposited items when cake is assembled
        self._ingredient_positions = []  # Clear positions too

    def handle_movement(self):
        pass

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, screen: pygame.Surface):
        global _font_label, _font_small
        if _font_label is None:
            _font_label = pygame.font.Font(None, 18)
            _font_small = pygame.font.Font(None, 14)

        _load_workbench_sprite()
        rect = self.get_collision_rect()

        # Draw workbench sprite if available, otherwise fallback to rectangle
        if _workbench_sprite:
            # Scale sprite to fit collision rect
            scaled_sprite = pygame.transform.scale(_workbench_sprite, (rect.width, rect.height))
            screen.blit(scaled_sprite, rect)
        else:
            # Fallback to original rectangle drawing
            bg_color = (140, 85, 30) if self._output_item else (180, 120, 60)
            pygame.draw.rect(screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(screen, (80, 45, 10), rect, 2, border_radius=8)

        # Deposited ingredients as small colored dots - fixed random positions
        dot_r = 5
        
        for i, (ingr, (pos_x, pos_y)) in enumerate(zip(self._deposited, self._ingredient_positions)):
            bg, _ = _ING_COLORS.get(ingr, ((200, 200, 200), (0, 0, 0)))
            pygame.draw.circle(screen, bg, (pos_x, pos_y), dot_r)
            pygame.draw.circle(screen, (60, 30, 0), (pos_x, pos_y), dot_r, 1)

        # Output cake ready indicator
        if self._output_item:
            ready_label = _font_label.render("Gâteau prêt !", True, (255, 255, 100))
            screen.blit(ready_label, ready_label.get_rect(centerx=rect.centerx, bottom=rect.bottom - 4))
            self._output_item._render(screen, int(self._output_item.position.x), int(self._output_item.position.y))

        self.draw_help(screen)
