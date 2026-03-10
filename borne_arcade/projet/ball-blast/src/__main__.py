from constantes import SCREEN_WIDTH, SCREEN_HEIGHT, FPS_ENABLED, FPS_LOG_FILE
from menu import Menu
from game import Game

import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Set up the display
pygame.display.set_caption("Ball Blast")
# Open window in fullscreen using the configured resolution
# Use DOUBLEBUF and HWSURFACE for better blit performance in fullscreen
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
# Game loop
running = True
clock = pygame.time.Clock()
frame_counter = 0

# sound1 = pygame.mixer.Sound("./assets/sound/bip.mp3")
# sound2 = pygame.mixer.Sound("./assets/sound/explosion.mp3")
# sound3 = pygame.mixer.Sound("./assets/sound/win.mp3")
# sound4 = pygame.mixer.Sound("./assets/sound/pop.mp3")

menu: Menu = Menu(screen)
game: Game = None

# Gestion des états
gameState = False
pause = False
newGame = False
gameOver = False
credits = False

playMusic = True

pygame.mixer.music.load("assets/sound/menu.mp3")
pygame.mixer.music.play()

while running:

    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break

        # Normalize events: if the device sends a unicode character (e.g. 'r','t','y')
        # prefer converting that to the corresponding pygame key constant so
        # downstream code checking `event.key` works reliably. Also update
        # input_helper so `is_pressed()` reflects the event state.
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            uni = getattr(event, 'unicode', '')
            mapped = event.key
            if uni:
                try:
                    mapped = pygame.key.key_code(uni)
                    event.key = mapped
                except Exception:
                    mapped = event.key
            # update input helper state
            try:
                from input_helper import on_keydown, on_keyup
                if event.type == pygame.KEYDOWN:
                    on_keydown(mapped)
                else:
                    on_keyup(mapped)
            except Exception:
                pass

    if credits:
        credits = menu.showCredits()
    elif not gameState:
        gameState, newGame, credits = menu.showMenu(events, pause)
        if gameState and newGame:
            game = Game(screen, clock)
            newGame = False

        # Si on passe du menu au jeu
        if gameState:
            playMusic = True
    else:
        gameOver, pause = game.showGame()
        
        if playMusic:
            pygame.mixer.music.load("./assets/sound/music" + str(random.randint(1, 3)) + ".mp3")
            pygame.mixer.music.play(loops=-1)
            playMusic = False

        if gameOver:
            gameState, gameOver = game.registerScore()
        
        # Si on passe du jeu au menu
        if pause:
            gameState = False
            pygame.mixer.music.load("assets/sound/menu.mp3")
            pygame.mixer.music.play()

    pygame.display.update()
    clock.tick(30)
    # simple FPS logging every ~30 frames (once/second)
    frame_counter += 1
    if FPS_ENABLED and frame_counter % 30 == 0:
        try:
            import os
            os.makedirs(os.path.dirname(FPS_LOG_FILE), exist_ok=True)
            with open(FPS_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"{pygame.time.get_ticks()}\t{clock.get_fps():.1f}\n")
        except Exception:
            pass

pygame.quit()
exit(0)
