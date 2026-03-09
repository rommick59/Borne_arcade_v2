"""
cards.py - Logique des cartes et du deck
"""
import random

SUITS = ['♠', '♥', '♦', '♣']
SUIT_NAMES = {'♠': 'PIQUE', '♥': 'COEUR', '♦': 'CARREAU', '♣': 'TREFLE'}
SUIT_COLORS = {'♠': (200, 220, 255), '♥': (255, 100, 120), '♦': (255, 160, 80), '♣': (120, 255, 160)}

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

# Valeurs de base des cartes pour le score
CARD_CHIPS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]
        self.chips = CARD_CHIPS[rank]
        self.selected = False
        self.enhanced = None  # 'gold', 'mult', 'wild', 'glass', 'steel'
        self.seal = None      # 'red', 'blue', 'gold', 'purple'

        # Animation
        self.y_offset = 0
        self.target_y = 0
        self.scale = 1.0
        self.alpha = 255
        self.shake = 0

    def get_color(self):
        return SUIT_COLORS[self.suit]

    def is_red(self):
        return self.suit in ['♥', '♦']

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def get_chips(self):
        """Retourne les chips de la carte avec bonus d'amélioration"""
        base = self.chips
        if self.enhanced == 'gold':
            base += 3
        elif self.enhanced == 'steel':
            base = int(base * 1.5)
        return base


class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        drawn = []
        for _ in range(n):
            if self.cards:
                drawn.append(self.cards.pop())
        return drawn

    def remaining(self):
        return len(self.cards)


# ========================
# ÉVALUATION DES MAINS
# ========================

HAND_NAMES = {
    'royal_flush':    'QUINTE FLUSH ROYALE',
    'straight_flush': 'QUINTE FLUSH',
    'four_of_a_kind': 'CARRÉ',
    'full_house':     'FULL HOUSE',
    'flush':          'COULEUR',
    'straight':       'SUITE',
    'three_of_a_kind':'BRELAN',
    'two_pair':       'DOUBLE PAIRE',
    'pair':           'PAIRE',
    'high_card':      'CARTE HAUTE',
}

# (chips_base, mult_base)
HAND_BASE_SCORES = {
    'royal_flush':    (100, 8),
    'straight_flush': (100, 8),
    'four_of_a_kind': (60,  7),
    'full_house':     (40,  4),
    'flush':          (35,  4),
    'straight':       (30,  4),
    'three_of_a_kind':(30,  3),
    'two_pair':       (20,  2),
    'pair':           (10,  2),
    'high_card':      (5,   1),
}


def evaluate_hand(cards):
    """
    Évalue une main de 1 à 5 cartes.
    Retourne (hand_type, scoring_cards, kickers)
    """
    if not cards:
        return ('high_card', [], [])

    n = len(cards)
    ranks = [c.rank for c in cards]
    suits = [c.suit for c in cards]
    values = sorted([c.value for c in cards], reverse=True)

    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    counts = sorted(rank_counts.values(), reverse=True)
    is_flush = len(set(suits)) == 1 and n == 5
    is_straight = False

    if n == 5:
        # Check straight normal
        if max(values) - min(values) == 4 and len(set(values)) == 5:
            is_straight = True
        # Check Ace-low straight (A-2-3-4-5)
        if set(values) == {14, 2, 3, 4, 5}:
            is_straight = True
            values = [5, 4, 3, 2, 1]

    # Grouper les cartes par rang
    groups = {}
    for c in cards:
        if c.rank not in groups:
            groups[c.rank] = []
        groups[c.rank].append(c)

    sorted_groups = sorted(groups.items(), key=lambda x: (len(x[1]), RANK_VALUES[x[0]]), reverse=True)

    # Déterminer le type de main
    if n == 5 and is_flush and is_straight:
        if values[0] == 14:
            return ('royal_flush', cards, [])
        return ('straight_flush', cards, [])

    if counts[0] == 4:
        scoring = sorted_groups[0][1]
        kickers = [c for c in cards if c not in scoring]
        return ('four_of_a_kind', scoring, kickers)

    if len(counts) >= 2 and counts[0] == 3 and counts[1] == 2:
        scoring = cards
        return ('full_house', scoring, [])

    if n == 5 and is_flush:
        return ('flush', cards, [])

    if n == 5 and is_straight:
        return ('straight', cards, [])

    if counts[0] == 3:
        scoring = sorted_groups[0][1]
        kickers = [c for c in cards if c not in scoring]
        return ('three_of_a_kind', scoring, kickers)

    if len(counts) >= 2 and counts[0] == 2 and n >= 4 and counts[1] == 2:
        scoring = sorted_groups[0][1] + sorted_groups[1][1]
        kickers = [c for c in cards if c not in scoring]
        return ('two_pair', scoring, kickers)

    if counts[0] == 2:
        scoring = sorted_groups[0][1]
        kickers = [c for c in cards if c not in scoring]
        return ('pair', scoring, kickers)

    # Carte haute
    best = sorted(cards, key=lambda c: c.value, reverse=True)
    return ('high_card', [best[0]], best[1:])


def calculate_score(hand_type, scoring_cards, jokers=None, mult_bonus=0, chips_bonus=0):
    """
    Calcule le score final d'une main.
    Retourne (chips_total, mult_total, score_final, détails)
    """
    base_chips, base_mult = HAND_BASE_SCORES[hand_type]

    chips = base_chips + chips_bonus
    mult = base_mult + mult_bonus

    # Additionner les chips des cartes scorantes
    for card in scoring_cards:
        chips += card.get_chips()
        if card.enhanced == 'mult':
            mult += 4
        elif card.enhanced == 'glass':
            mult *= 2

    # Appliquer les jokers
    if jokers:
        for joker in jokers:
            chips, mult = joker.apply(hand_type, scoring_cards, chips, mult)

    score = chips * mult
    return chips, mult, score
