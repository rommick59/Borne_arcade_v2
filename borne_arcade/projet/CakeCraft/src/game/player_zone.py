import pygame
import math
import random
from core.enums import Side, CustomerState, CakeType, Ingredient, GameState, DeliveryResult
from core.constants import (
    MAP_SEPARATOR_COLOR, MAP_SEPARATOR_WIDTH, MAP_KITCHEN_RATIO,
    MAP_INGREDIENT_BOX_RATIO, MAP_CUSTOMER_GAP_RATIO,
    MAP_COMPTOIR_HEIGHT, MAP_COMPTOIR_COLOR,
    PLAYER_SIZE, PLAYER_1_COLOR, PLAYER_2_COLOR,
    CUSTOMER_SIZE, CUSTOMER_MAX_COUNT,
    PLAYER_1_KEYS, PLAYER_2_KEYS, PLAYER_1_INTERACT, PLAYER_2_INTERACT,
    FONT_TITLE_PATH, FONT_BODY_PATH,
    MAX_FAILED_CUSTOMERS,
)
from entity.player import Player
from entity.customer import Customer
from core.position import Position
from interactable.creator import Creator
from interactable.deletor import Deletor
from interactable.holder import Holder
from interactable.hoven import Hoven
from interactable.workbench import Workbench
from interactable.counter import Counter


# Font globals (lazy load)
_FONT_TITLE = None
_FONT_BODY  = None
_FONT_LABEL = None

_PAD = 12

_CAKE_PALETTE = {
    CakeType.VANILLA_CAKE:    ((230, 168, 10),  (85, 58, 0)),
    CakeType.CHOCOLATE_CAKE:  ((88, 42, 12),    (255, 228, 200)),
    CakeType.STRAWBERRY_CAKE: ((202, 38, 85),   (255, 238, 244)),
    CakeType.CREAM_PUFF:      ((210, 175, 125), (72, 46, 16)),
}

_INGREDIENT_PALETTE = {
    Ingredient.FLOUR:      ((248, 242, 228), (112, 86, 52)),
    Ingredient.EGG:        ((255, 222, 85),  (112, 78, 0)),
    Ingredient.BUTTER:     ((255, 200, 8),   (112, 78, 0)),
    Ingredient.SUGAR:      ((255, 182, 202), (152, 48, 85)),
    Ingredient.CREAM:      ((244, 226, 212), (105, 76, 50)),
    Ingredient.CHOCOLATE:  ((88, 42, 12),    (255, 225, 192)),
    Ingredient.STRAWBERRY: ((222, 56, 76),   (255, 236, 240)),
    Ingredient.VANILLA:    ((198, 178, 228), (78, 50, 110)),
}

_PANEL_BG = (252, 246, 236)


def _draw_star(surface, cx, cy, size, color):
    points = []
    inner  = size * 0.4
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        r     = size if i % 2 == 0 else inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pygame.draw.polygon(surface, color, points)


class PlayerZone:
    def __init__(self, screen: pygame.Surface, side: Side):
        self.screen = screen
        self.side   = side

        w      = screen.get_width()
        h      = screen.get_height()
        half_w = w // 2

        x_offset      = 0 if side == Side.LEFT else half_w
        self._x_offset = x_offset

        # Kitchen
        kitchen_h         = int(h * MAP_KITCHEN_RATIO)
        self.kitchen_rect  = pygame.Rect(x_offset, 0, half_w, kitchen_h)

        # Shop
        shop_h = h - kitchen_h
        shop_y = kitchen_h

        gap_h         = int(shop_h * MAP_CUSTOMER_GAP_RATIO)
        self._gap_top = shop_y
        self._gap_bot = shop_y + gap_h

        # Order display box
        box_w = int(half_w * MAP_INGREDIENT_BOX_RATIO)
        box_x = x_offset if side == Side.LEFT else x_offset + half_w - box_w
        box_y = self._gap_bot
        box_h = shop_h - gap_h
        self.ingredient_box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        # Customer path
        path_w = half_w - box_w
        if side == Side.LEFT:
            controls = PLAYER_1_KEYS
            path_x   = x_offset + box_w
        else:
            controls = PLAYER_2_KEYS
            path_x   = x_offset
        self._path_cx = path_x + path_w // 2
        self._path_x  = path_x
        self._path_w  = path_w

        # Comptoir
        self.comptoir_rect = pygame.Rect(path_x, self._gap_top, path_w, MAP_COMPTOIR_HEIGHT)

        # Customer positions
        _leave_x        = -CUSTOMER_SIZE if side == Side.LEFT else w + CUSTOMER_SIZE
        self._spawn_pos = Position(self._path_cx, h - CUSTOMER_SIZE)
        self._wait_pos  = Position(self._path_cx, self._gap_top + MAP_COMPTOIR_HEIGHT + CUSTOMER_SIZE + 4)
        self._leave_pos = Position(_leave_x,      self._gap_top + MAP_COMPTOIR_HEIGHT + CUSTOMER_SIZE + 4)

        # Player
        color = PLAYER_1_COLOR if side == Side.LEFT else PLAYER_2_COLOR
        self.player = Player(
            Position(self.kitchen_rect.centerx, self.kitchen_rect.centery),
            PLAYER_SIZE, color, self.kitchen_rect, controls,
        )

        # Game state
        self.score         = 0
        self._failed_count = 0
        self.state         = GameState.PLAYING
        self.lost_time     = None

        # Customers
        self._customers = []

        # Interactables
        self.interactables = []
        self.workbench     = None
        self.counter       = None
        self._setup_interactables()
        self.player.available_interactables = self.interactables

        self._shuffle_interval     = 8.0   # seconds between shuffles
        self._shuffle_timer        = self._shuffle_interval
        self._shuffle_min          = 1.5   # current minimum interval (shrinks with score)
        self._shuffle_min_base     = 1.5   # starting minimum
        self._shuffle_min_floor    = 0.3   # hard floor
        self._shuffle_accel        = 0.92

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_interactables(self):
        kl = self.kitchen_rect.left
        kr = self.kitchen_rect.right
        is_right = self.side == Side.RIGHT
        interact = PLAYER_2_INTERACT if is_right else PLAYER_1_INTERACT

        # 8 ingredient Creators in 2 rows of 4, centred horizontally in the kitchen
        self._creators = []
        cols       = 4
        creator_sz = 50
        col_gap    = 105
        grid_w     = (cols - 1) * col_gap + creator_sz
        kcx        = (kl + kr) // 2
        grid_left  = kcx - grid_w // 2 + creator_sz // 2  # x of first column center
        for i, ingr in enumerate(Ingredient):
            col = i % cols
            row = i // cols
            cx = grid_left + col * col_gap
            cy = 80 + row * 100
            c = Creator(Position(cx, cy), creator_sz, ingr, self.player, activate_key=interact)
            self._creators.append(c)
            self.interactables.append(c)

        # Workbench — centred below the ingredient grid
        wb_y = 80 + 1 * 100 + 110  # below second row
        wb = Workbench(Position(kcx, wb_y), 90, self.player, activate_key=interact)
        self.workbench = wb
        self.interactables.append(wb)

        # Deletor — to the right of the workbench
        self.interactables.append(
            Deletor(Position(kcx + 90, wb_y), 50, "Poubelle", interact, self.player)
        )

        # Hoven (four pour cuire les gâteaux) — bottom corner of kitchen (mirrored), not touching wall
        hoven_half = 70  # half of collision_size=140
        margin     = 10  # gap from walls
        hoven_x = (kr - hoven_half - margin) if is_right else (kl + hoven_half + margin)
        hoven_y = self.kitchen_rect.bottom - hoven_half - margin
        hoven   = Hoven(Position(hoven_x, hoven_y), 140, "Four", interact, self.player)
        hoven.score_ref = lambda: self.score
        self.interactables.append(hoven)

        # Counter (delivery) — small cube centered on customer path, near kitchen bottom
        counter_y = self.kitchen_rect.bottom - 40
        ctr = Counter(Position(self._path_cx, counter_y), self.player,
                      collision_w=190, collision_h=80, activate_key=interact)
        ctr.on_delivery = self._handle_delivery
        self.counter = ctr
        self.interactables.append(ctr)

    # ── Shuffle ────────────────────────────────────────────────────────────────

    def _shuffle_creators(self):
        """Mélange aléatoirement les ingrédients entre les Creators."""
        ingredients = [c.ingredient_type for c in self._creators]
        random.shuffle(ingredients)
        for creator, ingr in zip(self._creators, ingredients):
            creator.ingredient_type = ingr
            creator.text = f"Prendre {ingr.value}"

    # ── Delivery callback ──────────────────────────────────────────────────────

    def _handle_delivery(self, result: DeliveryResult):
        from entity.item.cake_item import CakeItem
        customer = self.get_waiting_customer()
        if customer is None or not self.player.has_item():
            return
        item = self.player.current_item
        if not isinstance(item, CakeItem):
            return
        
        if result == DeliveryResult.NOT_COOKED:
            customer.receive_not_cooked()
            customer.receive_item(item)
            customer.state = CustomerState.LEAVING
            self.player.remove_item()
            return

        if item.cake_type == customer.recipe.cake_type:
            customer.serve()
            customer.receive_item(item)
            quality_multiplier = self.counter.get_quality_multiplier()
            tier = self.score // 1000
            difficulty_bonus = 1.0 + tier * 0.5
            final_score = int(customer.recipe.reward * quality_multiplier * difficulty_bonus)
            self.score += final_score
            self.player.remove_item()

    # ── Helpers ────────────────────────────────────────────────────────────────

    def get_waiting_customer(self):
        return next((c for c in self._customers if c.is_waiting), None)

    def has_lost(self) -> bool:
        return self._failed_count >= MAX_FAILED_CUSTOMERS

    # ── Update ─────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        self._update_queue_positions()
        self.player.update(dt)

        # Update shuffle min speed: -0.2s per 1000pts, floor 0.3s until 10000pts then no floor
        tier = self.score // 1000
        raw  = self._shuffle_min_base - tier * 0.2
        if self.score < 10000:
            self._shuffle_min = max(self._shuffle_min_floor, raw)
        else:
            self._shuffle_min = max(0.05, raw)  # near-instant floor above 10000pts

        self._shuffle_timer -= dt
        if self._shuffle_timer <= 0:
            self._shuffle_creators()
            self._shuffle_interval = max(self._shuffle_min,
                                         self._shuffle_interval * self._shuffle_accel)
            self._shuffle_timer = self._shuffle_interval

        # Update interactables that have an update() method
        for interactable in self.interactables:
            if hasattr(interactable, 'update'):
                interactable.update(dt)

        # Sync workbench recipe with current waiting customer
        waiting = self.get_waiting_customer()
        if self.workbench:
            self.workbench.current_recipe = waiting.recipe if waiting else None

        # Update customers, count failures
        already_lost = self.has_lost()
        for customer in self._customers:
            prev_state = customer.state
            # Once the zone has lost, stop patience countdown — send remaining customers away
            if already_lost and customer.state == CustomerState.WAITING:
                customer.state = CustomerState.LEAVING
            customer.update(dt)
            if not already_lost and prev_state == CustomerState.WAITING and customer.state == CustomerState.LEAVING:
                self._failed_count += 1

        self._customers = [c for c in self._customers if not c.is_done]

    def _update_queue_positions(self):
        spacing = CUSTOMER_SIZE * 2 + 4
        in_line = [c for c in self._customers
                   if c.state in (CustomerState.WALKING, CustomerState.QUEUED, CustomerState.WAITING)]
        in_line.sort(key=lambda c: c.position.y)

        for i, customer in enumerate(in_line):
            if i == 0:
                customer.wait_position = Position(self._wait_pos.x, self._wait_pos.y)
                if customer.state == CustomerState.QUEUED and customer._reached(customer.wait_position):
                    customer.state = CustomerState.WAITING
            else:
                prev_y = in_line[i - 1].wait_position.y
                customer.wait_position = Position(self._wait_pos.x, prev_y + spacing)
                if customer.state == CustomerState.WAITING:
                    customer.state = CustomerState.QUEUED

    def try_spawn(self, recipe, difficulty: float = 1.0):
        if len(self._customers) >= CUSTOMER_MAX_COUNT or self.has_lost():
            return
        customer = Customer(
            position       = Position(self._spawn_pos.x, self._spawn_pos.y),
            wait_position  = Position(self._wait_pos.x,  self._wait_pos.y),
            leave_position = Position(self._leave_pos.x, self._leave_pos.y),
            recipe         = recipe,
        )
        customer.patience = recipe.time_limit * difficulty
        self._customers.append(customer)

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self):
        pygame.draw.rect(self.screen, MAP_COMPTOIR_COLOR, self.comptoir_rect)

        waiting = self.get_waiting_customer()
        queued  = next((c for c in self._customers
                        if c.state == CustomerState.QUEUED), None)
        self._draw_order_panel(waiting, queued)

        pygame.draw.rect(self.screen, MAP_SEPARATOR_COLOR,
                         self.ingredient_box_rect, MAP_SEPARATOR_WIDTH)

        for interactable in self.interactables:
            interactable.draw(self.screen)

        for customer in self._customers:
            customer.draw(self.screen)

        self.player.draw(self.screen)

    def _draw_order_panel(self, customer, next_customer=None):
        global _FONT_TITLE, _FONT_BODY, _FONT_LABEL
        if _FONT_TITLE is None:
            try:    _FONT_TITLE = pygame.font.Font(FONT_TITLE_PATH, 24)
            except: _FONT_TITLE = pygame.font.SysFont('georgia', 24, bold=True)  # noqa: E722
        if _FONT_BODY is None:
            try:    _FONT_BODY = pygame.font.Font(FONT_BODY_PATH, 18)
            except: _FONT_BODY = pygame.font.SysFont('arial', 18)  # noqa: E722
        if _FONT_LABEL is None:
            try:    _FONT_LABEL = pygame.font.Font(FONT_BODY_PATH, 13)
            except: _FONT_LABEL = pygame.font.SysFont('arial', 13)  # noqa: E722

        box = self.ingredient_box_rect
        pygame.draw.rect(self.screen, _PANEL_BG, box)

        BAR_H = 22
        HUD_H = 30

        if customer is None:
            msg  = _FONT_BODY.render("En attente d'un client...", True, (175, 148, 115))
            hint = _FONT_LABEL.render("La commande s'affichera ici", True, (200, 178, 150))
            mid_y = (box.top + box.bottom - HUD_H) // 2
            self.screen.blit(msg,  msg.get_rect(center=(box.centerx, mid_y - 12)))
            self.screen.blit(hint, hint.get_rect(center=(box.centerx, mid_y + 14)))
            self._draw_panel_hud(box, HUD_H, next_customer)
            return

        recipe          = customer.recipe
        hdr_bg, hdr_txt = _CAKE_PALETTE.get(recipe.cake_type, ((180, 120, 60), (255, 255, 255)))

        HDR_H    = 46
        hdr_rect = pygame.Rect(box.left, box.top, box.width, HDR_H)
        pygame.draw.rect(self.screen, hdr_bg, hdr_rect)
        title_surf = _FONT_TITLE.render(recipe.cake_type.value, True, hdr_txt)
        self.screen.blit(title_surf, title_surf.get_rect(center=hdr_rect.center))

        # Ingredients already deposited in workbench (count-aware)
        deposited_remaining = list(self.workbench.get_deposited()) if self.workbench else []

        y = box.top + HDR_H + 10
        section_lbl = _FONT_LABEL.render("INGREDIENTS", True, (168, 138, 100))
        self.screen.blit(section_lbl, (box.left + _PAD, y))
        y += section_lbl.get_height() + 7

        BADGE_PX = 9; BADGE_PY = 5; BADGE_GAP = 6; BADGE_RADIUS = 10
        x = box.left + _PAD
        for ingredient in recipe.ingredients:
            bg, fg = _INGREDIENT_PALETTE.get(ingredient, ((210, 210, 210), (50, 50, 50)))
            if ingredient in deposited_remaining:
                done = True
                deposited_remaining.remove(ingredient)
            else:
                done = False
            if not done:
                bg = tuple(max(0, c - 40) for c in bg)

            lbl = _FONT_BODY.render(ingredient.value, True, fg)
            bw  = lbl.get_width()  + BADGE_PX * 2
            bh  = lbl.get_height() + BADGE_PY * 2

            if x + bw > box.right - _PAD:
                x  = box.left + _PAD
                y += bh + BADGE_GAP

            badge_rect = pygame.Rect(x, y, bw, bh)
            pygame.draw.rect(self.screen, bg, badge_rect, border_radius=BADGE_RADIUS)
            self.screen.blit(lbl, (x + BADGE_PX, y + BADGE_PY))

            if done:
                ck = _FONT_LABEL.render("OK", True, (50, 180, 50))
                self.screen.blit(ck, (x + bw - ck.get_width() - 2, y + 2))

            x += bw + BADGE_GAP

        bh_last = _FONT_BODY.get_height() + BADGE_PY * 2
        y += bh_last + 10

        pts_surf = _FONT_BODY.render(f"{recipe.reward} pts", True, (185, 140, 0))
        pts_rect = pts_surf.get_rect(right=box.right - _PAD, y=y)
        self.screen.blit(pts_surf, pts_rect)
        _draw_star(self.screen, pts_rect.left - 14, pts_rect.centery, 10, (215, 168, 0))

        self._draw_panel_hud(box, HUD_H, next_customer)

        bar_bg = pygame.Rect(box.left, box.bottom - BAR_H, box.width, BAR_H)
        pygame.draw.rect(self.screen, (212, 202, 188), bar_bg)

        ratio = customer.patience_ratio
        if ratio >= 0.5:
            t = (1.0 - ratio) * 2
            r, g = int(t * 255), 195
        else:
            t = ratio * 2
            r, g = 255, int(t * 195)

        fill_rect = pygame.Rect(box.left, box.bottom - BAR_H, int(box.width * ratio), BAR_H)
        pygame.draw.rect(self.screen, (r, g, 0), fill_rect)

        time_surf = _FONT_LABEL.render(f"{int(customer.patience)}s", True, (30, 18, 8))
        self.screen.blit(time_surf, time_surf.get_rect(centery=bar_bg.centery, x=box.left + 8))

    def _draw_panel_hud(self, box: pygame.Rect, hud_h: int, next_customer=None):
        """Score + coeurs + prochain gâteau dans une bande en bas du panneau de commande."""
        bar_h   = 22
        hud_y   = box.bottom - bar_h - hud_h
        hud_rect = pygame.Rect(box.left, hud_y, box.width, hud_h)
        pygame.draw.rect(self.screen, (238, 224, 200), hud_rect)

        # Prochain gâteau (au-dessus du HUD)
        if next_customer is not None:
            NEXT_H = 22
            next_rect = pygame.Rect(box.left, hud_y - NEXT_H, box.width, NEXT_H)
            pygame.draw.rect(self.screen, (228, 212, 185), next_rect)
            lbl  = _FONT_LABEL.render("Prochain : ", True, (140, 105, 65))
            name = _FONT_LABEL.render(next_customer.recipe.cake_type.value, True, (80, 50, 20))
            x = box.left + _PAD
            self.screen.blit(lbl,  lbl.get_rect(centery=next_rect.centery, left=x))
            self.screen.blit(name, name.get_rect(centery=next_rect.centery, left=x + lbl.get_width()))

        # Score (left-aligned)
        score_surf = _FONT_LABEL.render(f"Score : {self.score} pts", True, (80, 50, 20))
        self.screen.blit(score_surf, score_surf.get_rect(centery=hud_rect.centery, left=box.left + _PAD))

        # Heart icons (right-aligned, drawn right to left)
        lives = MAX_FAILED_CUSTOMERS - self._failed_count
        hx    = box.right - _PAD
        hy    = hud_rect.centery
        for i in range(MAX_FAILED_CUSTOMERS - 1, -1, -1):
            color = (220, 50, 80) if i < lives else (175, 145, 135)
            hx -= 18
            pygame.draw.circle(self.screen, color, (hx + 4,  hy - 2), 4)
            pygame.draw.circle(self.screen, color, (hx + 11, hy - 2), 4)
            pygame.draw.polygon(self.screen, color,
                                [(hx, hy), (hx + 7, hy + 8), (hx + 15, hy)])
            hx -= 5

    # ── Event dispatch ────────────────────────────────────────────────────────

    def handle_keydown(self, key):
        for interactable in self.interactables:
            if hasattr(interactable, "handle_keydown"):
                interactable.handle_keydown(key)

    def handle_movement(self, keys, dt: float = 1 / 60):
        self.player.handle_movement(keys, dt)

    def handle_events(self):
        for interactable in self.interactables:
            if hasattr(interactable, "handle_events") and callable(getattr(interactable, "handle_events")):
                interactable.handle_events()
        self.player.handle_events()
