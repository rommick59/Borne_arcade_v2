import math

import pygame

from constants import BULLET_EDGE, BULLET_MAIN, ENEMY_BAT, ENEMY_OUTLINE, ENEMY_SLIME, PLAYER_ACCENT
from constants import PLAYER_HAT, PLATFORM_HEIGHT
from helpers import clamp, lighten


class Player:
    _sprite_cache = {}

    def __init__(self, x, y, width, height):
        self.x = float(x)
        self.y = float(y)
        self.width = int(width)
        self.height = int(height)
        self.vy = 0.0
        self.facing = 1

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def move_horizontal(self, direction, speed, dt_factor):
        self.x += direction * speed * dt_factor
        if direction > 0:
            self.facing = 1
        elif direction < 0:
            self.facing = -1

    def wrap_horizontally(self, screen_width):
        if self.x + self.width < 0:
            self.x = float(screen_width)
        elif self.x > screen_width:
            self.x = -float(self.width)

    def shift_y(self, delta):
        self.y += delta

    def draw(self, screen, body_color, outline_color):
        x = int(self.x)
        y = int(self.y)
        sprite = self._sprite_cache.get(self.facing)
        if sprite is None:
            sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            facing = self.facing
            body = pygame.Rect(7, 17, self.width - 14, self.height - 18)
            pygame.draw.ellipse(sprite, body_color, body)
            pygame.draw.ellipse(sprite, outline_color, body, 2)

            highlight = pygame.Rect(body.x + 8, body.y + 6, body.w // 2, body.h // 3)
            pygame.draw.ellipse(sprite, lighten(body_color, 40), highlight)

            hat = pygame.Rect(8, 7, self.width - 16, 14)
            brim = pygame.Rect(4, 15, self.width - 8, 8)
            pygame.draw.rect(sprite, PLAYER_HAT, hat, border_radius=7)
            pygame.draw.rect(sprite, lighten(PLAYER_HAT, 48), hat, 2, border_radius=7)
            pygame.draw.rect(sprite, lighten(PLAYER_HAT, -22), brim, border_radius=4)

            backpack_x = 3 if facing > 0 else self.width - 21
            backpack = pygame.Rect(backpack_x, 23, 18, 22)
            pygame.draw.rect(sprite, lighten(PLAYER_ACCENT, -30), backpack, border_radius=6)
            pygame.draw.rect(sprite, PLAYER_ACCENT, backpack.inflate(-4, -4), border_radius=5)

            scarf_y = 28
            tail_dir = -facing
            knot = (self.width // 2 + 1, scarf_y)
            pygame.draw.circle(sprite, PLAYER_ACCENT, knot, 7)
            tail = [
                (self.width // 2 + 5, scarf_y + 2),
                (self.width // 2 + 5 + tail_dir * 18, scarf_y + 8),
                (self.width // 2 + 3 + tail_dir * 16, scarf_y + 17),
                (self.width // 2 - 3, scarf_y + 8),
            ]
            pygame.draw.polygon(sprite, PLAYER_ACCENT, tail)

            eye_offset = 4 if facing > 0 else -4
            eye_left = (self.width // 2 - 11, 34)
            eye_right = (self.width // 2 + 11, 34)
            for eye in (eye_left, eye_right):
                pygame.draw.circle(sprite, (255, 255, 255), eye, 7)
                pygame.draw.circle(sprite, outline_color, eye, 7, 2)
                pupil = (eye[0] + eye_offset // 2, eye[1] + 1)
                pygame.draw.circle(sprite, (22, 22, 28), pupil, 2)

            # Cute face: smile + blush cheeks.
            pygame.draw.arc(sprite, outline_color, (self.width // 2 - 10, 42, 20, 12), 0.2, 2.9, 2)
            pygame.draw.circle(sprite, (255, 156, 164), (self.width // 2 - 18, 42), 4)
            pygame.draw.circle(sprite, (255, 156, 164), (self.width // 2 + 18, 42), 4)
            left_shoe = pygame.Rect(self.width // 2 - 18, self.height - 7, 15, 8)
            right_shoe = pygame.Rect(self.width // 2 + 3, self.height - 7, 15, 8)
            pygame.draw.ellipse(sprite, lighten(outline_color, 28), left_shoe)
            pygame.draw.ellipse(sprite, lighten(outline_color, 28), right_shoe)
            self._sprite_cache[self.facing] = sprite

        shadow = pygame.Rect(x + 10, y + self.height - 6, self.width - 20, 10)
        pygame.draw.ellipse(screen, lighten(body_color, -95), shadow)
        screen.blit(sprite, (x, y))


class Platform:
    _sprite_cache = {}

    def __init__(self, x, y, width, kind="normal", vx=0.0, move_range=0.0):
        self.x = float(x)
        self.y = float(y)
        self.width = int(width)
        self.height = PLATFORM_HEIGHT
        self.kind = kind
        self.vx = float(vx)
        self.active = True

        self.min_x = clamp(self.x - move_range, 0.0, float(self.x))
        self.max_x = self.x + move_range

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt_factor, screen_width):
        if not self.active or self.kind != "moving":
            return

        self.x += self.vx * dt_factor

        max_allowed = min(float(screen_width - self.width), self.max_x)
        min_allowed = max(0.0, self.min_x)
        if self.x <= min_allowed:
            self.x = min_allowed
            self.vx = abs(self.vx)
        elif self.x >= max_allowed:
            self.x = max_allowed
            self.vx = -abs(self.vx)

    def shift_y(self, delta):
        self.y += delta

    def consume(self):
        self.active = False

    def draw(self, screen, normal_color, moving_color, boost_color, fragile_color):
        if not self.active:
            return

        if self.kind == "moving":
            base = moving_color
        elif self.kind == "boost":
            base = boost_color
        elif self.kind == "fragile":
            base = fragile_color
        else:
            base = normal_color

        key = (self.kind, self.width, base)
        sprite = self._sprite_cache.get(key)
        if sprite is None:
            sprite = pygame.Surface((self.width + 8, self.height + 8), pygame.SRCALPHA)
            draw_rect = pygame.Rect(4, 3, self.width, self.height)
            pygame.draw.rect(sprite, lighten(base, -45), draw_rect.inflate(4, 6), border_radius=9)
            pygame.draw.rect(sprite, base, draw_rect, border_radius=8)
            pygame.draw.rect(sprite, lighten(base, 52), draw_rect, 2, border_radius=8)

            if self.kind == "boost":
                pygame.draw.circle(sprite, (255, 240, 210), (draw_rect.centerx, draw_rect.centery), 5)
            elif self.kind == "fragile":
                pygame.draw.line(sprite, (82, 48, 26), (draw_rect.x + 10, draw_rect.y + 3), (draw_rect.right - 10, draw_rect.bottom - 3), 2)
                pygame.draw.line(sprite, (82, 48, 26), (draw_rect.x + 16, draw_rect.bottom - 3), (draw_rect.right - 16, draw_rect.y + 3), 2)
            self._sprite_cache[key] = sprite

        screen.blit(sprite, (int(self.x) - 4, int(self.y) - 3))


class Enemy:
    _sprite_cache = {}

    def __init__(self, x, y, width, height, kind="slime", vx=1.5, patrol_left=None, patrol_right=None):
        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)
        self.width = int(width)
        self.height = int(height)
        self.kind = kind
        self.vx = float(vx)
        self.active = True
        self.phase = (x * 0.13 + y * 0.07) % (2 * math.pi)

        if patrol_left is None:
            patrol_left = self.x - 40
        if patrol_right is None:
            patrol_right = self.x + 40
        self.patrol_left = float(min(patrol_left, patrol_right))
        self.patrol_right = float(max(patrol_left, patrol_right))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def shift_y(self, delta):
        self.base_y += delta
        self.y += delta

    def update(self, dt_factor):
        if not self.active:
            return

        self.x += self.vx * dt_factor
        if self.x <= self.patrol_left:
            self.x = self.patrol_left
            self.vx = abs(self.vx)
        elif self.x >= self.patrol_right:
            self.x = self.patrol_right
            self.vx = -abs(self.vx)

        self.phase += 0.07 * dt_factor
        if self.kind == "bat":
            self.y = self.base_y + math.sin(self.phase) * 6.0
        elif self.kind == "ghost":
            self.y = self.base_y + math.sin(self.phase * 1.2) * 8.0
        elif self.kind == "beetle":
            self.y = self.base_y + math.sin(self.phase * 0.45) * 1.8
        else:
            self.y = self.base_y + math.sin(self.phase * 0.75) * 2.5

    def draw(self, screen):
        if not self.active:
            return

        sprite = self._sprite_cache.get(self.kind)
        if sprite is None:
            sprite = pygame.Surface((self.width + 30, self.height + 12), pygame.SRCALPHA)
            if self.kind == "bat":
                wing_left = [(9, 24), (1, 14), (7, 31)]
                wing_right = [(self.width + 21, 24), (self.width + 29, 14), (self.width + 23, 31)]
                pygame.draw.polygon(sprite, lighten(ENEMY_BAT, -18), wing_left)
                pygame.draw.polygon(sprite, lighten(ENEMY_BAT, -18), wing_right)

                body = pygame.Rect(20, 8, self.width - 20, self.height - 10)
                pygame.draw.ellipse(sprite, ENEMY_BAT, body)
                pygame.draw.ellipse(sprite, ENEMY_OUTLINE, body, 2)
                ear_left = [(body.x + 4, body.y + 7), (body.x + 11, body.y - 6), (body.x + 16, body.y + 9)]
                ear_right = [(body.right - 4, body.y + 7), (body.right - 11, body.y - 6), (body.right - 16, body.y + 9)]
                pygame.draw.polygon(sprite, ENEMY_BAT, ear_left)
                pygame.draw.polygon(sprite, ENEMY_BAT, ear_right)
            elif self.kind == "ghost":
                ghost_color = lighten(ENEMY_BAT, 48)
                body = pygame.Rect(13, 4, self.width - 4, self.height - 2)
                pygame.draw.ellipse(sprite, ghost_color, body)
                tail_y = body.bottom - 1
                wave = [
                    (body.x, tail_y - 3),
                    (body.x + 7, tail_y + 4),
                    (body.x + 14, tail_y - 2),
                    (body.x + 21, tail_y + 5),
                    (body.x + 28, tail_y - 1),
                    (body.right, tail_y + 4),
                    (body.right, body.y + 10),
                    (body.x, body.y + 10),
                ]
                pygame.draw.polygon(sprite, ghost_color, wave)
                pygame.draw.ellipse(sprite, ENEMY_OUTLINE, body, 2)
                shine = pygame.Rect(body.x + 6, body.y + 5, body.w // 3, body.h // 4)
                pygame.draw.ellipse(sprite, lighten(ghost_color, 35), shine)
            elif self.kind == "beetle":
                shell_color = lighten(ENEMY_SLIME, -16)
                body = pygame.Rect(14, 9, self.width - 8, self.height - 7)
                pygame.draw.ellipse(sprite, shell_color, body)
                pygame.draw.ellipse(sprite, ENEMY_OUTLINE, body, 2)
                head = pygame.Rect(body.x + 4, body.y - 7, body.w - 8, 12)
                pygame.draw.ellipse(sprite, lighten(shell_color, 10), head)
                pygame.draw.ellipse(sprite, ENEMY_OUTLINE, head, 2)
                pygame.draw.line(sprite, lighten(shell_color, 30), (body.centerx, body.y + 2), (body.centerx, body.bottom - 3), 2)
                for leg_x in (body.x + 3, body.x + 11, body.right - 12, body.right - 4):
                    pygame.draw.line(sprite, ENEMY_OUTLINE, (leg_x, body.bottom - 3), (leg_x - 3, body.bottom + 4), 2)
            else:
                shadow = pygame.Rect(18, self.height + 1, self.width - 18, 7)
                pygame.draw.ellipse(sprite, lighten(ENEMY_SLIME, -95), shadow)
                body = pygame.Rect(12, 4, self.width - 6, self.height - 3)
                pygame.draw.ellipse(sprite, ENEMY_SLIME, body)
                pygame.draw.ellipse(sprite, ENEMY_OUTLINE, body, 2)
                shine = pygame.Rect(body.x + 7, body.y + 5, body.w // 3, body.h // 4)
                pygame.draw.ellipse(sprite, lighten(ENEMY_SLIME, 45), shine)

            eye_left = (self.width // 2 + 7, 20)
            eye_right = (self.width // 2 + 23, 20)
            pygame.draw.circle(sprite, (255, 255, 255), eye_left, 5)
            pygame.draw.circle(sprite, (255, 255, 255), eye_right, 5)
            pygame.draw.circle(sprite, ENEMY_OUTLINE, eye_left, 5, 2)
            pygame.draw.circle(sprite, ENEMY_OUTLINE, eye_right, 5, 2)
            pygame.draw.circle(sprite, (18, 15, 30), eye_left, 2)
            pygame.draw.circle(sprite, (18, 15, 30), eye_right, 2)
            pygame.draw.arc(sprite, ENEMY_OUTLINE, (self.width // 2 + 7, 26, 16, 8), 0.2, 2.9, 2)
            self._sprite_cache[self.kind] = sprite

        screen.blit(sprite, (int(self.x) - 10, int(self.y)))


class Bullet:
    _sprite_cache = {}

    def __init__(self, x, y, radius, speed):
        self.x = float(x)
        self.y = float(y)
        self.radius = int(radius)
        self.vx = 0.0
        self.vy = -abs(float(speed))
        self.active = True

    def get_rect(self):
        r = self.radius
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    def shift_y(self, delta):
        self.y += delta

    def update(self, dt_factor):
        self.x += self.vx * dt_factor
        self.y += self.vy * dt_factor

    def draw(self, screen):
        if not self.active:
            return
        sprite = self._sprite_cache.get(self.radius)
        if sprite is None:
            size = (self.radius + 2) * 2
            sprite = pygame.Surface((size, size), pygame.SRCALPHA)
            center = (size // 2, size // 2)
            pygame.draw.circle(sprite, BULLET_EDGE, center, self.radius + 2)
            pygame.draw.circle(sprite, BULLET_MAIN, center, self.radius)
            pygame.draw.circle(sprite, (255, 255, 255), (center[0] - 1, center[1] - 1), max(1, self.radius // 2))
            self._sprite_cache[self.radius] = sprite
        half = sprite.get_width() // 2
        screen.blit(sprite, (int(self.x) - half, int(self.y) - half))
