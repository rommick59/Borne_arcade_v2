import pygame
import os
import config

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Age Of War")

# ---- ASSETS ----

ASSETS_PATH = r"assets/img"

terrain_img = pygame.image.load(os.path.join(ASSETS_PATH, "terrain.png")).convert()
terrain_img = pygame.transform.scale(terrain_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

tank_blue_img = pygame.image.load(os.path.join(ASSETS_PATH, "tankbleu.png")).convert_alpha()
tank_red_img = pygame.image.load(os.path.join(ASSETS_PATH, "tankrouge.png")).convert_alpha()

soldier_blue_img = pygame.image.load(os.path.join(ASSETS_PATH, "unitebleu.png")).convert_alpha()
soldier_red_img = pygame.image.load(os.path.join(ASSETS_PATH, "uniterouge.png")).convert_alpha()

UNIT_SIZE = (40, 40)

tank_blue_img = pygame.transform.scale(tank_blue_img, UNIT_SIZE)
tank_red_img = pygame.transform.scale(tank_red_img, UNIT_SIZE)
soldier_blue_img = pygame.transform.scale(soldier_blue_img, UNIT_SIZE)
soldier_red_img = pygame.transform.scale(soldier_red_img, UNIT_SIZE)

# --- Initialisation écran ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AgeOfWar 2 Joueurs - Flèches")

FPS = 60
clock = pygame.time.Clock()

# --- Police ---
FONT = pygame.font.SysFont("Arial", 24)

def draw_text(text, x, y, color=(255,255,255)):
    surface = FONT.render(text, True, color)
    screen.blit(surface, (x, y))


UNIT_COSTS = {"soldier": 50, "tank": 100}
LINES = ["top", "middle", "bottom"]
LINES_Y = {"top": 150, "middle": 300, "bottom": 450}


# --- Etats joueurs ---
players = {
    "left": {
        "gold": 100,
        "base_hp": 100,
        "units": {line: [] for line in LINES}
    },
    "right": {
        "gold": 100,
        "base_hp": 100,
        "units": {line: [] for line in LINES}
    }
}

last_spawn_left = 0
last_spawn_right = 0


# --- Flèches de sélection ---
arrows = {"left": 1, "right": 1}  # index ligne sélectionnée, 0=top,1=middle,2=bottom

# --- Classe unité ---
class Unit(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, speed, hp, damage, reward, attack_cooldown, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.pos_x = float(x)

        self.direction = direction
        self.speed = speed

        self.hp = hp
        self.max_hp = hp

        self.damage = damage
        self.reward = reward

        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0

        self.target = None

    def update(self, enemy_units, ally_units):
        self.target = None
    # Chercher une unité ennemie à portée
        for e in enemy_units:
            if abs(self.pos_x - e.pos_x) <= 24:
                self.target = e
                break

        current_time = pygame.time.get_ticks()
        if self.target:
            # Attaque selon cooldown
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.target.hp -= self.damage
                self.last_attack_time = current_time
        else:
            # Vérifier si une unité alliée bloque la route
            blocked = False
            for ally in ally_units:
                if ally == self:
                    continue
                # Même ligne et proche devant
                if (self.direction == 1 and 0 < ally.pos_x - self.pos_x <= 24) or \
                   (self.direction == -1 and 0 < self.pos_x - ally.pos_x <= 24):
                    blocked = True
                    break
            if not blocked:
                self.pos_x += self.speed * self.direction
                self.rect.x = int(self.pos_x)

    def draw_hp_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 4
        fill = (self.hp / self.max_hp) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 6, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 6, fill, bar_height)
        pygame.draw.rect(surface, (255,0,0), fill_rect)
        pygame.draw.rect(surface, (255,255,255), outline_rect, 1)

# --- Création unité sur ligne sélectionnée ---def spawn_unit(player_side, unit_type):
def spawn_unit(player_side, unit_type):

    line = LINES[arrows[player_side]]
    cost = UNIT_COSTS[unit_type]

    p = players[player_side]

    if p["gold"] >= cost:

        p["gold"] -= cost

        direction = 1 if player_side == "left" else -1
        start_x = 50 if player_side == "left" else SCREEN_WIDTH - 50
        y = LINES_Y[line]

        if unit_type == "soldier":

            image = soldier_blue_img if player_side == "left" else soldier_red_img

            unit = Unit(
                start_x, y,
                direction,
                1,
                50,
                10,
                20,
                1000,
                image
            )

        else:

            image = tank_blue_img if player_side == "left" else tank_red_img

            unit = Unit(
                start_x, y,
                direction,
                0.5,
                50,
                25,
                50,
                2000,
                image
            )

        p["units"][line].append(unit)

def move_arrow(player_side, direction):
    """
    Déplace la flèche du joueur entre les lignes
    direction = -1 (haut) ou 1 (bas)
    """

    arrows[player_side] += direction

    # empêcher de sortir des lignes
    if arrows[player_side] < 0:
        arrows[player_side] = 0

    if arrows[player_side] > len(LINES) - 1:
        arrows[player_side] = len(LINES) - 1
        
# --- Mise à jour unités/combat ---
def update_units():
    for line in LINES:
        left_units = players["left"]["units"][line]
        right_units = players["right"]["units"][line]

        # Update avec combat et blocage
        for unit in left_units[:]:
            unit.update(right_units, left_units)
        for unit in right_units[:]:
            unit.update(left_units, right_units)

        # Mort et récompense
        for side_name, side, enemy_units in [("left", left_units, right_units), ("right", right_units, left_units)]:
            for unit in side[:]:
                if unit.hp <= 0:
                    enemy_player = "right" if side_name=="left" else "left"
                    players[enemy_player]["gold"] += unit.reward
                    side.remove(unit)

        # Collision base
        for unit in left_units[:]:
            if unit.pos_x >= SCREEN_WIDTH - 50:
                dmg = 5 if unit.speed >= 1 else 10
                players["right"]["base_hp"] -= dmg
                left_units.remove(unit)
        for unit in right_units[:]:
            if unit.pos_x <= 50:
                dmg = 5 if unit.speed >= 1 else 10
                players["left"]["base_hp"] -= dmg
                right_units.remove(unit)

# --- Dessin UI ---
def draw_ui():
    pygame.draw.rect(screen, (255,0,0), (20, 20, players["left"]["base_hp"], 20))
    pygame.draw.rect(screen, (255,0,0), (SCREEN_WIDTH-220, 20, players["right"]["base_hp"], 20))
    draw_text(f"G: {players['left']['gold']}", 20, 50)
    draw_text(f"G: {players['right']['gold']}", SCREEN_WIDTH-120, 50)

# --- Dessin unités ---
def draw_units():
    for player in players.values():
        for line_units in player["units"].values():
            for unit in line_units:
                screen.blit(unit.image, unit.rect)
                unit.draw_hp_bar(screen)

# --- Dessin flèches de sélection ---
def draw_arrows():
    arrow_size = 20
    for side, idx in arrows.items():
        x = 30 if side=="left" else SCREEN_WIDTH - 50
        y = LINES_Y[LINES[idx]]
        pygame.draw.polygon(screen, (255,255,0),
                            [(x, y), (x, y+arrow_size), (x+arrow_size, y+arrow_size//2)]) if side=="left" else \
                            pygame.draw.polygon(screen, (255,255,0),
                            [(x, y), (x, y+arrow_size), (x-arrow_size, y+arrow_size//2)])

# --- Boucle principale ---
def main():
    global last_spawn_left, last_spawn_right
    run = True
    gold_timer = 0
    passive_gold_rate = 10

    while run:
        dt = clock.tick(FPS)
        screen.blit(terrain_img, (0,0))

        # --- Événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # ---- Joueur gauche ----
        if keys[pygame.K_f] and current_time - last_spawn_left > config.SPAWN_DELAY:
            spawn_unit("left", "soldier")
            last_spawn_left = current_time

        if keys[pygame.K_g] and current_time - last_spawn_left > config.SPAWN_DELAY:
            spawn_unit("left", "tank")
            last_spawn_left = current_time


        # ---- Joueur droite ----
        if keys[pygame.K_h] and current_time - last_spawn_right > config.SPAWN_DELAY:
            spawn_unit("right", "soldier")
            last_spawn_right = current_time

        if keys[pygame.K_r] and current_time - last_spawn_right > config.SPAWN_DELAY:
            spawn_unit("right", "tank")
            last_spawn_right = current_time

        # déplacement flèche joueur gauche
        
        if keys[pygame.K_a]:
            move_arrow("left", -1)

        if keys[pygame.K_z]:
            move_arrow("left", 1)


        # déplacement flèche joueur droite
        if keys[pygame.K_UP]:
            move_arrow("right", -1)

        if keys[pygame.K_DOWN]:
            move_arrow("right", 1)

        # --- Argent passif ---
        gold_timer += dt
        if gold_timer >= 1000:
            players["left"]["gold"] += passive_gold_rate
            players["right"]["gold"] += passive_gold_rate
            gold_timer = 0

        # --- Mise à jour ---
        update_units()

        # --- Dessin ---
        draw_ui()
        draw_units()
        draw_arrows()
        pygame.display.flip()

        # --- Vérification victoire ---
        if players["left"]["base_hp"] <= 0:
            print("Right wins!")
            run = False
        if players["right"]["base_hp"] <= 0:
            print("Left wins!")
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()