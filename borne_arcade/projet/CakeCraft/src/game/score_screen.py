import pygame
import sys
from core.screen import Screen
from core.constants import FONT_TITLE_PATH, FONT_BODY_PATH

_DARK_BG     = (28, 18, 10)
_GOLD        = (255, 200, 50)
_SILVER      = (180, 180, 200)
_WHITE       = (255, 248, 240)
_RED_MUTED   = (200, 80, 80)
_GREEN_MUTED = (80, 180, 80)

_font_title  = None
_font_body   = None
_font_small  = None


def _load_fonts():
    global _font_title, _font_body, _font_small
    if _font_title is not None:
        return
    try:
        _font_title = pygame.font.Font(FONT_TITLE_PATH, 64)
        _font_body  = pygame.font.Font(FONT_BODY_PATH,  36)
        _font_small = pygame.font.Font(FONT_BODY_PATH,  24)
    except Exception:
        _font_title = pygame.font.SysFont('georgia', 64, bold=True)
        _font_body  = pygame.font.SysFont('arial', 36)
        _font_small = pygame.font.SysFont('arial', 24)


class ScoreScreen:
    def __init__(self, score_left: int, score_right: int,
                 lost_time_left: float = None, lost_time_right: float = None,
                 vs_mode: bool = False, bot_left: bool = False, bot_right: bool = False):
        self.screen          = Screen().screen
        self.score_left      = score_left
        self.score_right     = score_right
        self.lost_time_left  = lost_time_left
        self.lost_time_right = lost_time_right
        self.vs_mode         = vs_mode
        self.bot_left        = bot_left
        self.bot_right       = bot_right
        self.result          = None
        self.running         = True
        self.buttons         = {}
        self._selected       = 0  # 0 = Rejouer, 1 = Quitter

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        if seconds is None:
            return "—"
        m, s = divmod(int(seconds), 60)
        return f"{m}:{s:02d}"

    def _winner(self) -> str:
        if self.lost_time_left is None and self.lost_time_right is None:
            if self.score_left > self.score_right:
                return "Joueur 1"
            elif self.score_right > self.score_left:
                return "Joueur 2"
            return "Egalite !"
        if self.lost_time_left is None:
            return "Joueur 1"
        if self.lost_time_right is None:
            return "Joueur 2"
        if self.lost_time_left > self.lost_time_right:
            return "Joueur 1"
        if self.lost_time_right > self.lost_time_left:
            return "Joueur 2"
        if self.score_left > self.score_right:
            return "Joueur 1"
        if self.score_right > self.score_left:
            return "Joueur 2"
        return "Egalite !"

    def _ask_names_and_save(self):
        """Show name entry for human players then persist to scoreboard."""
        from game.name_entry import NameEntry, NameEntryDuo
        import game.scoreboard as sb

        if self.vs_mode:
            # Both players enter their name simultaneously
            name1, name2 = NameEntryDuo().run()
            if name1:
                sb.add_solo(name1, self.score_left)
            if name2:
                sb.add_solo(name2, self.score_right)
            if name1 and name2:
                sb.add_vs(name1, self.score_left, name2, self.score_right)
        elif self.bot_right:
            # J1 (left) is human
            name = NameEntry(0, "Joueur 1 — Entrez votre nom").run()
            if name:
                sb.add_solo(name, self.score_left)
        elif self.bot_left:
            # J2 (right) is human
            name = NameEntry(1, "Joueur 2 — Entrez votre nom").run()
            if name:
                sb.add_solo(name, self.score_right)

    def handle_events(self):
        _ORDER = ["replay", "quit"]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_3):
                    self.result = "quit"; self.running = False
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self._selected = 1 - self._selected
                elif event.key in (pygame.K_1, pygame.K_4, pygame.K_RETURN):
                    self.result = _ORDER[self._selected]; self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self.result = name; self.running = False

    def _draw_button(self, text: str, cx: int, cy: int, selected: bool = False) -> pygame.Rect:
        font  = _font_small
        label = font.render(text, True, _DARK_BG)
        rect  = label.get_rect(center=(cx, cy))
        pad   = pygame.Rect(rect.left - 24, rect.top - 12, rect.width + 48, rect.height + 24)
        pygame.draw.rect(self.screen, _GOLD, pad, border_radius=14)
        if selected:
            pygame.draw.rect(self.screen, (255, 255, 255), pad, 3, border_radius=14)
        self.screen.blit(label, rect)
        return pad

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(_DARK_BG)
        _load_fonts()

        winner = self._winner()

        title = _font_title.render("Fin de partie !", True, _GOLD)
        self.screen.blit(title, title.get_rect(centerx=w // 2, top=40))

        win_surf = _font_body.render(f"Gagnant : {winner}", True, _GOLD)
        self.screen.blit(win_surf, win_surf.get_rect(centerx=w // 2, top=130))

        pygame.draw.line(self.screen, (80, 60, 40), (60, 200), (w - 60, 200), 2)

        col_y = 220
        for side, score, lost_t, label in [
            ("left",  self.score_left,  self.lost_time_left,  "Joueur 1"),
            ("right", self.score_right, self.lost_time_right, "Joueur 2"),
        ]:
            cx = w // 4 if side == "left" else 3 * w // 4
            is_winner = (label == winner)

            name_color = _GOLD if is_winner else _WHITE
            name_surf  = _font_body.render(label, True, name_color)
            self.screen.blit(name_surf, name_surf.get_rect(centerx=cx, top=col_y))

            score_surf = _font_body.render(f"{score} pts", True, _GREEN_MUTED if is_winner else _SILVER)
            self.screen.blit(score_surf, score_surf.get_rect(centerx=cx, top=col_y + 55))

            survived = _font_small.render(
                f"Tenu {self._fmt_time(lost_t)}" if lost_t else "Jusqu'au bout",
                True, _WHITE
            )
            self.screen.blit(survived, survived.get_rect(centerx=cx, top=col_y + 105))

        btn_y = h - 100
        replay_rect = self._draw_button("Rejouer", w // 2 - 130, btn_y, selected=(self._selected == 0))
        quit_rect   = self._draw_button("Quitter", w // 2 + 130, btn_y, selected=(self._selected == 1))
        self.buttons = {"replay": replay_rect, "quit": quit_rect}

        pygame.display.flip()

    def run(self) -> str:
        # Ask for names and save before showing the results screen
        self._ask_names_and_save()

        # Then show results until the player chooses to replay or quit
        while self.running:
            self.handle_events()
            self.draw()

        return self.result
