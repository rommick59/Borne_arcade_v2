import os
import random
import sys

import pygame

from constants import ALERT, BG_BOTTOM, BG_TOP, BULLET_RADIUS, BULLET_SPEED, CAMERA_TARGET_Y, CARD, CARD_BORDER, COVER_PATH
from constants import ENEMY_H, ENEMY_MOVE_SPEED_MAX, ENEMY_MOVE_SPEED_MIN, ENEMY_SCORE, ENEMY_SPAWN_BASE
from constants import ENEMY_SPAWN_MAX, ENEMY_W, FAIL_Y_MARGIN, FPS, GRAVITY, HIGHLIGHT, HIGHSCORE_PATH
from constants import JUMP_SPEED, KEY_BACK, KEY_BACK_MENU, KEY_CONFIRM, KEY_DOWN, KEY_LEFT, KEY_PAUSE
from constants import KEY_RIGHT, KEY_SHOOT, KEY_UP, MAX_SCORES, NAME_LEN, PLAYER_BODY, PLAYER_H
from constants import PLAYER_MOVE_SPEED, PLAYER_OUTLINE, PLAYER_START_Y, PLAYER_W, PLATFORM_BOOST
from constants import PLATFORM_FRAGILE, PLATFORM_GAP_MAX, PLATFORM_GAP_MIN, PLATFORM_MAX_W, PLATFORM_MIN_W
from constants import PLATFORM_MOVE_RANGE, PLATFORM_MOVE_SPEED_MAX, PLATFORM_MOVE_SPEED_MIN, PLATFORM_MOVING
from constants import PLATFORM_NORMAL, SCORE_PER_PIXEL, SCREEN_H, SCREEN_W, SHOOT_COOLDOWN_MS
from constants import START_PLATFORM_Y, SUPER_JUMP_SPEED, TEXT_DIM, TEXT_MAIN
from entities import Bullet, Enemy, Platform, Player
from helpers import clamp, make_vertical_gradient
from storage import ensure_score_files, load_highscores, save_highscore

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MENU_OPTIONS = ("Jouer", "Regles", "Highscores", "Quitter")
PAUSE_OPTIONS = ("Reprendre", "Retour menu")
RULE_LINES = (
    "But du jeu:",
    "- Montez le plus haut possible en sautant de plateforme en plateforme.",
    "- Le saut est automatique quand vous retombez sur une plateforme.",
    "",
    "Systemes de jeu:",
    "- Plateforme orange: super saut.",
    "- Plateforme bleue: plateforme mouvante.",
    "- Plateforme marron: fragile (disparait apres utilisation).",
    "- Touche F: tir pour eliminer les ennemis.",
    "- Si vous tombez trop bas ou touchez un ennemi: fin de partie.",
    "",
    "Touches borne / clavier:",
    "- Gauche / Droite (ou Q / D): deplacement.",
    "- F (ou Entree): valider et tirer en partie.",
    "- T: pause pendant la partie.",
    "- Y / 4 / Echap: retour menu.",
)


class DoodleJumpeApp:
    def __init__(self):
        pygame.init()
        self.display_surface = self.create_display_surface()
        self.screen = self.display_surface
        self.display_size = self.display_surface.get_size()
        self.software_scale = False
        if self.display_size != (SCREEN_W, SCREEN_H):
            self.screen = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
            self.software_scale = True
        pygame.display.set_caption("Doodle Jumpe - Borne Arcade")
        pygame.mouse.set_visible(False)
        try:
            pygame.event.set_grab(True)
        except pygame.error:
            pass
        self.clock = pygame.time.Clock()
        allowed_events = [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]
        for event_name in ("WINDOWFOCUSGAINED", "WINDOWFOCUSLOST", "ACTIVEEVENT"):
            if hasattr(pygame, event_name):
                allowed_events.append(getattr(pygame, event_name))
        pygame.event.set_allowed(allowed_events)

        self.font_title = pygame.font.SysFont("Impact", 68)
        self.font_big = pygame.font.SysFont("Agency FB", 46, bold=True)
        self.font = pygame.font.SysFont("Trebuchet MS", 32, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 22, bold=True)
        self.text_cache = {}

        self.panel_rect = pygame.Rect(26, 26, SCREEN_W - 52, SCREEN_H - 52)
        self.panel_surface = pygame.Surface(self.panel_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(self.panel_surface, CARD, self.panel_surface.get_rect(), border_radius=18)
        pygame.draw.rect(self.panel_surface, CARD_BORDER, self.panel_surface.get_rect(), 3, border_radius=18)

        self.hud_surface = pygame.Surface((SCREEN_W, 90)).convert()
        self.hud_surface.fill((255, 255, 255))
        pygame.draw.line(self.hud_surface, CARD_BORDER, (0, 90), (SCREEN_W, 90), 2)
        self.hud_tip_surface = self.render_cached(
            self.font_small,
            "Gauche/Droite ou Q/D: deplacer   F: tirer   T: pause   Y/4: menu",
            TEXT_DIM,
        )
        self.hud_tip_pos = (SCREEN_W // 2 - self.hud_tip_surface.get_width() // 2, SCREEN_H - 34)

        self.pause_overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self.pause_overlay.fill((0, 0, 0, 150))
        self.pause_card_rect = pygame.Rect(SCREEN_W // 2 - 196, SCREEN_H // 2 - 134, 392, 258)
        self.pause_card_surface = pygame.Surface(self.pause_card_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(self.pause_card_surface, CARD, self.pause_card_surface.get_rect(), border_radius=14)
        pygame.draw.rect(self.pause_card_surface, CARD_BORDER, self.pause_card_surface.get_rect(), 3, border_radius=14)

        self._hud_score_value = None
        self._hud_score_surface = None
        self._hud_altitude_value = None
        self._hud_altitude_surface = None
        self._hud_enemy_count = None
        self._hud_enemy_surface = None
        self._hud_shoot_ready = None
        self._hud_shoot_surface = None
        self._status_key = None
        self._status_surface = None

        self.running = True
        self.state = "menu"
        self.menu_index = 0
        self.pause_index = 0
        self.move_left = False
        self.move_right = False

        self.name_chars = [0] * NAME_LEN
        self.name_index = 0

        self.score = 0
        self.distance = 0.0
        self.player = Player(SCREEN_W // 2 - PLAYER_W // 2, PLAYER_START_Y, PLAYER_W, PLAYER_H)
        self.platforms = []
        self.enemies = []
        self.bullets = []
        self.shoot_cooldown_until_ms = 0

        self.status_text = ""
        self.status_color = HIGHLIGHT
        self.status_until_ms = 0

        self.pause_started_ms = 0
        self.menu_input_lock_until_ms = 0

        self.rng = random.Random()
        self.cover = self.load_cover()
        self.init_audio()

        self.bg_game = make_vertical_gradient(SCREEN_W, SCREEN_H, BG_TOP, BG_BOTTOM)
        self.bg_menu = make_vertical_gradient(SCREEN_W, SCREEN_H, (190, 241, 255), (241, 252, 255))

        self.clouds = self.build_clouds()

        ensure_score_files(HIGHSCORE_PATH)
        self.highscores_cache = []
        self.refresh_highscores()
        self.reset_run_state()

    def create_display_surface(self):
        if hasattr(pygame, "SCALED"):
            scaled_flags = pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.SCALED
            try:
                return pygame.display.set_mode((SCREEN_W, SCREEN_H), scaled_flags)
            except pygame.error:
                pass

        desktop_size = None
        if hasattr(pygame.display, "get_desktop_sizes"):
            desktop_sizes = pygame.display.get_desktop_sizes()
            if desktop_sizes:
                desktop_size = desktop_sizes[0]
        if desktop_size is None:
            info = pygame.display.Info()
            desktop_size = (max(1, info.current_w), max(1, info.current_h))

        fullscreen_flags = pygame.DOUBLEBUF | pygame.NOFRAME

        try:
            return pygame.display.set_mode(desktop_size, fullscreen_flags)
        except pygame.error:
            fallback_flags = pygame.DOUBLEBUF
            if hasattr(pygame, "SCALED"):
                fallback_flags |= pygame.SCALED
            try:
                return pygame.display.set_mode((SCREEN_W, SCREEN_H), fallback_flags)
            except pygame.error:
                return pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def init_audio(self):
        self.audio_enabled = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            self.audio_enabled = False

        self.sfx_jump = self.load_sound_effect(
            "../DinoRail/assets/sound/jump.mp3",
            "../../sound/bip.mp3",
        )
        self.sfx_boost = self.load_sound_effect(
            "../Columns/sounds/level.mp3",
            "../Minesweeper/sounds/select.mp3",
        )
        self.sfx_shoot = self.load_sound_effect(
            "../ball-blast/assets/sound/pop.mp3",
            "../../sound/bip.mp3",
        )
        self.sfx_hit_enemy = self.load_sound_effect(
            "../ball-blast/assets/sound/explosion.mp3",
            "../Columns/sounds/suppr1.mp3",
        )

    def load_sound_effect(self, *relative_paths):
        if not self.audio_enabled:
            return None
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for rel_path in relative_paths:
            full_path = os.path.normpath(os.path.join(base_dir, rel_path))
            if not os.path.isfile(full_path):
                continue
            try:
                return pygame.mixer.Sound(full_path)
            except pygame.error:
                continue
        return None

    def play_sound(self, sound):
        if not self.audio_enabled or sound is None:
            return
        try:
            sound.play()
        except pygame.error:
            pass

    def load_cover(self):
        if not os.path.exists(COVER_PATH):
            return None
        try:
            image = pygame.image.load(COVER_PATH).convert()
            return pygame.transform.smoothscale(image, (340, 208))
        except pygame.error:
            return None

    def build_clouds(self):
        clouds = []
        seed = random.Random(20260305)
        for _ in range(16):
            size = seed.randint(52, 120)
            clouds.append(
                {
                    "x": seed.randint(-180, SCREEN_W + 120),
                    "y": seed.randint(30, SCREEN_H - 60),
                    "size": size,
                    "speed": seed.uniform(0.05, 0.22),
                    "surface_game": self.make_cloud_surface(size, (255, 255, 255)),
                    "surface_menu": self.make_cloud_surface(size, (246, 252, 255)),
                }
            )
        return clouds

    def make_cloud_surface(self, size, color):
        w = int(size * 1.2)
        h = int(size * 0.74)
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        base_h = int(size * 0.56)
        pygame.draw.ellipse(surface, color, (0, int(size * 0.18), size, base_h))
        pygame.draw.ellipse(
            surface,
            color,
            (int(size * 0.22), 0, int(size * 0.5), int(base_h * 0.65)),
        )
        pygame.draw.ellipse(
            surface,
            color,
            (int(size * 0.52), int(size * 0.08), int(size * 0.43), int(base_h * 0.6)),
        )
        return surface

    def render_cached(self, font, text, color):
        key = (id(font), text, color)
        surface = self.text_cache.get(key)
        if surface is not None:
            return surface

        surface = font.render(text, True, color).convert_alpha()
        if len(self.text_cache) > 4096:
            self.text_cache.clear()
        self.text_cache[key] = surface
        return surface

    def refresh_highscores(self):
        self.highscores_cache = load_highscores(HIGHSCORE_PATH)

    def open_highscores(self):
        self.refresh_highscores()
        self.state = "highscores"

    def reset_run_state(self):
        self.score = 0
        self.distance = 0.0
        self.status_text = ""
        self.status_until_ms = 0

        self.move_left = False
        self.move_right = False

        self.player = Player(SCREEN_W // 2 - PLAYER_W // 2, PLAYER_START_Y, PLAYER_W, PLAYER_H)
        self.player.vy = -9.2

        self.platforms = []
        self.enemies = []
        self.bullets = []
        self.shoot_cooldown_until_ms = 0

    def set_status(self, text, color=HIGHLIGHT, duration_ms=1200):
        self.status_text = text
        self.status_color = color
        self.status_until_ms = pygame.time.get_ticks() + duration_ms

    def difficulty_ratio(self):
        return clamp(self.score / 14500.0, 0.0, 1.0)

    def enemy_spawn_chance(self):
        ratio = self.difficulty_ratio()
        return ENEMY_SPAWN_BASE + (ENEMY_SPAWN_MAX - ENEMY_SPAWN_BASE) * ratio

    def choose_platform_kind(self, force_normal=False):
        if force_normal:
            return "normal"

        ratio = self.difficulty_ratio()
        boost_chance = 0.1
        moving_chance = 0.1 + 0.18 * ratio
        fragile_chance = 0.08 + 0.18 * ratio

        roll = self.rng.random()
        if roll < boost_chance:
            return "boost"
        if roll < boost_chance + moving_chance:
            return "moving"
        if roll < boost_chance + moving_chance + fragile_chance:
            return "fragile"
        return "normal"

    def platform_gap(self):
        ratio = self.difficulty_ratio()
        low = PLATFORM_GAP_MIN + int(10 * ratio)
        high = PLATFORM_GAP_MAX + int(26 * ratio)
        return self.rng.randint(low, high)

    def make_platform(self, y, force_normal=False):
        width = self.rng.randint(PLATFORM_MIN_W, PLATFORM_MAX_W)
        x = self.rng.randint(0, SCREEN_W - width)
        kind = self.choose_platform_kind(force_normal=force_normal)

        vx = 0.0
        move_range = 0.0
        if kind == "moving":
            speed = self.rng.uniform(PLATFORM_MOVE_SPEED_MIN, PLATFORM_MOVE_SPEED_MAX)
            vx = speed if self.rng.random() < 0.5 else -speed
            move_range = float(PLATFORM_MOVE_RANGE + self.rng.randint(-25, 45))

        return Platform(x, y, width, kind=kind, vx=vx, move_range=move_range)

    def maybe_spawn_enemy_for_platform(self, platform):
        if platform.kind != "normal":
            return
        if platform.width < ENEMY_W + 18:
            return
        if platform.y > SCREEN_H - 180:
            return
        if self.rng.random() > self.enemy_spawn_chance():
            return

        left = platform.x + 6
        right = platform.x + platform.width - ENEMY_W - 6
        if right <= left:
            return

        ratio = self.difficulty_ratio()
        speed = self.rng.uniform(ENEMY_MOVE_SPEED_MIN, ENEMY_MOVE_SPEED_MAX) * (1.0 + 0.35 * ratio)
        if self.rng.random() < 0.5:
            speed *= -1

        roll_kind = self.rng.random()
        if roll_kind < (0.2 + 0.25 * ratio):
            kind = "bat"
        elif roll_kind < 0.5:
            kind = "ghost"
        elif roll_kind < 0.75:
            kind = "beetle"
        else:
            kind = "slime"
        x = self.rng.uniform(left, right)
        enemy = Enemy(
            x,
            platform.y - ENEMY_H - 4,
            ENEMY_W,
            ENEMY_H,
            kind=kind,
            vx=speed,
            patrol_left=left,
            patrol_right=right,
        )
        self.enemies.append(enemy)

    def setup_initial_platforms(self):
        base_width = 188
        base_x = SCREEN_W // 2 - base_width // 2
        base = Platform(base_x, START_PLATFORM_Y, base_width, kind="normal")

        self.platforms = [base]
        self.player.x = float(base_x + base_width // 2 - self.player.width // 2)
        self.player.y = float(START_PLATFORM_Y - self.player.height)
        self.player.vy = -10.5

        y = START_PLATFORM_Y
        index = 0
        while y > -SCREEN_H:
            y -= self.platform_gap()
            platform = self.make_platform(y, force_normal=index < 3)
            self.platforms.append(platform)
            if index >= 5:
                self.maybe_spawn_enemy_for_platform(platform)
            index += 1

    def replenish_platforms(self):
        self.platforms = [p for p in self.platforms if p.active and p.y < SCREEN_H + 80]

        if not self.platforms:
            rescue = Platform(SCREEN_W // 2 - 80, START_PLATFORM_Y, 160, kind="normal")
            self.platforms = [rescue]

        top_y = min(platform.y for platform in self.platforms)
        while top_y > -140:
            new_y = top_y - self.platform_gap()
            platform = self.make_platform(new_y)
            self.platforms.append(platform)
            self.maybe_spawn_enemy_for_platform(platform)
            top_y = new_y

    def start_new_run(self):
        self.reset_run_state()
        self.setup_initial_platforms()
        self.name_chars = [0] * NAME_LEN
        self.name_index = 0
        self.state = "game"

    def go_to_menu(self, lock_ms=220):
        self.state = "menu"
        self.menu_input_lock_until_ms = pygame.time.get_ticks() + lock_ms

    def begin_name_input(self):
        self.name_chars = [0] * NAME_LEN
        self.name_index = 0
        self.state = "name_input"

    def shoot(self):
        now = pygame.time.get_ticks()
        if now < self.shoot_cooldown_until_ms:
            return

        self.shoot_cooldown_until_ms = now + SHOOT_COOLDOWN_MS
        x = self.player.x + self.player.width * 0.5
        y = self.player.y + 10
        self.bullets.append(Bullet(x, y, BULLET_RADIUS, BULLET_SPEED))
        self.play_sound(self.sfx_shoot)

    def handle_platform_collisions(self, previous_rect):
        if self.player.vy <= 0:
            return

        player_rect = self.player.get_rect()
        feet_left = player_rect.x + 8
        feet_right = player_rect.right - 8
        feet_top = player_rect.bottom - 5
        feet_bottom = feet_top + 10
        previous_bottom = previous_rect.bottom

        for platform in self.platforms:
            if not platform.active:
                continue
            platform_top = int(platform.y)
            if previous_bottom > platform_top + 8:
                continue
            platform_bottom = platform_top + platform.height
            if feet_bottom < platform_top or feet_top > platform_bottom:
                continue

            platform_left = int(platform.x)
            platform_right = platform_left + platform.width
            if feet_right <= platform_left or feet_left >= platform_right:
                continue

            self.player.y = float(platform_top - self.player.height)
            if platform.kind == "boost":
                self.player.vy = SUPER_JUMP_SPEED
                self.set_status("Super saut", PLATFORM_BOOST, 900)
                self.play_sound(self.sfx_boost)
            else:
                self.player.vy = JUMP_SPEED
                self.play_sound(self.sfx_jump)

            if platform.kind == "fragile":
                platform.consume()
                self.set_status("Plateforme fragile", PLATFORM_FRAGILE, 900)
            return

    def update_enemies(self, dt_factor):
        for enemy in self.enemies:
            enemy.update(dt_factor)

    def update_bullets(self, dt_factor):
        for bullet in self.bullets:
            bullet.update(dt_factor)

    def handle_bullet_enemy_collisions(self):
        if not self.bullets or not self.enemies:
            return

        enemy_boxes = []
        for enemy in self.enemies:
            if not enemy.active:
                continue
            ex = int(enemy.x)
            ey = int(enemy.y)
            enemy_boxes.append((enemy, ex, ey, ex + enemy.width, ey + enemy.height))

        if not enemy_boxes:
            return

        for bullet in self.bullets:
            if not bullet.active:
                continue
            radius = bullet.radius
            bx1 = int(bullet.x - radius)
            by1 = int(bullet.y - radius)
            bx2 = bx1 + radius * 2
            by2 = by1 + radius * 2
            for enemy, ex1, ey1, ex2, ey2 in enemy_boxes:
                if not enemy.active:
                    continue
                if bx2 <= ex1 or bx1 >= ex2 or by2 <= ey1 or by1 >= ey2:
                    continue

                bullet.active = False
                enemy.active = False
                self.score += ENEMY_SCORE
                self.set_status("Ennemi detruit +{}".format(ENEMY_SCORE), HIGHLIGHT, 700)
                self.play_sound(self.sfx_hit_enemy)
                break

    def handle_player_enemy_collision(self):
        px1 = int(self.player.x) + 8
        py1 = int(self.player.y) + 5
        px2 = px1 + self.player.width - 16
        py2 = py1 + self.player.height - 10
        for enemy in self.enemies:
            if not enemy.active:
                continue
            ex1 = int(enemy.x) + 6
            ey1 = int(enemy.y) + 6
            ex2 = ex1 + enemy.width - 12
            ey2 = ey1 + enemy.height - 12
            if px2 <= ex1 or px1 >= ex2 or py2 <= ey1 or py1 >= ey2:
                continue
            self.begin_name_input()
            return True
        return False

    def cleanup_dynamic_objects(self):
        self.bullets[:] = [
            b
            for b in self.bullets
            if b.active and -40 <= b.y <= SCREEN_H + 100 and -50 <= b.x <= SCREEN_W + 50
        ]
        self.enemies[:] = [e for e in self.enemies if e.active and e.y <= SCREEN_H + 120]

    def update_gameplay(self, dt):
        dt_factor = clamp(dt * FPS, 0.55, 1.85)

        direction = 0
        if self.move_left:
            direction -= 1
        if self.move_right:
            direction += 1

        self.player.move_horizontal(direction, PLAYER_MOVE_SPEED, dt_factor)
        self.player.wrap_horizontally(SCREEN_W)

        for platform in self.platforms:
            platform.update(dt_factor, SCREEN_W)

        previous_rect = self.player.get_rect()

        self.player.vy += GRAVITY * dt_factor
        self.player.vy = min(18.0, self.player.vy)
        self.player.y += self.player.vy * dt_factor

        self.handle_platform_collisions(previous_rect)

        if self.player.y < CAMERA_TARGET_Y and self.player.vy < 0:
            shift = CAMERA_TARGET_Y - self.player.y
            self.player.y = float(CAMERA_TARGET_Y)
            for platform in self.platforms:
                platform.shift_y(shift)
            for enemy in self.enemies:
                enemy.shift_y(shift)
            for bullet in self.bullets:
                bullet.shift_y(shift)
            self.distance += shift
            self.score = max(self.score, int(self.distance * SCORE_PER_PIXEL))

        self.replenish_platforms()
        self.update_enemies(dt_factor)
        self.update_bullets(dt_factor)
        self.handle_bullet_enemy_collisions()
        self.cleanup_dynamic_objects()

        if self.handle_player_enemy_collision():
            return

        if self.player.y > SCREEN_H + FAIL_Y_MARGIN:
            self.begin_name_input()

    def draw_background(self, game_mode=True):
        self.screen.blit(self.bg_game if game_mode else self.bg_menu, (0, 0))
        now = pygame.time.get_ticks()

        for cloud in self.clouds:
            drift = int((now * cloud["speed"]) % (SCREEN_W + 280))
            x = cloud["x"] + drift - 160
            y = cloud["y"]
            surface = cloud["surface_game"] if game_mode else cloud["surface_menu"]
            self.screen.blit(surface, (x, y))

    def draw_platforms(self):
        for platform in self.platforms:
            if platform.y < -40 or platform.y > SCREEN_H + 40:
                continue
            platform.draw(
                self.screen,
                normal_color=PLATFORM_NORMAL,
                moving_color=PLATFORM_MOVING,
                boost_color=PLATFORM_BOOST,
                fragile_color=PLATFORM_FRAGILE,
            )

    def draw_enemies(self):
        for enemy in self.enemies:
            if enemy.y < -80 or enemy.y > SCREEN_H + 80:
                continue
            enemy.draw(self.screen)

    def draw_bullets(self):
        for bullet in self.bullets:
            if bullet.y < -20 or bullet.y > SCREEN_H + 40:
                continue
            bullet.draw(self.screen)

    def draw_hud(self):
        self.screen.blit(self.hud_surface, (0, 0))

        if self._hud_score_value != self.score:
            self._hud_score_value = self.score
            self._hud_score_surface = self.render_cached(self.font, "Score {}".format(self.score), TEXT_MAIN)
        self.screen.blit(self._hud_score_surface, (20, 14))

        altitude = int(self.distance)
        if self._hud_altitude_value != altitude:
            self._hud_altitude_value = altitude
            self._hud_altitude_surface = self.render_cached(
                self.font_small, "Altitude {} px".format(altitude), TEXT_DIM
            )
        self.screen.blit(self._hud_altitude_surface, (23, 58))

        enemy_count = len(self.enemies)
        if self._hud_enemy_count != enemy_count:
            self._hud_enemy_count = enemy_count
            self._hud_enemy_surface = self.render_cached(
                self.font_small, "Ennemis {}".format(enemy_count), TEXT_DIM
            )
        self.screen.blit(self._hud_enemy_surface, (280, 58))

        shoot_ready = pygame.time.get_ticks() >= self.shoot_cooldown_until_ms
        if self._hud_shoot_ready != shoot_ready:
            self._hud_shoot_ready = shoot_ready
            shoot_color = HIGHLIGHT if shoot_ready else TEXT_DIM
            shoot_state = "Tir F: pret" if shoot_ready else "Tir F: recharge"
            self._hud_shoot_surface = self.render_cached(self.font_small, shoot_state, shoot_color)
        self.screen.blit(self._hud_shoot_surface, (462, 58))

        self.screen.blit(self.hud_tip_surface, self.hud_tip_pos)

        now = pygame.time.get_ticks()
        if self.status_text and now < self.status_until_ms:
            status_key = (self.status_text, self.status_color)
            if self._status_key != status_key:
                self._status_key = status_key
                self._status_surface = self.render_cached(self.font_small, self.status_text, self.status_color)
            self.screen.blit(self._status_surface, (SCREEN_W // 2 - self._status_surface.get_width() // 2, 58))

    def draw_game(self):
        self.draw_background(game_mode=True)
        self.draw_platforms()
        self.draw_enemies()
        self.draw_bullets()
        self.player.draw(self.screen, PLAYER_BODY, PLAYER_OUTLINE)
        self.draw_hud()

    def draw_menu(self):
        self.draw_background(game_mode=False)
        self.screen.blit(self.panel_surface, self.panel_rect.topleft)

        title = self.render_cached(self.font_title, "DOODLE JUMPE", HIGHLIGHT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 44))

        subtitle = self.render_cached(self.font_small, "Version borne arcade", TEXT_DIM)
        self.screen.blit(subtitle, (SCREEN_W // 2 - subtitle.get_width() // 2, 116))

        if self.cover:
            self.screen.blit(self.cover, (SCREEN_W // 2 - self.cover.get_width() // 2, 154))

        for index, label in enumerate(MENU_OPTIONS):
            color = HIGHLIGHT if self.menu_index == index else TEXT_MAIN
            line = self.render_cached(self.font, label, color)
            self.screen.blit(line, (SCREEN_W // 2 - line.get_width() // 2, 398 + index * 52))

        tip = self.render_cached(
            self.font_small,
            "Haut/Bas: menu   F/Entree: valider   Y/4/Echap: quitter",
            TEXT_DIM,
        )
        self.screen.blit(tip, (SCREEN_W // 2 - tip.get_width() // 2, SCREEN_H - 56))

    def draw_rules(self):
        self.draw_background(game_mode=False)
        self.screen.blit(self.panel_surface, self.panel_rect.topleft)

        title = self.render_cached(self.font_big, "REGLES", HIGHLIGHT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 48))

        y = 130
        for line in RULE_LINES:
            color = HIGHLIGHT if line.endswith(":") else TEXT_MAIN
            txt = self.render_cached(self.font_small, line, color)
            self.screen.blit(txt, (64, y))
            y += 34

        tip = self.render_cached(
            self.font_small,
            "F/Entree pour retour menu   Y/4/Echap pour retour menu",
            TEXT_DIM,
        )
        self.screen.blit(tip, (SCREEN_W // 2 - tip.get_width() // 2, SCREEN_H - 46))

    def draw_highscores(self):
        self.draw_background(game_mode=False)
        title = self.render_cached(self.font_big, "HIGHSCORES", HIGHLIGHT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))

        scores = self.highscores_cache
        if not scores:
            text = self.render_cached(self.font, "Aucun score enregistre", TEXT_MAIN)
            self.screen.blit(text, (SCREEN_W // 2 - text.get_width() // 2, 198))
        else:
            for i in range(MAX_SCORES):
                if i < len(scores):
                    name, value = scores[i]
                    line = "{:>2}. {}  -  {}".format(i + 1, name, value)
                else:
                    line = "{:>2}. {}  -  0".format(i + 1, "-" * NAME_LEN)
                txt = self.render_cached(self.font, line, TEXT_MAIN)
                self.screen.blit(txt, (SCREEN_W // 2 - 176, 138 + i * 42))

        tip = self.render_cached(self.font_small, "F/Entree pour valider   Y/4/Echap pour retour", TEXT_DIM)
        self.screen.blit(tip, (SCREEN_W // 2 - tip.get_width() // 2, SCREEN_H - 56))

    def draw_pause(self):
        self.draw_game()
        self.screen.blit(self.pause_overlay, (0, 0))
        self.screen.blit(self.pause_card_surface, self.pause_card_rect.topleft)

        title = self.render_cached(self.font_big, "PAUSE", HIGHLIGHT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, SCREEN_H // 2 - 106))

        for i, label in enumerate(PAUSE_OPTIONS):
            color = HIGHLIGHT if self.pause_index == i else TEXT_MAIN
            txt = self.render_cached(self.font, label, color)
            self.screen.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, SCREEN_H // 2 - 28 + i * 58))

    def draw_name_input(self):
        self.draw_background(game_mode=False)

        title = self.render_cached(self.font_big, "FIN DE PARTIE", ALERT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 54))

        score_text = self.render_cached(self.font, "Score: {}".format(self.score), TEXT_MAIN)
        self.screen.blit(score_text, (SCREEN_W // 2 - score_text.get_width() // 2, 118))

        sub = self.render_cached(self.font_small, "Entrez votre pseudo (4 lettres)", TEXT_MAIN)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 170))

        box_w = 72
        box_gap = 18
        total_w = NAME_LEN * box_w + (NAME_LEN - 1) * box_gap
        start_x = SCREEN_W // 2 - total_w // 2

        for i in range(NAME_LEN):
            box = pygame.Rect(start_x + i * (box_w + box_gap), 226, box_w, 88)
            fill = (248, 233, 140) if i == self.name_index else (235, 242, 252)
            pygame.draw.rect(self.screen, fill, box, border_radius=8)
            pygame.draw.rect(self.screen, (14, 20, 44), box, 3, border_radius=8)

            letter = ALPHABET[self.name_chars[i]]
            txt = self.render_cached(self.font_big, letter, (14, 20, 44))
            self.screen.blit(txt, (box.centerx - txt.get_width() // 2, box.y + 14))

        tip = self.render_cached(
            self.font_small,
            "Haut/Bas: lettre | Gauche/Droite: position | F/Entree: valider",
            TEXT_MAIN,
        )
        tip2 = self.render_cached(self.font_small, "Y/4/Echap: ignorer et retour menu", TEXT_DIM)
        self.screen.blit(tip, (SCREEN_W // 2 - tip.get_width() // 2, 374))
        self.screen.blit(tip2, (SCREEN_W // 2 - tip2.get_width() // 2, 404))

    def handle_event_menu(self, key):
        if key in KEY_UP:
            self.menu_index = (self.menu_index - 1) % len(MENU_OPTIONS)
        elif key in KEY_DOWN:
            self.menu_index = (self.menu_index + 1) % len(MENU_OPTIONS)
        elif key in KEY_CONFIRM:
            if self.menu_index == 0:
                self.start_new_run()
            elif self.menu_index == 1:
                self.state = "rules"
            elif self.menu_index == 2:
                self.open_highscores()
            else:
                self.running = False
        elif key in KEY_BACK_MENU:
            self.running = False

    def handle_event_game_down(self, key):
        if key in KEY_LEFT:
            self.move_left = True
        if key in KEY_RIGHT:
            self.move_right = True

        if key in KEY_SHOOT:
            self.shoot()
        elif key in KEY_PAUSE:
            self.pause_index = 0
            self.pause_started_ms = pygame.time.get_ticks()
            self.state = "pause"
        elif key in KEY_BACK:
            self.go_to_menu()

    def handle_event_game_up(self, key):
        if key in KEY_LEFT:
            self.move_left = False
        if key in KEY_RIGHT:
            self.move_right = False

    def resume_after_pause(self):
        now = pygame.time.get_ticks()
        delta = now - self.pause_started_ms
        if self.status_until_ms:
            self.status_until_ms += delta
        self.state = "game"

    def handle_event_pause(self, key):
        if key in KEY_UP or key in KEY_DOWN:
            self.pause_index = 1 - self.pause_index
        elif key in KEY_CONFIRM:
            if self.pause_index == 0:
                self.resume_after_pause()
            else:
                self.go_to_menu()
        elif key in KEY_BACK:
            self.resume_after_pause()

    def handle_event_name_input(self, key):
        alphabet_len = len(ALPHABET)
        if key in KEY_LEFT:
            self.name_index = (self.name_index - 1) % NAME_LEN
        elif key in KEY_RIGHT:
            self.name_index = (self.name_index + 1) % NAME_LEN
        elif key in KEY_UP:
            self.name_chars[self.name_index] = (self.name_chars[self.name_index] + 1) % alphabet_len
        elif key in KEY_DOWN:
            self.name_chars[self.name_index] = (self.name_chars[self.name_index] - 1) % alphabet_len
        elif key in KEY_CONFIRM:
            name = "".join(ALPHABET[index] for index in self.name_chars)
            save_highscore(HIGHSCORE_PATH, name, self.score)
            self.open_highscores()
        elif key in KEY_BACK:
            self.go_to_menu()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if getattr(event, "unicode", "") == "'":
                        key = pygame.K_QUOTE
                    if self.state == "menu" and now < self.menu_input_lock_until_ms:
                        continue

                    if self.state == "menu":
                        self.handle_event_menu(key)
                    elif self.state == "game":
                        self.handle_event_game_down(key)
                    elif self.state == "pause":
                        self.handle_event_pause(key)
                    elif self.state == "highscores":
                        if key in KEY_CONFIRM or key in KEY_BACK_MENU:
                            self.go_to_menu()
                    elif self.state == "rules":
                        if key in KEY_CONFIRM or key in KEY_BACK_MENU:
                            self.go_to_menu()
                    elif self.state == "name_input":
                        self.handle_event_name_input(key)
                elif event.type == pygame.KEYUP:
                    if self.state == "game":
                        self.handle_event_game_up(event.key)

            if self.state == "game":
                self.update_gameplay(dt)
                self.draw_game()
            elif self.state == "pause":
                self.draw_pause()
            elif self.state == "highscores":
                self.draw_highscores()
            elif self.state == "rules":
                self.draw_rules()
            elif self.state == "name_input":
                self.draw_name_input()
            else:
                self.draw_menu()

            if self.software_scale:
                pygame.transform.scale(self.screen, self.display_size, self.display_surface)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)


def run_game():
    DoodleJumpeApp().run()
