from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class TypeRobot:
    nom: str
    poids: int
    taille: tuple[int, int]
    points_de_vie: int
    vitesse: float
    points: int


class Robot:
    def __init__(self, type_robot: TypeRobot, x: int):
        self.type = type_robot
        self.points_de_vie = type_robot.points_de_vie
        self.points_de_vie_max = type_robot.points_de_vie
        self.facteur_vitesse = type_robot.vitesse
        self.rect = pygame.Rect(x, -type_robot.taille[1] - 2, type_robot.taille[0], type_robot.taille[1])

    def mettre_a_jour(self, vitesse_base: float):
        self.rect.y += int(vitesse_base * self.facteur_vitesse)

    def prendre_tir(self) -> bool:
        self.points_de_vie -= 1
        if self.type.nom == "tank" and self.points_de_vie == 1:
            self.facteur_vitesse = min(1.0, self.facteur_vitesse + 0.12)
        return self.points_de_vie <= 0

    def dessiner(self, ecran: pygame.Surface):
        if self.type.nom == "swift":
            couleur_principale, couleur_contour = (235, 120, 80), (255, 180, 145)
        elif self.type.nom == "tank":
            couleur_principale, couleur_contour = (160, 104, 220), (216, 182, 255)
        else:
            couleur_principale, couleur_contour = (224, 84, 112), (255, 170, 188)

        pygame.draw.rect(ecran, couleur_principale, self.rect, border_radius=6)
        pygame.draw.rect(ecran, couleur_contour, self.rect, 1, border_radius=6)

        if self.points_de_vie_max > 1:
            barre = pygame.Rect(self.rect.x + 4, self.rect.y - 7, self.rect.width - 8, 4)
            avant = barre.copy()
            avant.width = int(barre.width * (self.points_de_vie / self.points_de_vie_max))
            pygame.draw.rect(ecran, (45, 20, 50), barre, border_radius=2)
            pygame.draw.rect(ecran, (210, 160, 255), avant, border_radius=2)
