import os
import sys
import random
import time
import math

try:
    import pygame
except Exception as exc:
    print("Pygame introuvable. Installez python3-pygame.")
    print(exc)
    sys.exit(1)

WIDTH = 1280
HEIGHT = 1024
FPS = 60

SHIP_W = 60
SHIP_H = 70
SHIP_SPEED = 10
SHIP_ACCEL = 0.6
SHIP_DRAG = 0.85

ASTEROID_MIN = 18
ASTEROID_MAX = 52
ASTEROID_SPEED_MIN = 3.0
ASTEROID_SPEED_MAX = 8.0
SPAWN_MS = 420

BG_COLOR = (8, 10, 22)
NEBULA_COLOR_1 = (30, 40, 90)
NEBULA_COLOR_2 = (18, 60, 120)
STAR_COLORS = [(200, 200, 255), (180, 220, 255), (255, 220, 180)]
SHIP_COLOR = (60, 200, 255)
SHIP_ACCENT = (255, 240, 120)
ASTEROID_COLOR = (140, 140, 160)
TEXT_COLOR = (240, 240, 240)
WARN_COLOR = (255, 140, 120)


def clamp(value, low, high):
    return max(low, min(high, value))


def reset_state(width, height):
    return {
        "x": width // 2,
        "y": height - 140,
        "vx": 0.0,
        "asteroids": [],
        "particles": [],
        "score": 0,
        "lives": 3,
        "alive": True,
        "start": time.time(),
        "hit_flash": 0.0,
    }


def make_starfield(width, height):
    layers = []
    for count, speed, radius in [(60, 0.8, 1), (40, 1.4, 2), (24, 2.0, 3)]:
        stars = []
        for _ in range(count):
            stars.append({
                "x": random.randint(0, width),
                "y": random.randint(0, height),
                "speed": speed + random.random() * 0.6,
                "r": radius,
                "color": random.choice(STAR_COLORS),
            })
        layers.append(stars)
    return layers


def spawn_asteroid(width):
    radius = random.randint(ASTEROID_MIN, ASTEROID_MAX)
    x = random.randint(radius, width - radius)
    y = -radius * 2
    speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
    drift = random.uniform(-0.5, 0.5)
    return {
        "x": float(x),
        "y": float(y),
        "r": radius,
        "speed": speed,
        "drift": drift,
        "spin": random.uniform(-1.5, 1.5),
        "angle": random.random() * 360.0,
        "craters": [
            (random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4), random.uniform(0.15, 0.35))
            for _ in range(random.randint(2, 5))
        ],
    }


def add_thruster_particles(state):
    for _ in range(3):
        state["particles"].append({
            "x": state["x"] + random.uniform(-8, 8),
            "y": state["y"] + SHIP_H * 0.45,
            "vx": random.uniform(-0.6, 0.6),
            "vy": random.uniform(2.5, 5.0),
            "life": random.uniform(0.3, 0.6),
        })


def add_explosion_particles(state, x, y):
    for _ in range(40):
        angle = random.random() * 6.283
        speed = random.uniform(2.0, 6.0)
        state["particles"].append({
            "x": x,
            "y": y,
            "vx": speed * math.cos(angle),
            "vy": speed * math.sin(angle),
            "life": random.uniform(0.6, 1.1),
        })


def draw_ship(screen, x, y, invuln=False):
    points = [
        (x, y - SHIP_H * 0.5),
        (x - SHIP_W * 0.45, y + SHIP_H * 0.4),
        (x, y + SHIP_H * 0.15),
        (x + SHIP_W * 0.45, y + SHIP_H * 0.4),
    ]
    color = SHIP_COLOR if not invuln else (100, 255, 220)
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, (20, 30, 50), points, 2)
    pygame.draw.circle(screen, SHIP_ACCENT, (int(x), int(y - SHIP_H * 0.15)), 6)


def draw_asteroid(screen, asteroid):
    pygame.draw.circle(screen, ASTEROID_COLOR, (int(asteroid["x"]), int(asteroid["y"])), asteroid["r"])
    for cx, cy, cr in asteroid["craters"]:
        pygame.draw.circle(
            screen,
            (110, 110, 130),
            (int(asteroid["x"] + cx * asteroid["r"]), int(asteroid["y"] + cy * asteroid["r"])),
            int(asteroid["r"] * cr),
            1,
        )


def draw_nebula(screen, width, height, t):
    for i in range(6):
        r = 120 + i * 40
        x = int(width * 0.2 + (i * 60) + 40 * math.sin(t + i))
        y = int(height * 0.2 + (i * 30) + 30 * math.cos(t * 0.8 + i))
        color = NEBULA_COLOR_1 if i % 2 == 0 else NEBULA_COLOR_2
        surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, 40), (r, r), r)
        screen.blit(surface, (x - r, y - r))


def main():
    pygame.init()
    global WIDTH, HEIGHT
    info = pygame.display.Info()
    WIDTH = int(os.getenv("ARCADE_WIDTH", info.current_w or WIDTH))
    HEIGHT = int(os.getenv("ARCADE_HEIGHT", info.current_h or HEIGHT))
    fullscreen = os.getenv("ARCADE_FULLSCREEN", "1") == "1"
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("NebulaRun")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 22)
    big = pygame.font.SysFont("Arial", 48)

    state = reset_state(WIDTH, HEIGHT)
    star_layers = make_starfield(WIDTH, HEIGHT)
    pygame.time.set_timer(pygame.USEREVENT + 1, SPAWN_MS)

    running = True
    t = 0.0
    while running:
        dt = clock.tick(FPS) / 1000.0
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Résolution des touches remappées sur la borne: privilégier
                # event.unicode quand disponible pour retrouver le keycode
                keycode = event.key
                uni = getattr(event, 'unicode', '')
                if uni:
                    try:
                        keycode = pygame.key.key_code(uni)
                    except Exception:
                        pass

                # Debug: log les événements de touches non-bloquants
                try:
                    with open("nebularun_keydebug.log", "a", encoding="utf-8") as dbg:
                        dbg.write(f"event.key={event.key} unicode={uni!r} resolved={keycode}\n")
                except Exception:
                    pass

                if keycode in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                if not state["alive"] and keycode == pygame.K_r:
                    state = reset_state(WIDTH, HEIGHT)
            elif event.type == pygame.USEREVENT + 1 and state["alive"]:
                state["asteroids"].append(spawn_asteroid(WIDTH))

        keys = pygame.key.get_pressed()
        if state["alive"]:
            if keys[pygame.K_LEFT]:
                state["vx"] -= SHIP_ACCEL
            if keys[pygame.K_RIGHT]:
                state["vx"] += SHIP_ACCEL
            state["vx"] *= SHIP_DRAG
            state["vx"] = clamp(state["vx"], -SHIP_SPEED, SHIP_SPEED)
            state["x"] += state["vx"]
            state["x"] = clamp(state["x"], SHIP_W * 0.6, WIDTH - SHIP_W * 0.6)
            add_thruster_particles(state)

        if state["alive"]:
            for asteroid in state["asteroids"]:
                asteroid["y"] += asteroid["speed"]
                asteroid["x"] += asteroid["drift"]
                asteroid["angle"] += asteroid["spin"]
            state["asteroids"] = [a for a in state["asteroids"] if a["y"] < HEIGHT + 120]

            ship_radius = SHIP_W * 0.35
            for asteroid in state["asteroids"]:
                dx = asteroid["x"] - state["x"]
                dy = asteroid["y"] - state["y"]
                if dx * dx + dy * dy < (asteroid["r"] + ship_radius) ** 2:
                    state["lives"] -= 1
                    state["hit_flash"] = 0.6
                    if state["lives"] <= 0:
                        state["alive"] = False
                    else:
                        state["asteroids"].remove(asteroid)
                    break

            state["score"] = int(time.time() - state["start"]) * 10

        for star_layer in star_layers:
            for star in star_layer:
                star["y"] += star["speed"]
                if star["y"] > HEIGHT + 10:
                    star["y"] = -10
                    star["x"] = random.randint(0, WIDTH)

        for particle in state["particles"]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= dt
        state["particles"] = [p for p in state["particles"] if p["life"] > 0]

        if state["hit_flash"] > 0:
            state["hit_flash"] = max(0.0, state["hit_flash"] - dt)

        screen.fill(BG_COLOR)
        draw_nebula(screen, WIDTH, HEIGHT, t)

        for star_layer in star_layers:
            for star in star_layer:
                pygame.draw.circle(screen, star["color"], (int(star["x"]), int(star["y"])), star["r"])

        for particle in state["particles"]:
            alpha = int(255 * (particle["life"] / 0.6))
            surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 170, 80, alpha), (3, 3), 3)
            screen.blit(surf, (particle["x"], particle["y"]))

        for asteroid in state["asteroids"]:
            draw_asteroid(screen, asteroid)

        draw_ship(screen, state["x"], state["y"], invuln=state["hit_flash"] > 0)

        score_text = font.render(f"Score: {state['score']}", True, TEXT_COLOR)
        lives_text = font.render(f"Lives: {state['lives']}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 18))
        screen.blit(lives_text, (20, 44))

        hint = font.render("Fleches: gauche/droite | Q/Echap: quitter | R: rejouer", True, TEXT_COLOR)
        screen.blit(hint, (20, HEIGHT - 36))

        if state["hit_flash"] > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(flash, (*WARN_COLOR, 60), flash.get_rect())
            screen.blit(flash, (0, 0))

        if not state["alive"]:
            msg = big.render("GAME OVER", True, TEXT_COLOR)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 70))
            sub = font.render("Appuie sur R pour rejouer", True, TEXT_COLOR)
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
