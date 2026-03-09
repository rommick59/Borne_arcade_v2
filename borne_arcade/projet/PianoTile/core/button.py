import pygame


def _matches_key(event, key):
    if event.key == key:
        return True
    key_char = event.unicode.lower() if event.unicode else ""
    key_name = pygame.key.name(key).lower()
    return len(key_name) == 1 and key_char == key_name

class Button:
    def __init__(self):
        self.__buttons = {
            # Premier joueur
            pygame.K_r: False,
            pygame.K_t: False,
            pygame.K_y: False,
            pygame.K_f: False,
            pygame.K_g: False,
            pygame.K_h: False,  # Entrer
            # Deuxieme joueur
            pygame.K_a: False,
            pygame.K_z: False,
            pygame.K_e: False,
            pygame.K_q: False,
            pygame.K_s: False,
            pygame.K_d: False,  # Entrer
        }

    def update(self, event, navigation_mode=False):
        """Met à jour l'état des boutons (1 à 6) et renvoie la direction ou la touche pressée."""
        if event.type != pygame.KEYDOWN:
            return None  # Ignore les événements non-clavier

        if navigation_mode:
            if _matches_key(event, pygame.K_UP) or _matches_key(event, pygame.K_o):
                return (0, -1)
            elif _matches_key(event, pygame.K_DOWN) or _matches_key(event, pygame.K_l):
                return (0, 1)
            elif _matches_key(event, pygame.K_LEFT) or _matches_key(event, pygame.K_k):
                return (-1, 0)
            elif _matches_key(event, pygame.K_RIGHT) or _matches_key(event, pygame.K_m):
                return (1, 0)

            if _matches_key(event, pygame.K_h) or _matches_key(event, pygame.K_d):
                return "enter"

            return None

        if _matches_key(event, pygame.K_UP) or _matches_key(event, pygame.K_o):
            return (0, -1)
        elif _matches_key(event, pygame.K_DOWN) or _matches_key(event, pygame.K_l):
            return (0, 1)
        elif _matches_key(event, pygame.K_LEFT) or _matches_key(event, pygame.K_k):
            return (-1, 0)
        elif _matches_key(event, pygame.K_RIGHT) or _matches_key(event, pygame.K_m):
            return (1, 0)

        # Validation (un seul bouton logique, mappé sur deux touches)
        if _matches_key(event, pygame.K_h) or _matches_key(event, pygame.K_d):
            return "enter"

        # Joueur 1
        if _matches_key(event, pygame.K_r):
            return 0
        if _matches_key(event, pygame.K_t):
            return 1
        if _matches_key(event, pygame.K_y):
            return 2
        if _matches_key(event, pygame.K_f):
            return 3
        if _matches_key(event, pygame.K_g):
            return 4

        # Joueur 2
        if _matches_key(event, pygame.K_a):
            return 0
        if _matches_key(event, pygame.K_z):
            return 1
        if _matches_key(event, pygame.K_e):
            return 2
        if _matches_key(event, pygame.K_q):
            return 3
        if _matches_key(event, pygame.K_s):
            return 4

        return None

    def getAll(self):
        """
        Retourne l'état de tous les boutons suivis sous forme de dictionnaire.
        Exemple : {pygame.K_r: False, pygame.K_t: True, ...}
        """
        return self.__buttons.copy()
