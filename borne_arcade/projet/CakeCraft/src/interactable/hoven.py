import pygame
from interactable.holder import Holder
from entity.item.cake_item import CakeItem
from core.position import Position
from core.enums import CakeType
from core.constants import _asset
from hud.bubble import ProgressBubble

_sprite_idle = None

def _load_sprites():
    global _sprite_idle
    if _sprite_idle is not None:
        return
    try:
        _sprite_idle = pygame.image.load(_asset('sprites', 'furnitures', 'furnace', 'f_idle.png')).convert_alpha()
    except Exception:
        _sprite_idle = None

_SPIN_SPEED = 120  # degrees per second

class Hoven(Holder):
    """Four — hérite du Holder et ajoute la cuisson des CakeItem"""

    def __init__(self, position: Position, collision_size: int, text: str,
                 activate_key: int = None, player=None):
        super().__init__(position, collision_size, text, activate_key, player)
        self.cooking_speed = 0.1  # units/s — 1.0 = fully cooked (base: 10s)
        self.score_ref     = None  # set to a callable returning the player's score
        self.is_cooking    = False
        self.cooking_progress = 0.0
        self.burned_recently = False
        self.burned_timer    = 0.0
        self._spin_angle     = 0.0
        self._scaled_sprite: pygame.Surface | None = None
        self._scaled_size: tuple = (0, 0)
        
        # Créer la bulle de progression pour la cuisson
        bubble_width = collision_size
        bubble_height = 10
        bubble_x = position.x - collision_size // 2  # Centrer horizontalement avec le four
        bubble_y = position.y + collision_size // 2  # Juste en dessous du four
        self.progress_bubble = ProgressBubble(bubble_x, bubble_y, bubble_width, bubble_height, padding=3)

    def hold_item(self) -> bool:
        """Override pour commencer la cuisson si c'est un CakeItem"""
        if self.in_range and self.player.has_item():
            item = self.player.current_item
            
            # Vérifier si c'est un CakeItem
            if isinstance(item, CakeItem):
                self.held_item = self.player.remove_item()
                self.held_item.position = Position(self.position.x, self.position.y)
                self.is_cooking = True
                self.cooking_progress = self.held_item.cooked
                return True
            else:
                # Pour les autres items, comportement normal du Holder
                return super().hold_item()
        return False

    def update(self, dt: float):
        # Recalculate cooking speed from score: +0.01/s per 100pts, capped at 0.25/s (4s min)
        if self.score_ref is not None:
            bonus = (self.score_ref() // 100) * 0.01
            self.cooking_speed = min(0.25, 0.1 + bonus)

        if self.is_cooking:
            self._spin_angle = (self._spin_angle + _SPIN_SPEED * dt) % 360

        if self.is_cooking and self.held_item and isinstance(self.held_item, CakeItem):
            self.held_item.cooked += self.cooking_speed * dt
            
            # Supprimer le gâteau s'il atteint 200% (brûlé)
            if self.held_item.cooked >= 2.0:
                self.held_item = None  # Gâteau brûlé, supprimé
                self.is_cooking = False  # Plus de cuisson
                self.burned_recently = True  # Indicateur visuel
                self.burned_timer = 2.0  # Afficher pendant 2 secondes
        
        # Gérer le timer de l'indicateur de brûlé
        if self.burned_recently:
            self.burned_timer -= dt
            if self.burned_timer <= 0:
                self.burned_recently = False

    def draw(self, screen: pygame.Surface):
        """Override pour afficher le four et la progression de cuisson"""
        _load_sprites()
        rect = self.get_collision_rect()

        if _sprite_idle:
            # Re-scale only when size changes (typically never after first draw)
            if self._scaled_sprite is None or self._scaled_size != (rect.width, rect.height):
                self._scaled_sprite = pygame.transform.smoothscale(_sprite_idle, (rect.width, rect.height))
                self._scaled_size = (rect.width, rect.height)
            if self.is_cooking:
                rotated = pygame.transform.rotate(self._scaled_sprite, -self._spin_angle)
                screen.blit(rotated, rotated.get_rect(center=rect.center))
            else:
                screen.blit(self._scaled_sprite, rect)
        else:
            color = (180, 80, 20) if self.is_cooking else (140, 100, 60)
            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, (80, 50, 20), rect, 2, border_radius=6)

        # Cake au centre du four avec effet blanc→couleur→noir
        if self.is_cooking and self.held_item and isinstance(self.held_item, CakeItem):
            cake_size = rect.width // 2
            self.held_item.render_in_oven(screen, rect.centerx, rect.centery, cake_size)

        # Bulle de progression si en cours de cuisson
        if self.is_cooking and self.held_item and isinstance(self.held_item, CakeItem):
            self.progress_bubble.draw(screen)
            self.progress_bubble.draw_progress_bar(screen, self.held_item.cooked)


        self.draw_help(screen)

    def handle_keydown(self, key):
        """Override pour gérer la cuisson"""
        if key == self.activate_key:
            if self.held_item:
                # Si c'est un CakeItem cuit, on peut le récupérer
                if isinstance(self.held_item, CakeItem) and not self.is_cooking:
                    self.retrieve_item()
                else:
                    # Sinon comportement normal
                    self.retrieve_item()
            else:
                self.hold_item()

    def retrieve_item(self) -> bool:
        """Override pour arrêter la cuisson quand on récupère l'item"""
        if self.in_range and self.held_item and not self.player.has_item():
            self.player.give_item(self.held_item)
            self.held_item = None
            self.is_cooking = False
            self.cooking_progress = 0.0
            return True
        return False