import pygame
import sys
from core.screen import Screen
import game.scoreboard as sb

_DARK_BG = (28, 18, 10)
_GOLD    = (255, 200, 50)
_WHITE   = (255, 248, 240)
_GREY    = (120, 110, 100)
_TAB_ON  = (80, 60, 20)
_TAB_OFF = (40, 30, 10)

_TAB_SOLO = 0
_TAB_VS   = 1


class ScoreboardScreen:
    def __init__(self):
        self.screen     = Screen().screen
        self.running    = True
        self.tab        = _TAB_SOLO
        self._back_rect = None

        self._font_title = pygame.font.SysFont("georgia", 48, bold=True)
        self._font_body  = pygame.font.SysFont("monospace", 24)
        self._font_small = pygame.font.SysFont("monospace", 18)

    # ── Input ────────────────────────────────────────────────────────────────

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_1, pygame.K_4, pygame.K_3):
                    self.running = False
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_TAB):
                    self.tab = _TAB_VS if self.tab == _TAB_SOLO else _TAB_SOLO
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                w = self.screen.get_width()
                if pygame.Rect(w // 4 - 80, 90, 160, 40).collidepoint(event.pos):
                    self.tab = _TAB_SOLO
                elif pygame.Rect(3 * w // 4 - 80, 90, 160, 40).collidepoint(event.pos):
                    self.tab = _TAB_VS
                elif self._back_rect and self._back_rect.collidepoint(event.pos):
                    self.running = False

    # ── Draw helpers ─────────────────────────────────────────────────────────

    def _draw_tab(self, label: str, cx: int, active: bool):
        rect  = pygame.Rect(cx - 80, 90, 160, 40)
        pygame.draw.rect(self.screen, _TAB_ON if active else _TAB_OFF, rect, border_radius=8)
        pygame.draw.rect(self.screen, _GOLD if active else _GREY, rect, 2, border_radius=8)
        surf = self._font_small.render(label, True, _GOLD if active else _GREY)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def _cell(self, text: str, x: int, y: int, color, font=None, align="left"):
        f    = font or self._font_body
        surf = f.render(str(text), True, color)
        if align == "right":
            self.screen.blit(surf, surf.get_rect(right=x, top=y))
        else:
            self.screen.blit(surf, (x, y))

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(_DARK_BG)

        title = self._font_title.render("Meilleurs scores", True, _GOLD)
        self.screen.blit(title, title.get_rect(centerx=w // 2, top=20))

        self._draw_tab("Classement", w // 4,     self.tab == _TAB_SOLO)
        self._draw_tab("1 vs 1",    3 * w // 4, self.tab == _TAB_VS)

        pygame.draw.line(self.screen, (80, 60, 40), (40, 145), (w - 40, 145), 2)

        if self.tab == _TAB_SOLO:
            self._draw_solo(w, h)
        else:
            self._draw_vs(w, h)

        back_surf       = self._font_small.render("[ ECHAP ] Retour", True, _GREY)
        self._back_rect = back_surf.get_rect(centerx=w // 2, bottom=h - 20)
        self.screen.blit(back_surf, self._back_rect)

        pygame.display.flip()

    def _draw_solo(self, w: int, h: int):
        entries = sb.get_solo()
        start_y = 165
        row_h   = 38

        # Column X positions
        cx = w // 2
        col_rank  = cx - 260
        col_name  = cx - 200
        col_score = cx + 200

        # Header
        self._cell("#",     col_rank,  start_y, _GOLD, self._font_small)
        self._cell("Nom",   col_name,  start_y, _GOLD, self._font_small)
        self._cell("Score", col_score, start_y, _GOLD, self._font_small, align="right")
        pygame.draw.line(self.screen, (80, 60, 40),
                         (col_rank, start_y + 22), (col_score, start_y + 22), 1)

        for i, entry in enumerate(entries):
            color = _GOLD if i == 0 else _WHITE
            y     = start_y + (i + 1) * row_h
            self._cell(f"{i+1}",              col_rank,  y, color)
            self._cell(entry["name"],          col_name,  y, color)
            self._cell(f"{entry['score']} pts", col_score, y, color, align="right")

        if not entries:
            empty = self._font_small.render("Aucun score enregistre", True, _GREY)
            self.screen.blit(empty, empty.get_rect(centerx=w // 2, top=start_y + row_h))

    def _draw_vs(self, w: int, h: int):
        entries = sb.get_vs()
        start_y = 165
        row_h   = 38

        cx = w // 2
        col_rank   = cx - 360
        col_name1  = cx - 290
        col_score1 = cx - 80
        col_name2  = cx - 30
        col_score2 = cx + 180
        col_total  = cx + 360

        # Header
        for text, x, align in [
            ("#",        col_rank,   "left"),
            ("J1",       col_name1,  "left"),
            ("pts",      col_score1, "right"),
            ("J2",       col_name2,  "left"),
            ("pts",      col_score2, "right"),
            ("Total",    col_total,  "right"),
        ]:
            self._cell(text, x, start_y, _GOLD, self._font_small, align=align)
        pygame.draw.line(self.screen, (80, 60, 40),
                         (col_rank, start_y + 22), (col_total, start_y + 22), 1)

        total_games = len(entries)
        for i, entry in enumerate(reversed(entries)):  # most recent first
            color      = _WHITE
            y          = start_y + (i + 1) * row_h
            game_num   = total_games - i  # most recent = highest number
            self._cell(str(game_num),               col_rank,   y, color)
            self._cell(entry["name1"],            col_name1,  y, color)
            self._cell(f"{entry['score1']}",      col_score1, y, color, align="right")
            self._cell(entry["name2"],            col_name2,  y, color)
            self._cell(f"{entry['score2']}",      col_score2, y, color, align="right")
            self._cell(f"{entry['total']} pts",   col_total,  y, color, align="right")

        if not entries:
            empty = self._font_small.render("Aucun score enregistre", True, _GREY)
            self.screen.blit(empty, empty.get_rect(centerx=w // 2, top=start_y + row_h))

    # ── Loop ─────────────────────────────────────────────────────────────────

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
