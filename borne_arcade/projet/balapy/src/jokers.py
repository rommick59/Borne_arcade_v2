"""
jokers.py - Système de jokers (modificateurs) style balatry
"""
import random

class Joker:
    def __init__(self, jid, name, description, rarity='common', cost=3):
        self.id = jid
        self.name = name
        self.description = description
        self.rarity = rarity  # common, uncommon, rare, legendary
        self.cost = cost
        self.trigger_count = 0

    def apply(self, hand_type, scoring_cards, chips, mult):
        """Applique l'effet du joker. Override dans les sous-classes."""
        return chips, mult

    def get_color(self):
        colors = {
            'common':    (180, 180, 220),
            'uncommon':  (100, 220, 150),
            'rare':      (100, 150, 255),
            'legendary': (255, 200, 50),
        }
        return colors.get(self.rarity, (200, 200, 200))


class JokerJolly(Joker):
    """Joker de base: +4 mult"""
    def __init__(self):
        super().__init__('jolly', 'JOKER JOYEUX', '+4 Mult', 'common', 2)

    def apply(self, hand_type, scoring_cards, chips, mult):
        return chips, mult + 4


class JokerGreedy(Joker):
    """+3 mult si la main contient un carreau"""
    def __init__(self):
        super().__init__('greedy', 'JOKER AVIDE', '+3 Mult si ♦ dans la main', 'common', 3)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if any(c.suit == '♦' for c in scoring_cards):
            return chips, mult + 3
        return chips, mult


class JokerLusty(Joker):
    """+3 mult si la main contient un coeur"""
    def __init__(self):
        super().__init__('lusty', 'JOKER AMOUREUX', '+3 Mult si ♥ dans la main', 'common', 3)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if any(c.suit == '♥' for c in scoring_cards):
            return chips, mult + 3
        return chips, mult


class JokerTricky(Joker):
    """+4 mult sur une suite"""
    def __init__(self):
        super().__init__('tricky', 'JOKER RUSÉ', '+4 Mult sur Suite/Quinte Flush', 'common', 4)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('straight', 'straight_flush', 'royal_flush'):
            return chips, mult + 4
        return chips, mult


class JokerSly(Joker):
    """+50 chips sur une paire"""
    def __init__(self):
        super().__init__('sly', 'JOKER MALIN', '+50 Chips si Paire ou mieux', 'common', 3)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type not in ('high_card',):
            return chips + 50, mult
        return chips, mult


class JokerWily(Joker):
    """+100 chips sur brelan"""
    def __init__(self):
        super().__init__('wily', 'JOKER FUTÉ', '+100 Chips si Brelan ou mieux', 'uncommon', 4)

    def apply(self, hand_type, scoring_cards, chips, mult):
        good_hands = ('three_of_a_kind', 'full_house', 'four_of_a_kind',
                      'flush', 'straight', 'straight_flush', 'royal_flush')
        if hand_type in good_hands:
            return chips + 100, mult
        return chips, mult


class JokerClever(Joker):
    """+80 chips sur double paire"""
    def __init__(self):
        super().__init__('clever', 'JOKER GÉNIE', '+80 Chips sur Double Paire', 'common', 4)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type == 'two_pair':
            return chips + 80, mult
        return chips, mult


class JokerDevious(Joker):
    """+100 chips sur couleur"""
    def __init__(self):
        super().__init__('devious', 'JOKER DIABOLIQUE', '+100 Chips sur Couleur', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('flush', 'straight_flush', 'royal_flush'):
            return chips + 100, mult
        return chips, mult


class JokerCrafty(Joker):
    """+80 chips sur suite"""
    def __init__(self):
        super().__init__('crafty', 'JOKER ARTISAN', '+80 Chips sur Suite', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('straight', 'straight_flush', 'royal_flush'):
            return chips + 80, mult
        return chips, mult


class JokerHalf(Joker):
    """x1.5 mult si 3 cartes ou moins jouées"""
    def __init__(self):
        super().__init__('half', 'DEMI JOKER', 'x1.5 Mult si ≤3 cartes jouées', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if len(scoring_cards) <= 3:
            return chips, int(mult * 1.5)
        return chips, mult


class JokerZany(Joker):
    """+12 mult sur brelan"""
    def __init__(self):
        super().__init__('zany', 'JOKER DINGUE', '+12 Mult sur Brelan', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('three_of_a_kind', 'full_house'):
            return chips, mult + 12
        return chips, mult


class JokerMad(Joker):
    """+10 mult sur double paire"""
    def __init__(self):
        super().__init__('mad', 'JOKER FOU', '+10 Mult sur Double Paire', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type == 'two_pair':
            return chips, mult + 10
        return chips, mult


class JokerCrazy(Joker):
    """+12 mult sur suite"""
    def __init__(self):
        super().__init__('crazy', 'JOKER CINGLÉ', '+12 Mult sur Suite', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('straight', 'straight_flush', 'royal_flush'):
            return chips, mult + 12
        return chips, mult


class JokerDroll(Joker):
    """+10 mult sur couleur"""
    def __init__(self):
        super().__init__('droll', 'JOKER DRÔLE', '+10 Mult sur Couleur', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('flush', 'straight_flush', 'royal_flush'):
            return chips, mult + 10
        return chips, mult


class JokerSneaky(Joker):
    """+15 mult sur suite"""
    def __init__(self):
        super().__init__('sneaky', 'JOKER SOURNOIS', '+15 Mult sur Suite', 'rare', 6)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('straight', 'straight_flush', 'royal_flush'):
            return chips, mult + 15
        return chips, mult


class JokerBanner(Joker):
    """+30 chips par défausse restante"""
    def __init__(self):
        super().__init__('banner', 'BANNIÈRE', '+30 Chips/défausse restante', 'uncommon', 5)
        self.discards_left = 3

    def apply(self, hand_type, scoring_cards, chips, mult):
        return chips + (self.discards_left * 30), mult


class JokerMystic(Joker):
    """+15 mult si pas de défausse utilisée"""
    def __init__(self):
        super().__init__('mystic', 'JOKER MYSTIQUE', '+15 Mult si 0 défausse', 'rare', 6)
        self.discards_used = 0

    def apply(self, hand_type, scoring_cards, chips, mult):
        if self.discards_used == 0:
            return chips, mult + 15
        return chips, mult


class JokerLucky(Joker):
    """1 chance sur 5 de +20 mult"""
    def __init__(self):
        super().__init__('lucky', 'JOKER CHANCEUX', '1/5 chance: +20 Mult', 'uncommon', 5)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if random.random() < 0.2:
            self.trigger_count += 1
            return chips, mult + 20
        return chips, mult


class JokerSquare(Joker):
    """+4 mult si exactement 4 cartes jouées"""
    def __init__(self):
        super().__init__('square', 'JOKER CARRÉ', '+4 Mult si exactement 4 cartes', 'common', 4)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if len(scoring_cards) == 4:
            return chips, mult + 4
        return chips, mult


class JokerRaiseHell(Joker):
    """x2 mult sur Quinte Flush ou mieux"""
    def __init__(self):
        super().__init__('raisehell', 'ENFER', 'x2 Mult sur Quinte Flush', 'rare', 8)

    def apply(self, hand_type, scoring_cards, chips, mult):
        if hand_type in ('straight_flush', 'royal_flush'):
            return chips, mult * 2
        return chips, mult


class JokerBlueJoker(Joker):
    """+2 chips par carte restante dans le deck"""
    def __init__(self):
        super().__init__('blue', 'JOKER BLEU', '+2 Chips/carte restante deck', 'uncommon', 5)
        self.deck_remaining = 52

    def apply(self, hand_type, scoring_cards, chips, mult):
        return chips + (self.deck_remaining * 2), mult


# Toutes les classes de jokers disponibles
ALL_JOKER_CLASSES = [
    JokerJolly, JokerGreedy, JokerLusty, JokerTricky, JokerSly,
    JokerWily, JokerClever, JokerDevious, JokerCrafty, JokerHalf,
    JokerZany, JokerMad, JokerCrazy, JokerDroll, JokerSneaky,
    JokerBanner, JokerMystic, JokerLucky, JokerSquare, JokerRaiseHell,
    JokerBlueJoker,
]


def get_random_joker_shop(exclude_ids=None):
    """Retourne 3 jokers aléatoires pour le shop"""
    exclude_ids = exclude_ids or []
    available = [cls for cls in ALL_JOKER_CLASSES]
    random.shuffle(available)

    result = []
    for cls in available:
        j = cls()
        if j.id not in exclude_ids and len(result) < 3:
            result.append(j)
    return result
