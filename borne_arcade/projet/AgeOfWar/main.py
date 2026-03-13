import pygame
from game import main as start_game  # importe la fonction main() de game.py

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AgeOfWar 2 Joueurs - Menu")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 36)

def draw_text(text, x, y, color=(255,255,255)):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, (x, y))

# --- Menu principal ---
def main_menu():
    run = True
    selected = 0
    options = ["Jouer", "Instructions", "Quitter"]

    while run:
        screen.fill((0,0,0))
        # Affichage des options
        for i, option in enumerate(options):
            color = (255,255,0) if i == selected else (255,255,255)
            draw_text(option, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50 + i*50, color)

        pygame.display.flip()
        clock.tick(60)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Jouer":
                        start_game()
                    elif options[selected] == "Instructions":
                        show_instructions()
                    elif options[selected] == "Quitter":
                        run = False

# --- Instructions ---
def show_instructions():
    running = True
    small_font = pygame.font.SysFont("Arial", 24)

    while running:
        screen.fill((0,0,0))
        y = 50
        lines = [
            "Placement des unités sur 3 lignes (Top / Middle / Bottom) :",
            "",
            "Joueur GAUCHE :",
            "Soldier -> Top: A | Middle: Z | Bottom: X",
            "Tank    -> Top: S | Middle: D | Bottom: F",
            "",
            "Joueur DROITE :",
            "Soldier -> Top: K | Middle: L | Bottom: ;",
            "Tank    -> Top: O | Middle: P | Bottom: [",
            "",
            "Objectif : Détruire la base ennemie",
            "Argent passif : +10/sec",
            "",
            "Appuyez sur ESC pour revenir au menu"
        ]
        for line in lines:
            text_surface = small_font.render(line, True, (255,255,255))
            screen.blit(text_surface, (50, y))
            y += 30

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

if __name__ == "__main__":
    main_menu()
    pygame.quit()