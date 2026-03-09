import math
import os
import random
from dataclasses import dataclass

import pygame


pygame.init()
BLEND_ALPHA_COMPAT = getattr(pygame, "BLEND_ALPHA_SDL2", 0)


def draw_rect_compat(surface, color, rect, width=0, border_radius=0):
    if border_radius > 0:
        try:
            pygame.draw.rect(surface, color, rect, width, border_radius)
            return
        except TypeError:
            pass
    pygame.draw.rect(surface, color, rect, width)

DISPLAY_INFO = pygame.display.Info()
WIDTH = DISPLAY_INFO.current_w if DISPLAY_INFO.current_w > 0 else 1000
HEIGHT = DISPLAY_INFO.current_h if DISPLAY_INFO.current_h > 0 else 760
FPS = 120

BUBBLE_RADIUS = 22
BUBBLE_DIAMETER = BUBBLE_RADIUS * 2
ROW_HEIGHT = int(BUBBLE_RADIUS * math.sqrt(3))
GRID_COLS = 18
GRID_MAX_ROWS = 20
INITIAL_ROWS = 8
LOSE_ROW = 14

GRID_LEFT = (WIDTH - (GRID_COLS * BUBBLE_DIAMETER + BUBBLE_RADIUS)) // 2
GRID_TOP = 90
GRID_RIGHT = WIDTH - GRID_LEFT

SHOOTER_POS = pygame.Vector2(WIDTH // 2, HEIGHT - 90)
SHOT_SPEED = 920
SHOT_MAX_STEP = 8

AIM_SPEED = 1
AIM_TAP_STEP = 0.035

NEW_ROW_EVERY = 6

KEY_START = {"t"}
KEY_QUIT = {"h"}
KEY_RESTART = {"g"}
KEY_SHOOT = {"r"}
KEY_AIM_LEFT = {"f"}
KEY_AIM_RIGHT = {"y"}
NAME_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ."
NAME_LENGTH = 3

COLORS = [
    (56, 166, 255),
    (255, 92, 92),
    (255, 214, 74),
    (74, 224, 126),
    (170, 112, 255),
    (255, 152, 58),
]

BG_TOP = (14, 18, 40)
BG_BOTTOM = (26, 15, 53)


@dataclass
class Bubble:
    row: int
    col: int
    color_index: int


@dataclass
class ShotBubble:
    position: pygame.Vector2
    velocity: pygame.Vector2
    color_index: int


@dataclass
class Particle:
    position: pygame.Vector2
    velocity: pygame.Vector2
    color: tuple[int, int, int]
    life: float
    radius: float
    gravity: float

    def update(self, dt: float):
        self.life -= dt
        self.velocity.y += self.gravity * dt
        self.position += self.velocity * dt
        self.radius = max(0.4, self.radius - dt * 8)

    def draw(self, surface: pygame.Surface):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(self.life * 255)))
        size = int(self.radius * 5)
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            particle_surf,
            (*self.color, alpha),
            (size, size),
            int(self.radius * 2),
        )
        surface.blit(particle_surf, (self.position.x - size, self.position.y - size), special_flags=BLEND_ALPHA_COMPAT)


class BubbleShooterGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Babble Shot - Neon Bubble Shooter")
        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.hud_font = pygame.font.SysFont("arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.aim_angle = -math.pi / 2
        self.board: dict[tuple[int, int], Bubble] = {}
        self.current_shot: ShotBubble | None = None
        self.current_color = 0
        self.next_color = 0
        self.highscore_file = os.path.join(os.path.dirname(__file__), "highscore")
        self.highscores: list[tuple[str, int]] = []
        self.name_letters = ["A"] * NAME_LENGTH
        self.name_cursor = 0
        self.end_state_after_name = "lost"

        self.score = 0
        self.combo = 0
        self.shots_taken = 0
        self.game_state = "menu"
        self.screen_shake = 0.0

        self.particles: list[Particle] = []

        self.background = self._create_background()
        self.bubble_surfaces = self._create_bubble_surfaces()
        self._load_highscores()

        self.reset_game()

    def reset_game(self):
        self.board.clear()
        self.particles.clear()
        self.current_shot = None
        self.score = 0
        self.combo = 0
        self.shots_taken = 0
        self.screen_shake = 0
        self.game_state = "playing"

        available_colors = [0, 1, 2, 3, 4]
        for row in range(INITIAL_ROWS):
            for col in range(GRID_COLS):
                if row % 2 == 1 and col == GRID_COLS - 1:
                    continue
                if random.random() < 0.95:
                    color_index = random.choice(available_colors)
                    self.board[(row, col)] = Bubble(row, col, color_index)

        self.current_color = self._pick_color_for_spawn()
        self.next_color = self._pick_color_for_spawn()

    def _load_highscores(self):
        self.highscores = []
        try:
            if not os.path.exists(self.highscore_file):
                with open(self.highscore_file, "w", encoding="utf-8"):
                    pass
            with open(self.highscore_file, "r", encoding="utf-8") as file:
                for raw_line in file:
                    line = raw_line.strip()
                    if not line or "-" not in line:
                        continue
                    name, score_text = line.split("-", 1)
                    try:
                        score = int(score_text)
                    except ValueError:
                        continue
                    if len(name) == 0:
                        name = "AAA"
                    self.highscores.append((name[:NAME_LENGTH], score))
            self.highscores.sort(key=lambda item: item[1], reverse=True)
            self.highscores = self.highscores[:10]
        except Exception:
            self.highscores = []

    def _save_highscores(self):
        try:
            with open(self.highscore_file, "w", encoding="utf-8") as file:
                for i, (name, score) in enumerate(self.highscores):
                    file.write(f"{name}-{score}")
                    if i < len(self.highscores) - 1:
                        file.write("\n")
        except Exception:
            pass

    def _next_name_char(self, value: str):
        index = NAME_ALPHABET.find(value)
        if index == -1:
            return NAME_ALPHABET[0]
        return NAME_ALPHABET[(index + 1) % len(NAME_ALPHABET)]

    def _prev_name_char(self, value: str):
        index = NAME_ALPHABET.find(value)
        if index == -1:
            return NAME_ALPHABET[0]
        return NAME_ALPHABET[(index - 1) % len(NAME_ALPHABET)]

    def _start_name_entry(self, result_state: str):
        self.end_state_after_name = result_state
        self.name_letters = ["A"] * NAME_LENGTH
        self.name_cursor = 0
        self.game_state = "name_entry"

    def _confirm_name_entry(self):
        name = "".join(self.name_letters)
        if name.strip() == "":
            name = "AAA"

        self.highscores.append((name, self.score))
        self.highscores.sort(key=lambda item: item[1], reverse=True)
        self.highscores = self.highscores[:10]
        self._save_highscores()
        self.game_state = self.end_state_after_name

    def _create_background(self):
        bg = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
            g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
            b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
            pygame.draw.line(bg, (r, g, b), (0, y), (WIDTH, y))

        for _ in range(90):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            alpha = random.randint(40, 120)
            star = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            pygame.draw.circle(star, (255, 255, 255, alpha), (size * 2, size * 2), size)
            bg.blit(star, (x, y), special_flags=BLEND_ALPHA_COMPAT)

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow, (86, 226, 253, 30), (WIDTH // 2, HEIGHT - 120), 260)
        pygame.draw.circle(glow, (255, 120, 210, 24), (WIDTH // 2, GRID_TOP + 130), 320)
        bg.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
        return bg

    def _create_bubble_surfaces(self):
        cache: dict[int, pygame.Surface] = {}
        size = BUBBLE_DIAMETER * 2
        center = size // 2

        for i, color in enumerate(COLORS):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            outline_color = (
                max(0, int(color[0] * 0.35)),
                max(0, int(color[1] * 0.35)),
                max(0, int(color[2] * 0.35)),
                255,
            )

            for ring in range(BUBBLE_RADIUS, 1, -1):
                t = ring / BUBBLE_RADIUS
                shade = (
                    int(color[0] * (0.55 + 0.45 * t)),
                    int(color[1] * (0.55 + 0.45 * t)),
                    int(color[2] * (0.55 + 0.45 * t)),
                    255,
                )
                pygame.draw.circle(surf, shade, (center, center), ring)

            pygame.draw.circle(surf, outline_color, (center, center), BUBBLE_RADIUS, 3)

            pygame.draw.circle(surf, (255, 255, 255, 90), (center - 7, center - 8), BUBBLE_RADIUS // 2)
            pygame.draw.circle(surf, (255, 255, 255, 45), (center - 13, center - 14), BUBBLE_RADIUS // 5)

            aura = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(aura, (*color, 40), (center, center), BUBBLE_RADIUS + 6)
            surf.blit(aura, (0, 0), special_flags=pygame.BLEND_ADD)

            cache[i] = surf

        return cache

    def _grid_to_pixel(self, row: int, col: int):
        x = GRID_LEFT + BUBBLE_RADIUS + col * BUBBLE_DIAMETER + (row % 2) * BUBBLE_RADIUS
        y = GRID_TOP + BUBBLE_RADIUS + row * ROW_HEIGHT
        return pygame.Vector2(x, y)

    def _pixel_to_grid(self, pos: pygame.Vector2):
        approx_row = int(round((pos.y - GRID_TOP - BUBBLE_RADIUS) / ROW_HEIGHT))
        approx_row = max(0, min(GRID_MAX_ROWS - 1, approx_row))

        offset = (approx_row % 2) * BUBBLE_RADIUS
        approx_col = int(round((pos.x - GRID_LEFT - BUBBLE_RADIUS - offset) / BUBBLE_DIAMETER))
        approx_col = max(0, min(GRID_COLS - 1, approx_col))

        return approx_row, approx_col

    def _neighbors(self, row: int, col: int):
        if row % 2 == 0:
            deltas = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        else:
            deltas = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]

        out = []
        for dr, dc in deltas:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_MAX_ROWS and 0 <= nc < GRID_COLS:
                if nr % 2 == 1 and nc == GRID_COLS - 1:
                    continue
                out.append((nr, nc))
        return out

    def _connected_same_color(self, start: tuple[int, int]):
        if start not in self.board:
            return set()
        color = self.board[start].color_index
        visited = set([start])
        stack = [start]
        while stack:
            node = stack.pop()
            for nb in self._neighbors(*node):
                if nb in visited or nb not in self.board:
                    continue
                if self.board[nb].color_index == color:
                    visited.add(nb)
                    stack.append(nb)
        return visited

    def _connected_to_top(self):
        visited = set()
        stack = [k for k in self.board.keys() if k[0] == 0]
        for s in stack:
            visited.add(s)

        while stack:
            node = stack.pop()
            for nb in self._neighbors(*node):
                if nb in visited or nb not in self.board:
                    continue
                visited.add(nb)
                stack.append(nb)
        return visited

    def _drop_floating(self, grant_rewards: bool = True):
        anchored = self._connected_to_top()
        floating = [k for k in self.board if k not in anchored]
        for key in floating:
            bubble = self.board.pop(key)
            self._burst_particles(self._grid_to_pixel(bubble.row, bubble.col), COLORS[bubble.color_index], 16, intense=True)
        if floating and grant_rewards:
            self.score += len(floating) * 22
            self.combo += 1
            self.screen_shake = max(self.screen_shake, 8)
        elif floating:
            self.screen_shake = max(self.screen_shake, 6)

    def _pick_color_for_spawn(self):
        if self.board:
            choices = sorted({b.color_index for b in self.board.values()})
            return random.choice(choices)
        return random.randint(0, len(COLORS) - 1)

    def _find_nearest_empty_cell(self, desired_row: int, desired_col: int):
        desired_row = max(0, min(GRID_MAX_ROWS - 1, desired_row))
        desired_col = max(0, min(GRID_COLS - 1, desired_col))

        if desired_row % 2 == 1 and desired_col == GRID_COLS - 1:
            desired_col -= 1

        if (desired_row, desired_col) not in self.board:
            return desired_row, desired_col

        queue = [(desired_row, desired_col)]
        visited = {(desired_row, desired_col)}

        while queue:
            r, c = queue.pop(0)
            for nb in self._neighbors(r, c):
                if nb in visited:
                    continue
                visited.add(nb)
                if nb not in self.board:
                    return nb
                queue.append(nb)

        for row in range(GRID_MAX_ROWS):
            for col in range(GRID_COLS):
                if row % 2 == 1 and col == GRID_COLS - 1:
                    continue
                if (row, col) not in self.board:
                    return row, col

        return GRID_MAX_ROWS - 1, GRID_COLS // 2

    def _burst_particles(self, pos: pygame.Vector2, color, amount: int, intense=False):
        speed_min, speed_max = (120, 340) if intense else (80, 220)
        for _ in range(amount):
            angle = random.random() * math.tau
            speed = random.uniform(speed_min, speed_max)
            vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            p = Particle(
                position=pygame.Vector2(pos.x, pos.y),
                velocity=vel,
                color=color,
                life=random.uniform(0.35, 0.8),
                radius=random.uniform(2.5, 5.0),
                gravity=random.uniform(180, 340),
            )
            self.particles.append(p)

    def _shoot(self):
        if self.current_shot or self.game_state != "playing":
            return

        dx = math.cos(self.aim_angle)
        dy = math.sin(self.aim_angle)
        if dy > -0.15:
            dy = -0.15

        velocity = pygame.Vector2(dx, dy).normalize() * SHOT_SPEED
        self.current_shot = ShotBubble(pygame.Vector2(SHOOTER_POS), velocity, self.current_color)
        self.current_color = self.next_color
        self.next_color = self._pick_color_for_spawn()

    def _insert_shot_to_grid(self):
        if not self.current_shot:
            return

        row, col = self._pixel_to_grid(self.current_shot.position)
        row, col = self._find_nearest_empty_cell(row, col)

        placed = Bubble(row, col, self.current_shot.color_index)
        self.board[(row, col)] = placed
        placed_pos = self._grid_to_pixel(row, col)

        self._burst_particles(placed_pos, COLORS[placed.color_index], 10)

        connected = self._connected_same_color((row, col))
        popped = False

        if len(connected) >= 3:
            popped = True
            base_gain = len(connected) * 18
            combo_bonus = self.combo * 15
            self.score += base_gain + combo_bonus
            self.combo += 1
            self.screen_shake = max(self.screen_shake, 7)

            for key in connected:
                bubble = self.board.pop(key)
                self._burst_particles(self._grid_to_pixel(bubble.row, bubble.col), COLORS[bubble.color_index], 18, intense=True)

            self._drop_floating()
        else:
            self.combo = 0

        if not popped:
            self.shots_taken += 1
            if self.shots_taken % NEW_ROW_EVERY == 0:
                self._push_new_row()

        self.current_shot = None

        if not self.board:
            self._start_name_entry("won")
        elif self._has_lost():
            self._start_name_entry("lost")

    def _push_new_row(self):
        new_board: dict[tuple[int, int], Bubble] = {}
        for (row, col), bubble in self.board.items():
            nr = row + 1
            if nr >= GRID_MAX_ROWS:
                continue
            new_board[(nr, col)] = Bubble(nr, col, bubble.color_index)

        self.board = new_board

        active_colors = sorted({b.color_index for b in self.board.values()})
        if not active_colors:
            active_colors = [0, 1, 2, 3]

        for col in range(GRID_COLS):
            if col == GRID_COLS - 1:
                continue
            if random.random() < 0.95:
                color = random.choice(active_colors)
                self.board[(0, col)] = Bubble(0, col, color)

        self._drop_floating(grant_rewards=False)

        self.screen_shake = max(self.screen_shake, 5)
        if self._has_lost():
            self._start_name_entry("lost")

    def _has_lost(self):
        for bubble in self.board.values():
            if bubble.row >= LOSE_ROW:
                return True
        return False

    def _update_aim(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_f]:
            self.aim_angle -= AIM_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_y]:
            self.aim_angle += AIM_SPEED * dt

        self.aim_angle = max(-math.radians(170), min(-math.radians(10), self.aim_angle))

    def _collides_with_board(self, pos: pygame.Vector2):
        collision_distance_sq = BUBBLE_DIAMETER ** 2
        for bubble in self.board.values():
            bpos = self._grid_to_pixel(bubble.row, bubble.col)
            if pos.distance_squared_to(bpos) <= collision_distance_sq:
                return True
        return False

    def _update_shot(self, dt):
        if not self.current_shot:
            return

        shot = self.current_shot
        movement = shot.velocity * dt
        distance = movement.length()
        steps = max(1, math.ceil(distance / SHOT_MAX_STEP))
        step_move = movement / steps

        for _ in range(steps):
            shot.position += step_move

            if shot.position.x <= GRID_LEFT + BUBBLE_RADIUS:
                shot.position.x = GRID_LEFT + BUBBLE_RADIUS
                shot.velocity.x = abs(shot.velocity.x)
                step_move.x = abs(step_move.x)
            elif shot.position.x >= GRID_RIGHT - BUBBLE_RADIUS:
                shot.position.x = GRID_RIGHT - BUBBLE_RADIUS
                shot.velocity.x = -abs(shot.velocity.x)
                step_move.x = -abs(step_move.x)

            if shot.position.y <= GRID_TOP + BUBBLE_RADIUS:
                self._insert_shot_to_grid()
                return

            if self._collides_with_board(shot.position):
                self._insert_shot_to_grid()
                return

    def _update_particles(self, dt):
        alive = []
        for p in self.particles:
            p.update(dt)
            if p.life > 0:
                alive.append(p)
        self.particles = alive

    def _draw_shooter(self):
        base = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(base, (88, 235, 255, 25), (90, 90), 78)
        pygame.draw.circle(base, (255, 120, 210, 22), (90, 90), 62)
        self.screen.blit(base, (SHOOTER_POS.x - 90, SHOOTER_POS.y - 90), special_flags=pygame.BLEND_ADD)

        barrel_len = 84
        tip = pygame.Vector2(
            SHOOTER_POS.x + math.cos(self.aim_angle) * barrel_len,
            SHOOTER_POS.y + math.sin(self.aim_angle) * barrel_len,
        )
        pygame.draw.line(self.screen, (70, 235, 255), SHOOTER_POS, tip, 10)
        pygame.draw.line(self.screen, (255, 255, 255), SHOOTER_POS, tip, 3)

        pygame.draw.circle(self.screen, (26, 36, 64), (int(SHOOTER_POS.x), int(SHOOTER_POS.y)), 24)
        pygame.draw.circle(self.screen, (130, 220, 255), (int(SHOOTER_POS.x), int(SHOOTER_POS.y)), 20, 3)

        bubble = self.bubble_surfaces[self.current_color]
        self.screen.blit(bubble, (SHOOTER_POS.x - bubble.get_width() // 2, SHOOTER_POS.y - bubble.get_height() // 2))

        nx, ny = SHOOTER_POS.x + 64, SHOOTER_POS.y + 8
        nb = self.bubble_surfaces[self.next_color]
        scaled = pygame.transform.smoothscale(nb, (int(nb.get_width() * 0.72), int(nb.get_height() * 0.72)))
        self.screen.blit(scaled, (nx - scaled.get_width() // 2, ny - scaled.get_height() // 2))

    def _draw_aim_guide(self):
        points = []
        pos = pygame.Vector2(SHOOTER_POS)
        vel = pygame.Vector2(math.cos(self.aim_angle), math.sin(self.aim_angle)) * 12

        for _ in range(55):
            pos += vel
            if pos.x <= GRID_LEFT + BUBBLE_RADIUS or pos.x >= GRID_RIGHT - BUBBLE_RADIUS:
                vel.x *= -1
            if pos.y <= GRID_TOP:
                break
            points.append((int(pos.x), int(pos.y)))

        for i, p in enumerate(points[::2]):
            alpha = max(30, 180 - i * 9)
            dot = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(dot, (160, 245, 255, alpha), (5, 5), 3)
            self.screen.blit(dot, (p[0] - 5, p[1] - 5), special_flags=pygame.BLEND_ADD)

    def _draw_board(self):
        panel = pygame.Surface((GRID_RIGHT - GRID_LEFT + 32, HEIGHT - GRID_TOP + 18), pygame.SRCALPHA)
        draw_rect_compat(panel, (10, 14, 35, 110), panel.get_rect(), 0, 22)
        draw_rect_compat(panel, (100, 190, 255, 60), panel.get_rect(), 2, 22)
        self.screen.blit(panel, (GRID_LEFT - 16, GRID_TOP - 10))

        for bubble in self.board.values():
            pos = self._grid_to_pixel(bubble.row, bubble.col)
            surf = self.bubble_surfaces[bubble.color_index]
            self.screen.blit(surf, (pos.x - surf.get_width() // 2, pos.y - surf.get_height() // 2))

        if self.current_shot:
            pos = self.current_shot.position
            surf = self.bubble_surfaces[self.current_shot.color_index]
            self.screen.blit(surf, (pos.x - surf.get_width() // 2, pos.y - surf.get_height() // 2))

        danger_y = int(self._grid_to_pixel(LOSE_ROW, 0).y)
        pygame.draw.line(self.screen, (255, 92, 92), (GRID_LEFT + 8, danger_y), (GRID_RIGHT - 8, danger_y), 2)

    def _draw_hud(self):
        score_txt = self.hud_font.render(f"Score  {self.score}", True, (234, 245, 255))
        combo_txt = self.hud_font.render(f"Combo  x{self.combo}", True, (255, 190, 235))
        shots_txt = self.small_font.render(f"Ligne +1 dans {NEW_ROW_EVERY - (self.shots_taken % NEW_ROW_EVERY)} tir(s)", True, (174, 210, 255))

        self.screen.blit(score_txt, (36, 22))
        self.screen.blit(combo_txt, (36, 54))
        self.screen.blit(shots_txt, (36, 84))

        right = self.small_font.render("←/→ ou f/y viser • r tirer • t jouer • g rejouer • h quitter", True, (190, 210, 255))
        self.screen.blit(right, (WIDTH - right.get_width() - 32, 30))

        if self.highscores:
            best_name, best_score = self.highscores[0]
            top_txt = self.small_font.render(f"Top 1  {best_name} - {best_score}", True, (255, 230, 180))
            self.screen.blit(top_txt, (36, 112))

    def _draw_overlay(self, title: str, subtitle: str, color=(255, 255, 255)):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((6, 9, 22, 160))
        self.screen.blit(overlay, (0, 0))

        card = pygame.Surface((620, 290), pygame.SRCALPHA)
        draw_rect_compat(card, (18, 28, 58, 210), card.get_rect(), 0, 26)
        draw_rect_compat(card, (118, 228, 255, 120), card.get_rect(), 2, 26)

        self.screen.blit(card, (WIDTH // 2 - 310, HEIGHT // 2 - 160))

        t = self.title_font.render(title, True, color)
        s = self.hud_font.render(subtitle, True, (220, 235, 255))
        c = self.small_font.render("t pour jouer • h pour quitter", True, (185, 205, 240))

        self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 108))
        self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 - 25))
        self.screen.blit(c, (WIDTH // 2 - c.get_width() // 2, HEIGHT // 2 + 54))

    def _draw_name_entry(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((6, 9, 22, 185))
        self.screen.blit(overlay, (0, 0))

        card = pygame.Surface((760, 430), pygame.SRCALPHA)
        draw_rect_compat(card, (18, 28, 58, 225), card.get_rect(), 0, 26)
        draw_rect_compat(card, (118, 228, 255, 130), card.get_rect(), 2, 26)
        self.screen.blit(card, (WIDTH // 2 - 380, HEIGHT // 2 - 230))

        title = self.title_font.render("Nouveau HighScore", True, (235, 245, 255))
        sub = self.hud_font.render(f"Score  {self.score}", True, (255, 210, 170))
        help_text = self.small_font.render("←/→ case • ↑/↓ lettre • r confirmer", True, (190, 210, 245))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 190))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 130))

        box_y = HEIGHT // 2 - 30
        box_w = 90
        box_h = 120
        spacing = 42
        start_x = WIDTH // 2 - (NAME_LENGTH * box_w + (NAME_LENGTH - 1) * spacing) // 2

        for i, letter in enumerate(self.name_letters):
            x = start_x + i * (box_w + spacing)
            active = i == self.name_cursor
            bg_color = (45, 70, 120, 220) if active else (28, 45, 84, 210)
            border_color = (255, 230, 140) if active else (120, 190, 240)
            box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            draw_rect_compat(box, bg_color, box.get_rect(), 0, 16)
            draw_rect_compat(box, border_color, box.get_rect(), 3, 16)
            self.screen.blit(box, (x, box_y))

            letter_surface = self.title_font.render(letter, True, (245, 250, 255))
            self.screen.blit(
                letter_surface,
                (x + box_w // 2 - letter_surface.get_width() // 2, box_y + box_h // 2 - letter_surface.get_height() // 2 - 4),
            )

        self.screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT // 2 + 130))

        ranking_y = HEIGHT // 2 + 172
        for index, (name, score) in enumerate(self.highscores[:3]):
            text = self.small_font.render(f"{index + 1}. {name} - {score}", True, (170, 200, 240))
            self.screen.blit(text, (WIDTH // 2 - 150, ranking_y + index * 24))

    def _apply_screen_shake(self):
        if self.screen_shake <= 0:
            return 0, 0
        intensity = self.screen_shake
        self.screen_shake = max(0, self.screen_shake - 0.45)
        return random.uniform(-intensity, intensity), random.uniform(-intensity, intensity)

    def update(self, dt):
        if self.game_state != "playing":
            self._update_particles(dt)
            return

        self._update_aim(dt)
        self._update_shot(dt)
        self._update_particles(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        shake_x, shake_y = self._apply_screen_shake()
        if shake_x or shake_y:
            temp = self.screen.copy()
            self.screen.blit(temp, (shake_x, shake_y))

        self._draw_board()
        self._draw_aim_guide()
        self._draw_shooter()

        for p in self.particles:
            p.draw(self.screen)

        self._draw_hud()

        if self.game_state == "menu":
            self._draw_overlay("Babble Shot", "Bubble Shooter Néon ultra stylé")
        elif self.game_state == "name_entry":
            self._draw_name_entry()
        elif self.game_state == "won":
            self._draw_overlay("Victoire !", f"Score final : {self.score}", (140, 255, 180))
        elif self.game_state == "lost":
            self._draw_overlay("Game Over", f"Score final : {self.score}", (255, 150, 150))

        pygame.display.flip()

    def run(self):
        self.game_state = "menu"

        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                        self.running = False
                        continue

                    key_char = event.unicode.lower()
                    if self.game_state == "name_entry":
                        if event.key == pygame.K_LEFT and self.name_cursor > 0:
                            self.name_cursor -= 1
                        if event.key == pygame.K_RIGHT and self.name_cursor < NAME_LENGTH - 1:
                            self.name_cursor += 1
                        if event.key == pygame.K_UP:
                            self.name_letters[self.name_cursor] = self._next_name_char(self.name_letters[self.name_cursor])
                        if event.key == pygame.K_DOWN:
                            self.name_letters[self.name_cursor] = self._prev_name_char(self.name_letters[self.name_cursor])
                        if key_char in KEY_SHOOT:
                            self._confirm_name_entry()
                    else:
                        if key_char in KEY_QUIT:
                            self.running = False
                        if key_char in KEY_START:
                            self.reset_game()
                        if key_char in KEY_SHOOT:
                            self._shoot()
                        if key_char in KEY_RESTART:
                            self.reset_game()

                        if key_char in KEY_AIM_LEFT:
                            self.aim_angle -= AIM_TAP_STEP
                        if key_char in KEY_AIM_RIGHT:
                            self.aim_angle += AIM_TAP_STEP

                        self.aim_angle = max(-math.radians(170), min(-math.radians(10), self.aim_angle))

            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    BubbleShooterGame().run()
