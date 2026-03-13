import pygame
import sys
from core.screen import Screen
from core.constants import (
    MENU_BG_COLOR, MENU_TITLE_COLOR, MENU_TITLE_FONT_SIZE, MENU_TITLE_Y_OFFSET,
    MENU_BTN_COLOR, MENU_BTN_HOVER_COLOR, MENU_BTN_TEXT_COLOR, MENU_BTN_SHADOW_COLOR,
    MENU_BTN_FONT_SIZE, MENU_BTN_WIDTH, MENU_BTN_HEIGHT,
    MENU_BTN_BORDER_RADIUS, MENU_BTN_SHADOW_OFFSET, MENU_BTN_SPACING,
)
from core.enums import MenuButton

_MENU_ORDER = [MenuButton.JOUER, MenuButton.SCORE, MenuButton.QUITTER]

# J1 arcade controls for menu navigation
_KEY_UP      = pygame.K_UP
_KEY_DOWN    = pygame.K_DOWN
_KEY_CONFIRM = (pygame.K_1, pygame.K_4, pygame.K_RETURN)


class Menu:
    def __init__(self):
        self.screen      = Screen().screen
        self.running     = True
        self.next_screen = None
        self.buttons     = {}
        self._selected   = 0  # index into _MENU_ORDER

    def _confirm(self, spec: MenuButton):
        if spec == MenuButton.QUITTER:
            pygame.quit(); sys.exit()
        self.next_screen = spec
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_3):
                    pygame.quit(); sys.exit()
                elif event.key == _KEY_UP:
                    self._selected = (self._selected - 1) % len(_MENU_ORDER)
                elif event.key == _KEY_DOWN:
                    self._selected = (self._selected + 1) % len(_MENU_ORDER)
                elif event.key in _KEY_CONFIRM:
                    self._confirm(_MENU_ORDER[self._selected])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for spec, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self._confirm(spec)

    def draw_button(self, spec: MenuButton, x: int, y: int, width: int, height: int):
        rect      = pygame.Rect(x, y, width, height)
        self.buttons[spec] = rect
        is_hovered  = rect.collidepoint(pygame.mouse.get_pos())
        is_selected = _MENU_ORDER[self._selected] == spec

        shadow_rect = rect.move(MENU_BTN_SHADOW_OFFSET, MENU_BTN_SHADOW_OFFSET)
        pygame.draw.rect(self.screen, MENU_BTN_SHADOW_COLOR, shadow_rect, border_radius=MENU_BTN_BORDER_RADIUS)

        color = MENU_BTN_HOVER_COLOR if (is_hovered or is_selected) else MENU_BTN_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=MENU_BTN_BORDER_RADIUS)

        if is_selected:
            pygame.draw.rect(self.screen, (255, 200, 50), rect, 3, border_radius=MENU_BTN_BORDER_RADIUS)

        font  = pygame.font.SysFont(None, MENU_BTN_FONT_SIZE)
        label = font.render(spec.value, True, MENU_BTN_TEXT_COLOR)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(MENU_BG_COLOR)
        center_x = self.screen.get_width() // 2
        title_y  = self.screen.get_height() // 2 - MENU_TITLE_Y_OFFSET

        font_title = pygame.font.SysFont(None, MENU_TITLE_FONT_SIZE)
        title      = font_title.render("CakeCraft", True, MENU_TITLE_COLOR)
        self.screen.blit(title, title.get_rect(center=(center_x, title_y)))

        btn_x = center_x - MENU_BTN_WIDTH // 2
        first_y = self.screen.get_height() // 2 - 20
        self.draw_button(MenuButton.JOUER,   btn_x, first_y,                          MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        self.draw_button(MenuButton.SCORE,   btn_x, first_y + MENU_BTN_SPACING,       MENU_BTN_WIDTH, MENU_BTN_HEIGHT)
        self.draw_button(MenuButton.QUITTER, btn_x, first_y + MENU_BTN_SPACING * 2,  MENU_BTN_WIDTH, MENU_BTN_HEIGHT)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
        return self.next_screen
