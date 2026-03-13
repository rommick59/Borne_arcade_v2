import pygame
from game.player_zone import PlayerZone
from core.enums import Side, Ingredient
from core.constants import PLAYER_SPEED, PLAYER_1_INTERACT, PLAYER_2_INTERACT
from entity.item.ingredient_item import IngredientItem
from entity.item.cake_item import CakeItem


_REACH = 6  # pixels tolerance to consider "arrived"


def _remaining_needed(recipe, workbench) -> list:
    """Return ingredients still needed, respecting duplicates."""
    if not recipe:
        return []
    deposited = list(workbench.get_deposited()) if workbench else []
    remaining = list(recipe.ingredients)
    for ing in deposited:
        if ing in remaining:
            remaining.remove(ing)
    return remaining


class BotZone(PlayerZone):
    """PlayerZone where the player is controlled by a simple bot."""

    def __init__(self, screen: pygame.Surface, side: Side):
        super().__init__(screen, side)
        self._bot_target   = None  # current interactable the bot is walking toward
        self._bot_cooldown = 0.0   # small delay between actions to feel less instant

    # ── Bot logic ─────────────────────────────────────────────────────────────

    def _hoven(self):
        return next((i for i in self.interactables if i.__class__.__name__ == "Hoven"), None)

    def _deletor(self):
        return next((i for i in self.interactables if i.__class__.__name__ == "Deletor"), None)

    def _bot_tick(self, dt: float):
        if self._bot_cooldown > 0:
            self._bot_cooldown -= dt
            return

        recipe  = self.workbench.current_recipe if self.workbench else None
        hoven   = self._hoven()
        deletor = self._deletor()
        waiting = self.get_waiting_customer()

        # ── Cleanup mode: no customer waiting — discard everything ────────────
        if not waiting:
            # Cake in oven → retrieve it first
            oven_has_cake = hoven and hoven.held_item and isinstance(hoven.held_item, CakeItem)
            if oven_has_cake and not self.player.has_item():
                self._bot_walk_to(hoven, dt)
                if self._bot_in_range(hoven):
                    self._bot_press_f()
                return

            # Carrying anything → trash it
            if self.player.has_item() and deletor:
                self._bot_walk_to(deletor, dt)
                if self._bot_in_range(deletor):
                    self._bot_press_f()
                return

            # Ingredients on workbench → pull them out one by one and trash
            if self.workbench and (self.workbench._deposited or self.workbench._output_item) and not self.player.has_item():
                self._bot_walk_to(self.workbench, dt)
                if self._bot_in_range(self.workbench):
                    self._bot_press_f()
                return

            return  # nothing to do

        # ── Normal mode: customer is waiting ─────────────────────────────────

        time_is_urgent  = waiting.patience <= 3.0
        oven_has_cake   = hoven and hoven.held_item and isinstance(hoven.held_item, CakeItem)

        # 1. Oven has a cooked cake ready — go retrieve it
        #    Also retrieve early if customer is about to leave (< 3s left)
        if oven_has_cake and not self.player.has_item() and (hoven.held_item.cooked >= 1.0 or time_is_urgent):
            self._bot_walk_to(hoven, dt)
            if self._bot_in_range(hoven):
                self._bot_press_f()
            return

        # 2. Carrying a cooked cake — deliver it (don't press F while still in oven range)
        if self.player.has_item() and isinstance(self.player.current_item, CakeItem) and self.player.current_item.cooked >= 1.0:
            self._bot_walk_to(self.counter, dt)
            if self._bot_in_range(self.counter) and not self._bot_in_range(hoven):
                self._bot_press_f()
            return

        # 3. Carrying an uncooked cake — put it in the oven (only if oven is free)
        #    If time is urgent, deliver directly instead of putting in oven
        if self.player.has_item() and isinstance(self.player.current_item, CakeItem) and self.player.current_item.cooked < 1.0:
            if time_is_urgent:
                self._bot_walk_to(self.counter, dt)
                if self._bot_in_range(self.counter) and not self._bot_in_range(hoven):
                    self._bot_press_f()
            elif hoven and not hoven.held_item:
                self._bot_walk_to(hoven, dt)
                if self._bot_in_range(hoven):
                    self._bot_press_f()
            return

        # 4. Workbench assembled an uncooked cake — pick it up (if oven is free)
        if self.workbench and self.workbench._output_item and not self.player.has_item():
            if hoven and not hoven.held_item:
                self._bot_walk_to(self.workbench, dt)
                if self._bot_in_range(self.workbench):
                    self._bot_press_f()
            return

        # 5. Carrying a wrong/unneeded ingredient — trash it
        if self.player.has_item() and isinstance(self.player.current_item, IngredientItem):
            needed = _remaining_needed(recipe, self.workbench)
            held   = self.player.current_item.ingredient_type
            if held in needed:
                self._bot_walk_to(self.workbench, dt)
                if self._bot_in_range(self.workbench):
                    self._bot_press_f()
            else:
                if deletor:
                    self._bot_walk_to(deletor, dt)
                    if self._bot_in_range(deletor):
                        self._bot_press_f()
            return

        # 6. Go pick the next needed ingredient — only if oven is free or empty
        oven_busy = hoven and hoven.held_item is not None
        if recipe and not self.player.has_item() and not (self.workbench and self.workbench._output_item) and not oven_busy:
            needed = _remaining_needed(recipe, self.workbench)
            if needed:
                creator = next((c for c in self._creators if c.ingredient_type == needed[0]), None)
                if creator:
                    self._bot_walk_to(creator, dt)
                    if self._bot_in_range(creator):
                        self._bot_press_f()

    def _bot_walk_to(self, interactable, dt: float = 1 / 60):
        self._bot_target = interactable
        rect = interactable.get_collision_rect()
        tx   = rect.centerx
        ty   = rect.bottom
        px   = self.player.position.x
        py   = self.player.position.y + self.player.collision_h // 2
        dx   = tx - px
        dy   = ty - py
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist > _REACH:
            step = PLAYER_SPEED * dt
            self.player.move(
                dx / dist * step,
                dy / dist * step,
            )

    def _bot_in_range(self, interactable) -> bool:
        return self.player.get_collision_rect().colliderect(
            interactable.get_collision_rect()
        )

    def _bot_press_f(self):
        interact_key = PLAYER_2_INTERACT if self.side == Side.RIGHT else PLAYER_1_INTERACT
        target = self._bot_target
        if target and hasattr(target, "handle_keydown") and self._bot_in_range(target):
            prev = target.in_range
            target.in_range = True
            target.handle_keydown(interact_key)
            target.in_range = prev
        self._bot_cooldown = 0.15

    # ── Override — ignore human input, run bot instead ────────────────────────

    def handle_movement(self, keys, dt: float = 1 / 60):
        pass

    def handle_events(self):
        # Still need to update in_range for interactables
        self.player.handle_events()

    def handle_keydown(self, key):
        pass

    def update(self, dt: float):
        super().update(dt)
        self._bot_tick(dt)
