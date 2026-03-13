import pygame


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_survol, couleur_texte=(20, 20, 20)):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_survol = couleur_survol
        self.couleur_texte = couleur_texte
        self.est_survole = False

    def dessiner(self, ecran, police):
        couleur_active = self.couleur_survol if self.est_survole else self.couleur

        ombre = self.rect.move(0, 4)
        pygame.draw.rect(ecran, (10, 10, 20), ombre, border_radius=14)
        pygame.draw.rect(ecran, couleur_active, self.rect, border_radius=14)
        pygame.draw.rect(ecran, (235, 235, 245), self.rect, 2, border_radius=14)

        surface_texte = police.render(self.texte, True, self.couleur_texte)
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        ecran.blit(surface_texte, rect_texte)

    def verifier_survol(self, position):
        self.est_survole = self.rect.collidepoint(position)
        return self.est_survole

    def est_clique(self, position, evenement):
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            return self.rect.collidepoint(position)
        return False


# Compatibilite anciens imports
Button = Bouton
