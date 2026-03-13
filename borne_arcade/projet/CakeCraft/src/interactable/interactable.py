from core.position import Position
import pygame

_BTN_SIZE = 32


class Interactable:
    def __init__(self, position: Position, collision_size: int = 50,
                 text: str = "", activate_keys=None):
        self.position       = position
        self.collision_size = collision_size
        self.in_range       = False
        self.text           = text
        self.activate_keys  = activate_keys
        self._btn_img       = None
        self._btn_loaded    = False

    def get_collision_rect(self):
        half = self.collision_size // 2
        return pygame.Rect(
            self.position.x - half,
            self.position.y - half,
            self.collision_size,
            self.collision_size,
        )

    def draw_collision_zone(self, screen: pygame.Surface, color: tuple = (0, 255, 0), alpha: int = 50):
        surf = pygame.Surface((self.collision_size, self.collision_size))
        surf.set_alpha(alpha)
        surf.fill(color)
        screen.blit(surf, (self.position.x - self.collision_size // 2,
                           self.position.y - self.collision_size // 2))

    def _get_btn_img(self) -> pygame.Surface | None:
        if not self._btn_loaded:
            self._btn_loaded = True
            if self.activate_keys is not None:
                from hud.buttons import get_button_image
                self._btn_img = get_button_image(self.activate_keys)
        return self._btn_img

    def draw_help(self, screen: pygame.Surface, color: tuple = (30, 30, 30)):
        if not self.in_range:
            return
        btn = self._get_btn_img()
        if btn is None:
            return
        bx = self.position.x - _BTN_SIZE // 2
        by = self.position.y - self.collision_size // 2 - _BTN_SIZE - 4
        screen.blit(btn, (bx, by))
