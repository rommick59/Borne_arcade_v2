from constantes import SCREEN_WIDTH, SCREEN_HEIGHT
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
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# Game loop
running = True
clock = pygame.time.Clock()

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
        # downstream code checking `event.key` works reliably.
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            uni = getattr(event, 'unicode', '')
            if uni:
                try:
                    mapped = pygame.key.key_code(uni)
                    # pygame Event attributes are mutable - override key so
                    # existing checks on event.key behave as expected
                    event.key = mapped
                except Exception:
                    pass

    if credits:
        credits = menu.showCredits()
    elif not gameState:
        gameState, newGame, credits = menu.showMenu(events, pause)
        if gameState and newGame:
            game = Game(screen)
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
    clock.tick(40)

pygame.quit()
exit(0)
