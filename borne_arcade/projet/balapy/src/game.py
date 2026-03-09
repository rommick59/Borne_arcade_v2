"""
game.py - Logique principale du jeu BALATRY Arcade
États: MENU, PLAYING, SCORING, SHOP, GAME_OVER, VICTORY
"""
import pygame
import math
import random

from cards import Deck, evaluate_hand, calculate_score, HAND_NAMES
from jokers import get_random_joker_shop
from renderer import (CardRenderer, HUDRenderer, Fonts, draw_rounded_rect,
                      draw_glow, C_BG, C_BG2, C_PANEL, C_BORDER, C_GOLD, C_GOLD2,
                      C_WHITE, C_GRAY, C_RED, C_GREEN, C_BLUE, C_PURPLE, C_ORANGE,
                      C_DARK_RED, C_DARK_GREEN, SUIT_FG, lerp)


# Configuration des niveaux (blind)
BLINDS = [
    {'name': 'PETIT BLIND', 'target': 300,   'reward': 3,  'ante': 1},
    {'name': 'GRAND BLIND', 'target': 450,   'reward': 4,  'ante': 1},
    {'name': 'PETIT BLIND', 'target': 800,   'reward': 4,  'ante': 2},
    {'name': 'GRAND BLIND', 'target': 1200,  'reward': 5,  'ante': 2},
    {'name': 'PETIT BLIND', 'target': 2000,  'reward': 5,  'ante': 3},
    {'name': 'GRAND BLIND', 'target': 3000,  'reward': 6,  'ante': 3},
    {'name': 'GRAND FINAL', 'target': 8000,  'reward': 15, 'ante': 4},
]

HANDS_PER_ROUND = 4
DISCARDS_PER_ROUND = 3
HAND_SIZE = 8
MAX_JOKERS = 5
MAX_SELECTED = 5


class FloatingText:
    """Texte flottant animé"""
    def __init__(self, text, x, y, color, font, duration=1.5, speed_y=-60):
        self.text = text
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.font = font
        self.duration = duration
        self.timer = 0
        self.speed_y = speed_y
        self.surf = font.render(text, True, color)

    def update(self, dt):
        self.timer += dt
        self.y += self.speed_y * dt

    def is_dead(self):
        return self.timer >= self.duration

    def draw(self, surface):
        alpha = int(255 * (1 - self.timer / self.duration))
        s = self.surf.copy()
        s.set_alpha(alpha)
        surface.blit(s, (int(self.x - s.get_width() // 2), int(self.y)))





class Game:
    def __init__(self, screen, sw, sh):
        self.screen = screen
        self.sw = sw
        self.sh = sh
        self.scale = min(sw / 1280, sh / 720)

        self.fonts = Fonts(self.scale)
        self.card_renderer = CardRenderer(self.fonts)
        self.hud = HUDRenderer(self.fonts, sw, sh)

        self.card_w, self.card_h = self.card_renderer.get_card_size(sw, sh)

        self.state = 'MENU'
        self.float_texts = []
        self.anim_timer = 0


        self._init_game()


        try:
            import numpy as np
            rate = 44100
            n = int(rate * duration)
            t = [i / rate for i in range(n)]
            wave = [int(32767 * math.sin(2 * math.pi * freq * ti) *
                        math.exp(-3 * ti / duration)) for ti in t]
            arr = bytes(sum([[w & 0xff, (w >> 8) & 0xff] * 2 for w in wave], []))
            sound = pygame.sndarray.make_sound(
                __import__('numpy').array([[w, w] for w in wave], dtype='int16'))
            return sound
        except:
            return None


    def _init_game(self):
        """Initialise une nouvelle partie"""
        self.deck = Deck()
        self.hand = []
        self.selected = []
        self.cursor = 0

        self.money = 4
        self.score = 0
        self.round_score = 0
        self.blind_index = 0
        self.hands_left = HANDS_PER_ROUND
        self.discards_left = DISCARDS_PER_ROUND

        self.jokers = []
        self.consumables = []

        self.last_hand_type = ''
        self.last_chips = 0
        self.last_mult = 0
        self.last_score = 0

        # Stats
        self.stats = {h: 0 for h in HAND_NAMES}
        self.total_hands_played = 0

        self.shop_items = []
        self.shop_cursor = 0

        # Animations
        self.scoring_phase = False
        self.scoring_timer = 0
        self.scoring_cards = []
        self.show_score_popup = False
        self.score_popup_timer = 0

        self.anim_timer = 0

    def current_blind(self):
        if self.blind_index < len(BLINDS):
            return BLINDS[self.blind_index]
        return BLINDS[-1]

    def handle_input(self, key):
        if self.state == 'MENU':
            self._menu_input(key)
        elif self.state == 'PLAYING':
            self._playing_input(key)
        elif self.state == 'SCORING':
            self._scoring_input(key)
        elif self.state == 'SHOP':
            self._shop_input(key)
        elif self.state == 'GAME_OVER':
            self._gameover_input(key)
        elif self.state == 'VICTORY':
            self._gameover_input(key)
        elif self.state == 'STATS':
            self.state = 'PLAYING'

    def _menu_input(self, key):
        if key in (pygame.K_f, pygame.K_RETURN, pygame.K_SPACE):
            self._init_game()
            self._start_round()
            self.state = 'PLAYING'

    def _playing_input(self, key):
        if not self.hand:
            return

        if key == pygame.K_LEFT:
            self.cursor = (self.cursor - 1) % len(self.hand)


        elif key == pygame.K_RIGHT:
            self.cursor = (self.cursor + 1) % len(self.hand)


        elif key == pygame.K_f:
            # Sélectionner / désélectionner la carte sous le curseur
            card = self.hand[self.cursor]
            if card in self.selected:
                self.selected.remove(card)
            elif len(self.selected) < MAX_SELECTED:
                self.selected.append(card)

        elif key == pygame.K_g:
            # JOUER la main sélectionnée
            if self.selected and self.hands_left > 0:
                self._play_hand()

        elif key == pygame.K_h:
            # DÉFAUSSER les cartes sélectionnées
            if self.selected and self.discards_left > 0:
                self._discard()

        elif key == pygame.K_t:
            # Afficher info jokers
            pass  # Géré dans le rendu

    def _scoring_input(self, key):
        # Passer l'animation de score
        if key in (pygame.K_f, pygame.K_RETURN):
            self.scoring_phase = False
            self.state = 'PLAYING'
            self._check_round_end()

    def _shop_input(self, key):
        n = len(self.shop_items)
        if n == 0:
            if key in (pygame.K_h, pygame.K_r):
                self._next_round()
            return

        if key == pygame.K_LEFT:
            self.shop_cursor = (self.shop_cursor - 1) % n
        elif key == pygame.K_RIGHT:
            self.shop_cursor = (self.shop_cursor + 1) % n
        elif key == pygame.K_f:
            # Acheter l'item sélectionné
            self._buy_shop_item(self.shop_cursor)
        elif key == pygame.K_h:
            # Continuer / passer le shop
            self._next_round()

    def _gameover_input(self, key):
        if key in (pygame.K_f, pygame.K_RETURN):
            self.state = 'MENU'

    # ========================
    # LOGIQUE DE JEU
    # ========================

    def _start_round(self):
        """Démarre un nouveau round"""
        self.deck.reset()
        self.hand = []
        self.selected = []
        self.cursor = 0
        self.round_score = 0
        self.hands_left = HANDS_PER_ROUND
        self.discards_left = DISCARDS_PER_ROUND
        self._draw_hand()

    def _apply_boss_effect(self):
        """Applique un effet de boss aléatoire"""
        effects = ['no_flush', 'blind_suits', 'hand_size_minus', 'no_discard']
        self.boss_effect = random.choice(effects)

    def _draw_hand(self):
        """Pioche jusqu'à HAND_SIZE cartes"""
        needed = HAND_SIZE - len(self.hand)
        drawn = self.deck.draw(needed)
        self.hand.extend(drawn)
        if self.cursor >= len(self.hand):
            self.cursor = max(0, len(self.hand) - 1)

    def _play_hand(self):
        """Joue la main sélectionnée"""
        if not self.selected:
            return

        cards = list(self.selected)

        hand_type, scoring_cards, kickers = evaluate_hand(cards)

        # Mettre à jour les jokers qui ont besoin d'info
        for j in self.jokers:
            if hasattr(j, 'discards_left'):
                j.discards_left = self.discards_left
            if hasattr(j, 'deck_remaining'):
                j.deck_remaining = self.deck.remaining()
            if hasattr(j, 'discards_used'):
                j.discards_used = DISCARDS_PER_ROUND - self.discards_left

        chips, mult, score = calculate_score(hand_type, scoring_cards, self.jokers)

        self.last_hand_type = hand_type
        self.last_chips = chips
        self.last_mult = mult
        self.last_score = score
        self.round_score += score
        self.stats[hand_type] = self.stats.get(hand_type, 0) + 1
        self.total_hands_played += 1
        self.hands_left -= 1

        # Retirer les cartes jouées de la main
        for c in self.selected:
            if c in self.hand:
                self.hand.remove(c)
        self.selected = []

        # Piocher de nouvelles cartes
        self._draw_hand()
        self.cursor = min(self.cursor, max(0, len(self.hand) - 1))




        # Entrer en phase de scoring
        self.scoring_phase = True
        self.scoring_timer = 0
        self.scoring_cards = scoring_cards
        self.state = 'SCORING'

        self._add_float(f"+{score:,}", self.sw // 2, self.sh * 0.4, C_GOLD, self.fonts.big)

        # Vérifier victoire du blind
        blind = self.current_blind()
        if self.round_score >= blind['target']:
            self._win_round()

    def _discard(self):
        """Défausse les cartes sélectionnées"""
        if self.discards_left <= 0:
            self._add_float("PAS DE DÉFAUSSE!", self.sw // 2, self.sh * 0.5, C_RED, self.fonts.medium)
            return

        for c in self.selected:
            if c in self.hand:
                self.hand.remove(c)

        self.selected = []
        self.discards_left -= 1
        self._draw_hand()
        self.cursor = min(self.cursor, max(0, len(self.hand) - 1))

        self._add_float(f"DÉFAUSSE! ({self.discards_left} restantes)", self.sw // 2, self.sh * 0.5, C_ORANGE, self.fonts.medium)

    def _win_round(self):
        """Gagne le blind actuel"""
        blind = self.current_blind()
        reward = blind['reward']
        self.money += reward


        self._add_float(f"VICTOIRE! +${reward}", self.sw // 2, self.sh * 0.3, C_GOLD, self.fonts.big, duration=2.5)

        self.blind_index += 1

        if self.blind_index >= len(BLINDS):
            self.state = 'VICTORY'
            return

        # Aller au shop
        self._generate_shop()
        self.state = 'SHOP'

    def _check_round_end(self):
        """Vérifie si le round est terminé (défaite)"""
        blind = self.current_blind()
        if self.round_score >= blind['target']:
            return  # Déjà géré

        if self.hands_left <= 0:
            # Défaite
            self.state = 'GAME_OVER'

    def _generate_shop(self):
        """Génère les items du shop"""
        existing_ids = [j.id for j in self.jokers]
        self.shop_items = get_random_joker_shop(existing_ids)
        self.shop_cursor = 0

    def _buy_shop_item(self, idx):
        """Achète un item dans le shop"""
        if idx >= len(self.shop_items):
            return
        item = self.shop_items[idx]

        if self.money >= item.cost and len(self.jokers) < MAX_JOKERS:
            self.money -= item.cost
            self.jokers.append(item)
            self.shop_items.pop(idx)
            self.shop_cursor = min(self.shop_cursor, max(0, len(self.shop_items) - 1))
            self._add_float(f"Joker acheté!", self.sw // 2, self.sh * 0.5, C_GREEN, self.fonts.medium)
        elif len(self.jokers) >= MAX_JOKERS:
            self._add_float("MAX JOKERS!", self.sw // 2, self.sh * 0.5, C_RED, self.fonts.medium)
        else:
            self._add_float("Pas assez d'argent!", self.sw // 2, self.sh * 0.5, C_RED, self.fonts.medium)

    def _next_round(self):
        """Lance le prochain round"""
        self._start_round()
        self.state = 'PLAYING'

    # ========================
    # UTILITAIRES VISUELS
    # ========================

    def _card_x(self, idx):
        """Position X d'une carte dans la main"""
        n = len(self.hand)
        if n == 0:
            return self.sw // 2
        total_w = n * self.card_w + (n - 1) * 12
        start_x = (self.sw - total_w) // 2
        return start_x + idx * (self.card_w + 12)

    def _card_y(self, selected=False):
        """Position Y des cartes (légèrement remontées si sélectionnées)"""
        base_y = int(self.sh * 0.58)
        return base_y - (int(self.card_h * 0.25) if selected else 0)

    def _add_float(self, text, x, y, color, font, duration=1.8, speed=-80):
        self.float_texts.append(FloatingText(text, x, y, color, font, duration, speed))



    # ========================
    # UPDATE
    # ========================

    def update(self, dt):
        self.anim_timer += dt


        # Textes flottants
        self.float_texts = [f for f in self.float_texts if not f.is_dead()]
        for f in self.float_texts:
            f.update(dt)

        # Scoring auto
        if self.state == 'SCORING':
            self.scoring_timer += dt
            if self.scoring_timer > 2.5:
                self.scoring_phase = False
                self.state = 'PLAYING'
                self._check_round_end()

    # ========================
    # DRAW
    # ========================

    def draw(self):
        self.screen.fill(C_BG)
        self._draw_bg_pattern()

        if self.state == 'MENU':
            self._draw_menu()
        elif self.state in ('PLAYING', 'SCORING'):
            self._draw_game()
        elif self.state == 'SHOP':
            self._draw_shop()
        elif self.state == 'GAME_OVER':
            self._draw_gameover(False)
        elif self.state == 'VICTORY':
            self._draw_gameover(True)
        elif self.state == 'STATS':
            self._draw_stats()

        # Particules et textes flottants
        for f in self.float_texts:
            f.draw(self.screen)

    def _draw_bg_pattern(self):
        """Motif de fond animé"""
        t = self.anim_timer
        for i in range(0, self.sw, 80):
            alpha = int(15 + 8 * math.sin(t * 0.5 + i * 0.02))
            pygame.draw.line(self.screen, (60, 40, 80, alpha), (i, 0), (i, self.sh))
        for j in range(0, self.sh, 80):
            alpha = int(15 + 8 * math.sin(t * 0.5 + j * 0.02))
            pygame.draw.line(self.screen, (60, 40, 80, alpha), (0, j), (self.sw, j))

    def _draw_menu(self):
        """Écran titre"""
        t = self.anim_timer

        # Titre principal
        title_y = int(self.sh * 0.28)
        glow_r = int(200 + 20 * math.sin(t * 2))
        draw_glow(self.screen, C_GOLD, (self.sw // 2, title_y), glow_r, 80)

        title = self.fonts.title.render("BALATRY", True, C_GOLD)
        sub   = self.fonts.big.render("ARCADE", True, C_WHITE)
        self.screen.blit(title, (self.sw // 2 - title.get_width() // 2, title_y - title.get_height() // 2))
        self.screen.blit(sub, (self.sw // 2 - sub.get_width() // 2, title_y + title.get_height() // 2 + 10))

        # Animation de cartes déco
        suits = ['♠', '♥', '♦', '♣']
        for i, s in enumerate(suits):
            x = self.sw // 2 + int(220 * math.cos(t * 0.4 + i * math.pi / 2))
            y = int(self.sh * 0.35) + int(30 * math.sin(t * 0.6 + i))
            color = SUIT_FG[s]
            sf = self.fonts.big.render(s, True, color)
            self.screen.blit(sf, (x - sf.get_width() // 2, y - sf.get_height() // 2))

        # Instructions
        blink = int(255 * (0.5 + 0.5 * math.sin(t * 3)))
        start = self.fonts.medium.render("APPUIE SUR  [F]  POUR JOUER", True, (*C_GOLD[:3], blink))
        start.set_alpha(blink)
        self.screen.blit(start, (self.sw // 2 - start.get_width() // 2, int(self.sh * 0.62)))

        # Contrôles
        ctrl_y = int(self.sh * 0.75)
        controls = [
            ("◄ ►", "Naviguer les cartes"),
            ("F", "Sélectionner/Valider"),
            ("G", "Jouer la main"),
            ("H", "Défausser"),
        ]
        for i, (k, d) in enumerate(controls):
            col = 3
            row = i % ((len(controls) + col - 1) // col)
            ci = i // ((len(controls) + col - 1) // col)
            x = self.sw // 4 + ci * self.sw // 3
            y = ctrl_y + row * int(30 * self.scale)

            k_s = self.fonts.small.render(f"[{k}]", True, C_GOLD)
            d_s = self.fonts.small.render(d, True, C_GRAY)
            self.screen.blit(k_s, (x, y))
            self.screen.blit(d_s, (x + k_s.get_width() + 8, y))

        # Version
        v = self.fonts.tiny.render("v1.0 - ARCADE EDITION", True, C_GRAY)
        self.screen.blit(v, (self.sw - v.get_width() - 10, self.sh - v.get_height() - 5))

    def _draw_game(self):
        """Écran de jeu principal"""
        blind = self.current_blind()

        # ---- PANNEAU GAUCHE: Info round ----
        panel_w = int(self.sw * 0.22)
        panel_x = int(self.sw * 0.01)
        panel_y = int(self.sh * 0.02)

        # Blind name + target
        self.hud.draw_panel(self.screen, panel_x, panel_y, panel_w, int(self.sh * 0.18))
        ante_s = self.fonts.tiny.render(f"ANTE {blind['ante']}", True, C_GRAY)
        blind_s = self.fonts.normal.render(blind['name'], True, C_GOLD)
        self.screen.blit(ante_s, (panel_x + 10, panel_y + 6))
        self.screen.blit(blind_s, (panel_x + 10, panel_y + 22))

        # Barre de progression
        bar_y = panel_y + int(self.sh * 0.1)
        self.hud.draw_progress_bar(
            self.screen, panel_x + 10, bar_y,
            panel_w - 20, 18,
            self.round_score, blind['target'],
            C_GREEN,
            f"{self.round_score:,} / {blind['target']:,}"
        )

        # Mains / défausses
        info_y = panel_y + int(self.sh * 0.2)
        self.hud.draw_panel(self.screen, panel_x, info_y, panel_w, int(self.sh * 0.15))

        hands_s = self.fonts.normal.render(f"Mains:    {self.hands_left}", True,
                                            C_GREEN if self.hands_left > 1 else C_RED)
        disc_s  = self.fonts.normal.render(f"Défausses: {self.discards_left}", True,
                                            C_BLUE if self.discards_left > 0 else C_GRAY)
        self.screen.blit(hands_s, (panel_x + 10, info_y + 8))
        self.screen.blit(disc_s,  (panel_x + 10, info_y + 36))

        # Argent
        money_y = info_y + int(self.sh * 0.18)
        self.hud.draw_panel(self.screen, panel_x, money_y, panel_w, int(self.sh * 0.08))
        money_s = self.fonts.medium.render(f"$ {self.money}", True, C_GOLD)
        self.screen.blit(money_s, (panel_x + 10, money_y + 8))

        # Deck restant
        deck_y = money_y
        deck_s = self.fonts.small.render(f"Deck: {self.deck.remaining()}", True, C_GRAY)
        self.screen.blit(deck_s, (panel_x + 10, deck_y))

        # ---- PANNEAU MAINS ----
        hands_x = panel_x
        hands_y = panel_y + int(self.sh * 0.6)
        self.hud.draw_panel(self.screen, hands_x, hands_y, panel_w, int(self.sh * 0.35), "MAINS")
        hy = hands_y + 30
        hand_multipliers = {
            'High Card': (5, 1),
            'Pair': (10, 2),
            'Two Pair': (20, 2),
            'Three Kind': (30, 3),
            'Straight': (30, 4),
            'Flush': (35, 4),
            'Full House': (40, 4),
            'Four Kind': (60, 7),
            'Str. Flush': (100, 8),
            'Royal Flush': (100, 8),
        }
        for name, (chips, mult) in hand_multipliers.items():
            h_s = self.fonts.tiny.render(f"{name}: {chips}×{mult}", True, C_WHITE)
            self.screen.blit(h_s, (hands_x + 8, hy))
            hy += 18

        # ---- PANNEAU DROIT: Jokers ----
        joker_x = self.sw - panel_w - int(self.sw * 0.01)
        self.hud.draw_panel(self.screen, joker_x, panel_y, panel_w,
                            int(self.sh * 0.55), "JOKERS")
        jy = panel_y + 30
        for i, j in enumerate(self.jokers):
            jc = j.get_color()
            draw_rounded_rect(self.screen, (30, 25, 50), (joker_x + 8, jy, panel_w - 16, 44), 8,
                               2, jc)
            n_s = self.fonts.small.render(j.name, True, jc)
            d_s = self.fonts.tiny.render(j.description[:28], True, C_GRAY)
            self.screen.blit(n_s, (joker_x + 14, jy + 4))
            self.screen.blit(d_s, (joker_x + 14, jy + 22))
            jy += 50

        if not self.jokers:
            empty_s = self.fonts.tiny.render("(aucun joker)", True, C_GRAY)
            self.screen.blit(empty_s, (joker_x + 14, panel_y + 36))


        # ---- CENTRE: Score de la dernière main ----
        if self.last_hand_type:
            hand_name = HAND_NAMES.get(self.last_hand_type, '')
            hy = int(self.sh * 0.03)
            hn_s = self.fonts.medium.render(hand_name, True, C_WHITE)
            cx = self.sw // 2
            self.screen.blit(hn_s, (cx - hn_s.get_width() // 2, hy))

            # Chips x Mult
            c_s = self.fonts.big.render(f"{self.last_chips}", True, C_BLUE)
            x_s = self.fonts.medium.render("×", True, C_WHITE)
            m_s = self.fonts.big.render(f"{self.last_mult}", True, C_RED)
            eq_s = self.fonts.medium.render("=", True, C_WHITE)
            sc_s = self.fonts.big.render(f"{self.last_score:,}", True, C_GOLD)

            total_w = c_s.get_width() + 10 + x_s.get_width() + 10 + m_s.get_width() + 10 + eq_s.get_width() + 10 + sc_s.get_width()
            sx = cx - total_w // 2
            sy = hy + hn_s.get_height() + 5

            self.screen.blit(c_s, (sx, sy))
            sx += c_s.get_width() + 10
            self.screen.blit(x_s, (sx, sy + 6))
            sx += x_s.get_width() + 10
            self.screen.blit(m_s, (sx, sy))
            sx += m_s.get_width() + 10
            self.screen.blit(eq_s, (sx, sy + 6))
            sx += eq_s.get_width() + 10
            self.screen.blit(sc_s, (sx, sy))
        

        # ---- CARTES EN MAIN ----
        self._draw_hand_cards()

        # ---- CONTRÔLES ----
        ctrl_y = self.sh - int(30 * self.scale) - 5
        self.hud.draw_controls_hint(self.screen, ctrl_y)

        # Indicateur de sélection
        if self.selected:
            sel_s = self.fonts.small.render(
                f"{len(self.selected)}/5 cartes sélectionnées - [G] Jouer  [H] Défausser",
                True, C_WHITE)
            self.screen.blit(sel_s, (self.sw // 2 - sel_s.get_width() // 2,
                                      int(self.sh * 0.88)))

        # Scoring overlay
        if self.state == 'SCORING':
            self._draw_scoring_overlay()

    def _draw_hand_cards(self):
        """Dessine les cartes de la main"""
        n = len(self.hand)
        if n == 0:
            return

        for i, card in enumerate(self.hand):
            x = self._card_x(i)
            y_base = int(self.sh * 0.58)
            selected = card in self.selected
            cursor = (i == self.cursor)

            y = y_base - (int(self.card_h * 0.25) if selected else 0)

            # Effet de flottement pour le curseur
            if cursor:
                y -= int(8 * abs(math.sin(self.anim_timer * 3)))

            self.card_renderer.draw_card(
                self.screen, card, x, y, self.card_w, self.card_h,
                selected=selected, cursor=cursor
            )

            # Numéro sous la carte (pour aide navigation)
            # idx_s = self.fonts.tiny.render(str(i+1), True, C_GRAY)
            # self.screen.blit(idx_s, (x + self.card_w//2 - idx_s.get_width()//2, y + self.card_h + 2))

    def _draw_scoring_overlay(self):
        """Overlay pendant le calcul du score"""
        # Semi-transparent
        overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        # Cartes scorantes
        n = len(self.scoring_cards)
        if n > 0:
            cw = int(self.card_w * 1.2)
            ch = int(self.card_h * 1.2)
            total_w = n * cw + (n - 1) * 20
            sx = (self.sw - total_w) // 2
            sy = int(self.sh * 0.35)

            for i, card in enumerate(self.scoring_cards):
                glow_colors = {'♠': C_BLUE, '♥': C_RED, '♦': C_ORANGE, '♣': C_GREEN}
                draw_glow(self.screen, glow_colors[card.suit],
                          (sx + i * (cw + 20) + cw // 2, sy + ch // 2), cw, 100)
                self.card_renderer.draw_card(self.screen, card, sx + i * (cw + 20), sy, cw, ch)

        # Message
        msg = self.fonts.medium.render("[F] pour continuer", True, C_GRAY)
        self.screen.blit(msg, (self.sw // 2 - msg.get_width() // 2, int(self.sh * 0.85)))

    def _draw_shop(self):
        """Écran du shop"""
        # Titre
        t_s = self.fonts.big.render("★  BOUTIQUE  ★", True, C_GOLD)
        self.screen.blit(t_s, (self.sw // 2 - t_s.get_width() // 2, int(self.sh * 0.06)))

        # Argent
        m_s = self.fonts.medium.render(f"Argent: ${self.money}", True, C_GOLD)
        self.screen.blit(m_s, (self.sw // 2 - m_s.get_width() // 2, int(self.sh * 0.14)))

        # Items du shop
        n = len(self.shop_items)
        item_w = int(self.sw * 0.25)
        item_h = int(self.sh * 0.3)
        gap = int(self.sw * 0.03)
        total_w = n * item_w + (n - 1) * gap
        sx = (self.sw - total_w) // 2
        sy = int(self.sh * 0.25)

        for i, item in enumerate(self.shop_items):
            ix = sx + i * (item_w + gap)
            is_cursor = (i == self.shop_cursor)
            can_buy = self.money >= item.cost and len(self.jokers) < MAX_JOKERS

            border_c = C_GOLD if is_cursor else C_BORDER
            bg_c = (40, 32, 65) if is_cursor else C_PANEL
            draw_rounded_rect(self.screen, bg_c, (ix, sy, item_w, item_h), 14, 3, border_c)

            if is_cursor:
                draw_glow(self.screen, C_GOLD, (ix + item_w // 2, sy + item_h // 2), 80, 60)

            # Rareté
            rarity_colors = {'common': C_GRAY, 'uncommon': C_GREEN, 'rare': C_BLUE, 'legendary': C_GOLD}
            rc = rarity_colors.get(item.rarity, C_GRAY)
            r_s = self.fonts.tiny.render(item.rarity.upper(), True, rc)
            self.screen.blit(r_s, (ix + item_w // 2 - r_s.get_width() // 2, sy + 10))

            # Icône joker (texte)
            icon_s = self.fonts.big.render("🃏", True, item.get_color())
            # Fallback si emoji pas dispo
            icon_s2 = self.fonts.big.render("J", True, item.get_color())
            try:
                self.screen.blit(icon_s, (ix + item_w // 2 - icon_s.get_width() // 2, sy + 40))
            except:
                self.screen.blit(icon_s2, (ix + item_w // 2 - icon_s2.get_width() // 2, sy + 40))

            # Nom
            n_s = self.fonts.normal.render(item.name, True, item.get_color())
            self.screen.blit(n_s, (ix + item_w // 2 - n_s.get_width() // 2, sy + int(item_h * 0.42)))

            # Description (wrappée)
            desc_lines = self._wrap_text(item.description, self.fonts.tiny, item_w - 20)
            dy = sy + int(item_h * 0.56)
            for line in desc_lines[:3]:
                l_s = self.fonts.tiny.render(line, True, C_GRAY)
                self.screen.blit(l_s, (ix + item_w // 2 - l_s.get_width() // 2, dy))
                dy += int(18 * self.scale)

            # Prix
            price_col = C_GREEN if can_buy else C_RED
            p_s = self.fonts.medium.render(f"${item.cost}", True, price_col)
            self.screen.blit(p_s, (ix + item_w // 2 - p_s.get_width() // 2, sy + item_h - 36))

        if n == 0:
            empty_s = self.fonts.medium.render("Plus d'items disponibles", True, C_GRAY)
            self.screen.blit(empty_s, (self.sw // 2 - empty_s.get_width() // 2, int(self.sh * 0.5)))

        # Contrôles
        ctrl_y = int(self.sh * 0.75)
        controls_text = "[◄►] Naviguer   [F] Acheter   [H] Continuer"
        c_s = self.fonts.small.render(controls_text, True, C_GRAY)
        self.screen.blit(c_s, (self.sw // 2 - c_s.get_width() // 2, ctrl_y))

        # Jokers actuels
        if self.jokers:
            j_y = int(self.sh * 0.82)
            j_title = self.fonts.small.render("MES JOKERS:", True, C_GOLD)
            self.screen.blit(j_title, (self.sw // 2 - j_title.get_width() // 2, j_y))
            j_y += 22
            all_j = "  |  ".join([j.name for j in self.jokers])
            j_s = self.fonts.tiny.render(all_j, True, C_GRAY)
            self.screen.blit(j_s, (self.sw // 2 - j_s.get_width() // 2, j_y))

    def _draw_gameover(self, victory):
        t = self.anim_timer

        if victory:
            title_col = C_GOLD
            title_text = "🏆 VICTOIRE! 🏆"
            sub_text = "Tu as battu tous les blinds!"
            bg_col = (20, 30, 15)
        else:
            title_col = C_RED
            title_text = "GAME OVER"
            sub_text = "Tu n'as pas atteint l'objectif..."
            bg_col = (30, 10, 15)

        self.screen.fill(bg_col)
        self._draw_bg_pattern()

        draw_glow(self.screen, title_col, (self.sw // 2, int(self.sh * 0.3)),
                  int(200 + 20 * math.sin(t * 2)), 100)

        t_s = self.fonts.title.render(title_text, True, title_col)
        self.screen.blit(t_s, (self.sw // 2 - t_s.get_width() // 2, int(self.sh * 0.22)))

        s_s = self.fonts.medium.render(sub_text, True, C_WHITE)
        self.screen.blit(s_s, (self.sw // 2 - s_s.get_width() // 2, int(self.sh * 0.42)))

        # Stats
        stats_y = int(self.sh * 0.52)
        stats = [
            (f"Score total:", f"{self.round_score:,}"),
            (f"Mains jouées:", f"{self.total_hands_played}"),
            (f"Blinds battus:", f"{self.blind_index}"),
            (f"Argent final:", f"${self.money}"),
        ]
        for label, val in stats:
            l_s = self.fonts.normal.render(label, True, C_GRAY)
            v_s = self.fonts.normal.render(val, True, C_WHITE)
            self.screen.blit(l_s, (self.sw // 2 - 200, stats_y))
            self.screen.blit(v_s, (self.sw // 2 + 60, stats_y))
            stats_y += int(34 * self.scale)

        # Continuer
        blink = int(255 * (0.5 + 0.5 * math.sin(t * 3)))
        c_s = self.fonts.medium.render("[R] REJOUER", True, C_GOLD)
        c_s.set_alpha(blink)
        self.screen.blit(c_s, (self.sw // 2 - c_s.get_width() // 2, int(self.sh * 0.82)))

    def _draw_stats(self):
        """Écran de statistiques"""
        self.hud.draw_panel(self.screen, int(self.sw * 0.1), int(self.sh * 0.05),
                             int(self.sw * 0.8), int(self.sh * 0.85), "STATISTIQUES")

        t_s = self.fonts.big.render("STATISTIQUES", True, C_GOLD)
        self.screen.blit(t_s, (self.sw // 2 - t_s.get_width() // 2, int(self.sh * 0.1)))

        y = int(self.sh * 0.22)
        for hand_type, name in HAND_NAMES.items():
            count = self.stats.get(hand_type, 0)
            col = C_WHITE if count > 0 else C_GRAY
            l_s = self.fonts.normal.render(f"{name}:", True, col)
            v_s = self.fonts.normal.render(str(count), True, C_GOLD if count > 0 else C_GRAY)
            self.screen.blit(l_s, (int(self.sw * 0.2), y))
            self.screen.blit(v_s, (int(self.sw * 0.65), y))

            # Mini barre
            if count > 0:
                max_count = max(self.stats.values()) or 1
                bar_w = int(self.sw * 0.15 * count / max_count)
                pygame.draw.rect(self.screen, C_BLUE,
                                  (int(self.sw * 0.68), y + 4, bar_w, 14), border_radius=4)
            y += int(36 * self.scale)

        back_s = self.fonts.small.render("[G] ou [R] pour revenir", True, C_GRAY)
        self.screen.blit(back_s, (self.sw // 2 - back_s.get_width() // 2, int(self.sh * 0.88)))

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current = ''
        for w in words:
            test = current + ' ' + w if current else w
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines
