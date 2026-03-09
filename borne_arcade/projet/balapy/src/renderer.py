"""
renderer.py - Rendu graphique du jeu
"""
import pygame
import math


# Palette de couleurs
C_BG         = (15, 10, 25)
C_BG2        = (25, 18, 40)
C_PANEL      = (30, 22, 50)
C_BORDER     = (80, 60, 120)
C_GOLD       = (255, 200, 50)
C_GOLD2      = (220, 160, 30)
C_WHITE      = (240, 235, 255)
C_GRAY       = (140, 130, 160)
C_RED        = (255, 80, 100)
C_GREEN      = (80, 255, 140)
C_BLUE       = (80, 160, 255)
C_PURPLE     = (180, 80, 255)
C_ORANGE     = (255, 160, 50)
C_DARK_RED   = (180, 30, 50)
C_DARK_GREEN = (20, 120, 60)

# Couleurs des enseignes
SUIT_FG = {'♠': (180, 210, 255), '♥': (255, 100, 120), '♦': (255, 160, 80), '♣': (120, 240, 160)}


def lerp(a, b, t):
    return a + (b - a) * t


def draw_rounded_rect(surface, color, rect, radius=10, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def draw_glow(surface, color, center, radius, intensity=120):
    """Dessine un halo lumineux"""
    glow_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -2):
        alpha = int(intensity * (1 - r / radius) ** 2)
        col = (*color[:3], min(alpha, 255))
        pygame.draw.circle(glow_surf, col, (radius, radius), r)
    surface.blit(glow_surf, (center[0] - radius, center[1] - radius))


class Fonts:
    _instance = None

    def __init__(self, scale=1.0):
        self.scale = scale
        self._load()

    def _load(self):
        s = self.scale
        try:
            # Essayer des polices système stylées
            self.title   = pygame.font.SysFont('Impact', int(72 * s), bold=True)
            self.big     = pygame.font.SysFont('Impact', int(48 * s), bold=True)
            self.medium  = pygame.font.SysFont('Impact', int(32 * s))
            self.normal  = pygame.font.SysFont('Consolas', int(22 * s))
            self.small   = pygame.font.SysFont('Consolas', int(16 * s))
            self.tiny    = pygame.font.SysFont('Consolas', int(13 * s))
            self.card_rank = pygame.font.SysFont('Impact', int(38 * s), bold=True)
            self.card_suit = pygame.font.SysFont('Arial', int(28 * s))
            self.score   = pygame.font.SysFont('Impact', int(56 * s), bold=True)
        except:
            default = pygame.font.Font(None, int(32 * s))
            self.title = self.big = self.medium = self.normal = self.small = default
            self.tiny = self.card_rank = self.card_suit = self.score = default

    @classmethod
    def get(cls, scale=1.0):
        if cls._instance is None:
            cls._instance = Fonts(scale)
        return cls._instance


class CardRenderer:
    def __init__(self, fonts):
        self.fonts = fonts

    def get_card_size(self, sw, sh):
        """Taille adaptative de carte"""
        w = max(70, int(sw * 0.072))
        h = int(w * 1.45)
        return w, h

    def draw_card(self, surface, card, x, y, w, h, selected=False, highlighted=False, cursor=False, alpha=255, scale=1.0):
        """Dessine une carte complète"""
        if scale != 1.0:
            w2 = int(w * scale)
            h2 = int(h * scale)
            x += (w - w2) // 2
            y += (h - h2) // 2
            w, h = w2, h2

        rect = pygame.Rect(x, y, w, h)

        # Ombre
        shadow_surf = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 120), (3, 3, w, h), border_radius=10)
        surface.blit(shadow_surf, (x - 1, y + 4))

        # Fond de la carte
        if card.enhanced == 'gold':
            bg_color = (60, 50, 20)
        elif card.enhanced == 'steel':
            bg_color = (25, 35, 55)
        elif card.enhanced == 'glass':
            bg_color = (40, 55, 70)
        elif card.enhanced == 'mult':
            bg_color = (55, 20, 30)
        else:
            bg_color = (245, 240, 255) if alpha == 255 else (200, 195, 220)

        # Créer surface avec alpha
        card_surf = pygame.Surface((w, h), pygame.SRCALPHA)

        # Fond
        r, g, b = bg_color
        pygame.draw.rect(card_surf, (*bg_color, alpha), (0, 0, w, h), border_radius=10)

        # Bordure sélection / curseur
        if cursor:
            border_col = C_GOLD
            border_w = 3
        elif selected:
            border_col = C_GREEN
            border_w = 3
        elif highlighted:
            border_col = C_BLUE
            border_w = 2
        else:
            border_col = (160, 150, 200)
            border_w = 1

        pygame.draw.rect(card_surf, (*border_col, alpha), (0, 0, w, h), border_w, border_radius=10)

        # Rang et enseigne
        suit_color = SUIT_FG[card.suit]
        is_face_dark = card.enhanced in ('steel', 'glass', 'mult')
        rank_color = suit_color if is_face_dark else (
            (220, 60, 80) if card.is_red() else (30, 30, 60)
        )

        # Coin supérieur gauche
        rank_surf = self.fonts.card_rank.render(card.rank, True, rank_color)
        card_surf.blit(rank_surf, (5, 2))

        suit_surf = self.fonts.card_suit.render(card.suit, True, suit_color)
        card_surf.blit(suit_surf, (5, int(h * 0.28)))

        # Centre de la carte - grande enseigne
        big_suit_font = pygame.font.SysFont('Arial', int(h * 0.4), bold=True)
        big_suit = big_suit_font.render(card.suit, True, suit_color)
        sx = (w - big_suit.get_width()) // 2
        sy = (h - big_suit.get_height()) // 2
        card_surf.blit(big_suit, (sx, sy))

        # Coin inférieur droit (inversé)
        rank_surf2 = pygame.transform.rotate(rank_surf, 180)
        suit_surf2 = pygame.transform.rotate(suit_surf, 180)
        card_surf.blit(rank_surf2, (w - rank_surf2.get_width() - 5, h - rank_surf2.get_height() - 2))
        card_surf.blit(suit_surf2, (w - suit_surf2.get_width() - 5, int(h * 0.55)))

        # Badge d'amélioration
        if card.enhanced:
            badges = {'gold': ('★', C_GOLD), 'mult': ('+M', C_RED),
                      'steel': ('⚙', C_BLUE), 'glass': ('◈', (150, 230, 255)),
                      'wild': ('*', C_PURPLE)}
            if card.enhanced in badges:
                txt, col = badges[card.enhanced]
                badge_surf = self.fonts.tiny.render(txt, True, col)
                card_surf.blit(badge_surf, (w - badge_surf.get_width() - 3, 3))

        surface.blit(card_surf, (x, y))

        # Halo si sélectionné
        if selected:
            draw_glow(surface, C_GREEN, (x + w // 2, y + h // 2), w // 2, 60)
        elif cursor:
            draw_glow(surface, C_GOLD, (x + w // 2, y + h // 2), w // 2, 80)

        return rect


class HUDRenderer:
    def __init__(self, fonts, sw, sh):
        self.fonts = fonts
        self.sw = sw
        self.sh = sh

    def draw_panel(self, surface, x, y, w, h, title=None, color=C_PANEL):
        draw_rounded_rect(surface, color, (x, y, w, h), radius=12,
                          border=2, border_color=C_BORDER)
        if title:
            t = self.fonts.small.render(title, True, C_GOLD)
            surface.blit(t, (x + 10, y + 6))

    def draw_score_display(self, surface, chips, mult, score, x, y, w):
        """Affiche chips x mult = score"""
        h = int(self.sh * 0.12)
        self.draw_panel(surface, x, y, w, h)

        cx = x + w // 2
        cy = y + h // 2

        # CHIPS
        chips_str = f"{chips}"
        c_surf = self.fonts.big.render(chips_str, True, C_BLUE)
        surface.blit(c_surf, (cx - c_surf.get_width() - 60, cy - c_surf.get_height() // 2))

        # x
        x_surf = self.fonts.medium.render("×", True, C_WHITE)
        surface.blit(x_surf, (cx - x_surf.get_width() // 2, cy - x_surf.get_height() // 2))

        # MULT
        m_surf = self.fonts.big.render(f"{mult}", True, C_RED)
        surface.blit(m_surf, (cx + 40, cy - m_surf.get_height() // 2))

        # = SCORE
        if score > 0:
            score_surf = self.fonts.score.render(f"{score:,}", True, C_GOLD)
            surface.blit(score_surf, (cx - score_surf.get_width() // 2,
                                       cy + c_surf.get_height() // 2 + 5))

    def draw_progress_bar(self, surface, x, y, w, h, value, maximum, color=C_GREEN, label=""):
        pygame.draw.rect(surface, (40, 35, 60), (x, y, w, h), border_radius=6)
        if maximum > 0:
            fill = int(w * min(value / maximum, 1.0))
            if fill > 0:
                pygame.draw.rect(surface, color, (x, y, fill, h), border_radius=6)
        pygame.draw.rect(surface, C_BORDER, (x, y, w, h), 1, border_radius=6)
        if label:
            lbl = self.fonts.tiny.render(label, True, C_WHITE)
            surface.blit(lbl, (x + 5, y + (h - lbl.get_height()) // 2))

    def draw_controls_hint(self, surface, y):
        """Affiche les contrôles en bas de l'écran"""
        controls = [
            ("◄►", "Naviguer"),
            ("F", "selectionner"),
            ("G", "jouer"),
            ("H", "defausser"),
        ]
        total_w = 0
        items = []
        for key, desc in controls:
            k = self.fonts.tiny.render(f"[{key}]", True, C_GOLD)
            d = self.fonts.tiny.render(desc, True, C_GRAY)
            items.append((k, d))
            total_w += k.get_width() + d.get_width() + 30

        x = (self.sw - total_w) // 2
        for k, d in items:
            surface.blit(k, (x, y))
            x += k.get_width() + 6
            surface.blit(d, (x, y))
            x += d.get_width() + 24
