#!/usr/bin/env python3.11
import pygame
import sys
import os
# Ensure src/ is always on the path (robustness when run from any directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.menu import Menu
from game.run import Game
from game.player_select import PlayerSelectScreen
from core.enums import MenuButton

def main():
    pygame.init()

    while True:
        result = Menu().run()

        if result == MenuButton.JOUER:
            mode = PlayerSelectScreen().run()
            if mode == PlayerSelectScreen.TWO_PLAYERS:
                Game().run()
            elif mode == PlayerSelectScreen.P1_VS_BOT:
                Game(bot_right=True).run()
            elif mode == PlayerSelectScreen.BOT_VS_P2:
                Game(bot_left=True).run()
        elif result == MenuButton.SCORE:
            from game.scoreboard_screen import ScoreboardScreen
            ScoreboardScreen().run()
        else:
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
