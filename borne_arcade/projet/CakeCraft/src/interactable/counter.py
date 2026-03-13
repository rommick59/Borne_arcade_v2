import pygame
import math
from interactable.interactable import Interactable
from entity.item.cake_item import CakeItem
from core.position import Position
from core.enums import DeliveryResult

_font = None


class Counter(Interactable):
    """Comptoir de livraison — le joueur dépose le gâteau ici pour servir le client."""

    def __init__(self, position: Position, player,
                 collision_w: int = 190, collision_h: int = 40,
                 activate_key: int = pygame.K_f):
        super().__init__(position, collision_size=max(collision_w, collision_h),
                         text="Livrer la commande", activate_keys=activate_key)
        self.player       = player
        self.activate_key = activate_key
        self.on_delivery  = None
        self._coll_w      = collision_w
        self._coll_h      = collision_h

        self._flash_timer   = 0.0
        self._flash_success = True
        self._quality_multiplier = 1.0  # Stocke le multiplicateur de qualité

    def _calculate_cooking_quality(self, cooked_level: float) -> float:
        """
        Calcule le multiplicateur de qualité basé sur la cuisson:
        - 0.0 à 0.9: plus c'est cuit, plus de points (progression linéaire)
        - 0.91 à 1.11: score maximum (100% des points)
        - 1.12 à 2.0: moins de points (dégradation linéaire)
        Retourne un float entre 0 et 1
        """
        if cooked_level == 0:
            return 0
        elif cooked_level <= 0.9:
            # Progression linéaire de 0.1 à 1.0
            # 0.01 -> 0.1x, 0.9 -> 1.0x
            return 0.1 + (cooked_level / 0.9) * 0.9
        elif cooked_level <= 1.11:
            # Zone parfaite : score maximum
            return 1.0
        else:
            # Dégradation de 1.0 à 0.1
            # 1.12 -> 0.98x, 2.0 -> 0.1x
            t = (cooked_level - 1.11) / (2.0 - 1.11)  # 0 à 1
            return 1.0 - t * 0.9  # 1.0 -> 0.1

    def get_quality_multiplier(self) -> float:
        """Retourne le multiplicateur de qualité actuel, arrondi au supérieur"""
        return math.ceil(self._quality_multiplier * 10) / 10  # Arrondi à 0.1 près

    def update(self, dt: float):
        self._flash_timer = max(0.0, self._flash_timer - dt)

    def handle_keydown(self, key):
        if key != self.activate_key or not self.in_range:
            return

        result = self._try_deliver()
        self._flash_timer   = 0.6
        self._flash_success = (result == DeliveryResult.SUCCESS)

        if self.on_delivery:
            self.on_delivery(result)

    def _try_deliver(self) -> DeliveryResult:
        if not self.player.has_item():
            return DeliveryResult.WRONG_ITEM
        if not isinstance(self.player.current_item, CakeItem):
            return DeliveryResult.WRONG_ITEM
        if not self.player.current_item.cooked > 0:
            return DeliveryResult.NOT_COOKED
        
        # Calculer la qualité de cuisson
        cake = self.player.current_item
        self._quality_multiplier = self._calculate_cooking_quality(cake.cooked)
        
        return DeliveryResult.SUCCESS   # zone handles actual serving via callback

    def get_collision_rect(self):
        return pygame.Rect(
            self.position.x - self._coll_w // 2,
            self.position.y - self._coll_h // 2,
            self._coll_w, self._coll_h,
        )

    def draw_help(self, screen: pygame.Surface, color: tuple = (30, 30, 30)):
        if not self.in_range:
            return
        from interactable.interactable import _BTN_SIZE
        btn = self._get_btn_img()
        if btn is None:
            return
        bx = self.position.x - _BTN_SIZE // 2
        by = self.position.y - self._coll_h // 2 - _BTN_SIZE - 4
        screen.blit(btn, (bx, by))

    def handle_movement(self):
        pass

    def draw(self, screen: pygame.Surface):
        rect = self.get_collision_rect()

        if self._flash_timer > 0:
            color = (80, 200, 80) if self._flash_success else (200, 60, 60)
        else:
            color = (210, 170, 90)

        surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surf.fill((*color, 160))
        screen.blit(surf, rect.topleft)
        self.draw_help(screen)
