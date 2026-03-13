from entity.entity import Entity
from core.position import Position
from recipe.recipe import Recipe
from core.enums import CustomerState
from core.constants import CUSTOMER_SIZE, CUSTOMER_SPEED, _asset
import pygame

_sprite_happy: pygame.Surface | None = None
_sprite_angry: pygame.Surface | None = None
_sprites_loaded = False


def _load_sprites(size: int):
    global _sprite_happy, _sprite_angry, _sprites_loaded
    if _sprites_loaded:
        return
    _sprites_loaded = True
    try:
        raw = pygame.image.load(_asset('sprites', 'customers', 'customer_happy.png')).convert_alpha()
        _sprite_happy = pygame.transform.smoothscale(raw, (size * 2, size * 2))
    except Exception:
        _sprite_happy = None
    try:
        raw = pygame.image.load(_asset('sprites', 'customers', 'customer_angry.png')).convert_alpha()
        _sprite_angry = pygame.transform.smoothscale(raw, (size * 2, size * 2))
    except Exception:
        _sprite_angry = None


class Customer(Entity):
    def __init__(self, position: Position, wait_position: Position, leave_position: Position, recipe: Recipe):
        super().__init__(position)
        self.wait_position  = wait_position
        self.leave_position = leave_position
        self.recipe         = recipe
        self.state          = CustomerState.WALKING
        self.patience       = recipe.time_limit
        self._failed        = False
        self._not_cooked_received = False
        self._carried_item  = None

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt: float):
        if self.state == CustomerState.WALKING:
            self._walk_toward(self.wait_position, dt)
            if self._reached(self.wait_position):
                self.state = CustomerState.QUEUED

        elif self.state == CustomerState.QUEUED:
            if not self._reached(self.wait_position):
                self._walk_toward(self.wait_position, dt)

        elif self.state == CustomerState.WAITING:
            self.patience -= dt
            if self.patience <= 0:
                self._failed = True
                self.state   = CustomerState.LEAVING

        elif self.state in (CustomerState.SERVED, CustomerState.LEAVING):
            self._walk_toward(self.leave_position, dt)

        if self._carried_item:
            self._carried_item.position = Position(self.position.x, self.position.y)

    def serve(self):
        self.state   = CustomerState.SERVED
        self._failed = False

    def receive_not_cooked(self):
        self._not_cooked_received = True

    def receive_item(self, item):
        self._carried_item = item
        item.position = Position(self.position.x, self.position.y)

    @property
    def patience_ratio(self) -> float:
        return max(0.0, self.patience / self.recipe.time_limit)

    @property
    def is_waiting(self) -> bool:
        return self.state == CustomerState.WAITING

    @property
    def is_done(self) -> bool:
        return self.state in (CustomerState.SERVED, CustomerState.LEAVING) and self._reached(self.leave_position)

    def _is_angry(self) -> bool:
        if self.state == CustomerState.SERVED:
            return False
        if self._failed or self._not_cooked_received:
            return True
        if self.state == CustomerState.WAITING and self.patience_ratio <= 0.5:
            return True
        return False

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, screen: pygame.Surface):
        _load_sprites(CUSTOMER_SIZE)
        x, y = int(self.position.x), int(self.position.y)

        sprite = (_sprite_angry if self._is_angry() else _sprite_happy)
        if sprite:
            screen.blit(sprite, sprite.get_rect(center=(x, y)))
        else:
            from core.constants import CUSTOMER_COLOR, CUSTOMER_ANGRY_COLOR
            color = CUSTOMER_ANGRY_COLOR if self._is_angry() else CUSTOMER_COLOR
            pygame.draw.circle(screen, color, (x, y), CUSTOMER_SIZE)

        if self._carried_item:
            from core.constants import ITEM_SIZE
            item_y = y - CUSTOMER_SIZE - ITEM_SIZE // 2 - 5
            self._carried_item._render(screen, x, item_y)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _walk_toward(self, target: Position, dt: float):
        dx   = target.x - self.position.x
        dy   = target.y - self.position.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        step = CUSTOMER_SPEED * dt
        if dist <= step:
            self.position.x = target.x
            self.position.y = target.y
        else:
            factor           = step / dist
            self.position.x += dx * factor
            self.position.y += dy * factor

    def _reached(self, target: Position) -> bool:
        dx = target.x - self.position.x
        dy = target.y - self.position.y
        return (dx ** 2 + dy ** 2) ** 0.5 < 1
