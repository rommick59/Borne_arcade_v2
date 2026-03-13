from interactable.interactable import Interactable
from entity.entity import Entity
from core.position import Position
import pygame
from core.constants import PLAYER_SIZE, PLAYER_SPRITE_PATH, PLAYER_SPRITE_SCALE, PLAYER_ANIM_FPS, PLAYER_SPEED, PLAYER_COLLISION_H


# Sprite sheet row indices (RPG Maker VX format)
_DIR_DOWN  = 0
_DIR_LEFT  = 1
_DIR_RIGHT = 2
_DIR_UP    = 3

_COLS = 3
_ROWS = 4

_SHEET_W = 64
_SHEET_H = 128
_frame_w  = _SHEET_W // _COLS
_frame_h  = _SHEET_H // _ROWS
SPRITE_W = max(1, int(_frame_w * PLAYER_SPRITE_SCALE / _frame_h) - 2)
SPRITE_H = PLAYER_SPRITE_SCALE

_frames = []


def _load_sprites():
    global _frames
    if _frames:
        return
    try:
        sheet   = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()
        sw, sh  = sheet.get_width(), sheet.get_height()
        frame_w = sw // _COLS
        frame_h = sh // _ROWS
        scale   = PLAYER_SPRITE_SCALE
        new_w   = int(frame_w * scale / frame_h)

        _frames = []
        for row in range(_ROWS):
            row_frames = []
            for col in range(_COLS):
                raw     = sheet.subsurface(col * frame_w, row * frame_h, frame_w, frame_h)
                full    = pygame.transform.scale(raw, (new_w, scale))
                trimmed = full.subsurface(0, 0, max(1, new_w - 2), scale).copy()
                row_frames.append(trimmed)
            _frames.append(row_frames)
    except Exception:
        _frames = []


class Player(Entity):
    def __init__(self, position: Position, size: int = PLAYER_SIZE,
                 color: tuple = (255, 0, 0), boundary: pygame.Rect = None,
                 controls: dict = None):
        super().__init__(position)
        self.size       = size
        self.color      = color
        self.boundary   = boundary
        self.controls   = controls
        self.collision_w = SPRITE_W
        self.collision_h = SPRITE_H
        self.available_interactables = []
        self.current_item = None

        self._direction  = _DIR_DOWN
        self._frame_idx  = 1
        self._anim_timer = 0.0
        self._is_moving  = False

    def move(self, dx: int, dy: int):
        if self.boundary:
            new_x = self.position.x + dx
            new_y = self.position.y + dy

            half_w = self.collision_w // 2
            half_h = self.collision_h // 2
            new_x = max(self.boundary.left + half_w, min(new_x, self.boundary.right  - half_w))
            new_y = max(self.boundary.top  + half_h, min(new_y, self.boundary.bottom - half_h))

            final_dx = new_x - self.position.x
            final_dy = new_y - self.position.y

            if final_dx != 0 or final_dy != 0:
                super().move(final_dx, final_dy)

            if dy < 0:
                self._direction = _DIR_UP
            elif dy > 0:
                self._direction = _DIR_DOWN
            elif dx < 0:
                self._direction = _DIR_LEFT
            elif dx > 0:
                self._direction = _DIR_RIGHT

            self._is_moving = True
        else:
            super().move(dx, dy)

    def update(self, dt: float):
        if self._is_moving:
            self._anim_timer += dt
            if self._anim_timer >= 1.0 / PLAYER_ANIM_FPS:
                self._anim_timer = 0.0
                self._frame_idx  = (self._frame_idx + 1) % _COLS
        else:
            self._frame_idx  = 1
            self._anim_timer = 0.0

        self._is_moving = False

    def draw(self, screen: pygame.Surface):
        _load_sprites()

        if _frames:
            frame = _frames[self._direction][self._frame_idx]
            x = int(self.position.x) - frame.get_width()  // 2
            y = int(self.position.y) - frame.get_height() // 2
            screen.blit(frame, (x, y))
        else:
            pygame.draw.rect(screen, self.color,
                             (self.position.x - self.size // 2,
                              self.position.y - self.size // 2,
                              self.size, self.size))

        # Draw carried item above the player's head
        if self.current_item:
            carry_cx = int(self.position.x)
            carry_cy = int(self.position.y) - SPRITE_H // 2 - self.current_item.size // 2 - 4
            self.current_item._render(screen, carry_cx, carry_cy)

    def handle_events(self):
        interactable_in_range = self.check_collision_with_interactables()
        for interactable in self.available_interactables:
            interactable.in_range = (interactable == interactable_in_range)

    def handle_movement(self, keys, dt: float = 1 / 60):
        speed = PLAYER_SPEED * dt
        if keys[self.controls["left"]]:
            self.move(-speed, 0)
        if keys[self.controls["right"]]:
            self.move(speed, 0)
        if keys[self.controls["up"]]:
            self.move(0, -speed)
        if keys[self.controls["down"]]:
            self.move(0, speed)

    def get_collision_rect(self):
        # Small hitbox at feet level (bottom of sprite)
        feet_y = self.position.y + self.collision_h // 2 - PLAYER_COLLISION_H
        return pygame.Rect(
            self.position.x - self.collision_w // 2,
            feet_y,
            self.collision_w,
            PLAYER_COLLISION_H,
        )

    def check_collision_with_interactables(self):
        player_rect = self.get_collision_rect()
        for interactable in self.available_interactables:
            if player_rect.colliderect(interactable.get_collision_rect()):
                return interactable
        return None

    def give_item(self, item):
        if item and self.current_item is None:
            self.current_item = item
            # Give item its own Position (not shared reference)
            item.position = Position(self.position.x, self.position.y)
            return True
        return False

    def remove_item(self):
        if self.current_item:
            item = self.current_item
            self.current_item = None
            return item
        return None

    def has_item(self):
        return self.current_item is not None
