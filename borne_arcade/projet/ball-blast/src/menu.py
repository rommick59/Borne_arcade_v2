"""
Module contenant la gestion de l'interface de menu du jeu
"""

import pygame

from constantes import WHITE, BLACK, RED, GREEN, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT, FONT, SELECT_KEY, BACK_KEY
from input_helper import is_pressed


class Menu:
    """
    Classe gérant l'interface de menu du jeu
    
    Attributes:
        screen (pygame.Surface): Surface de dessin de l'écran
        selectedOption (int): Option sélectionnée dans le menu
        texture (pygame.Surface): Texture d'arrière-plan du menu
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialise l'objet menu
        
        Args:
            screen (pygame.Surface): Surface de dessin de l'écran
            
        Raises:
            None
        """
        self.screen: pygame.Surface = screen
        self.selectedOption: int = 0
        self.texture: pygame.Surface = pygame.transform.scale(
            pygame.image.load('./assets/bg_pxl.jpg').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def showMenu(self, keyEvent, pause: bool = False) -> tuple[bool, bool, bool]:
        """
        Affiche l'interface de menu et gère les interactions
        
        Args:
            keyEvent: Liste des événements clavier (pygame.event.Event)
            pause (bool): Indique si le menu est affiché en pause
            
        Returns:
            tuple[bool, bool, bool]: 
                - goTogame: Indique si le jeu doit reprendre
                - newGame: Indique si une nouvelle partie doit commencer
                - credits: Indique si l'écran des crédits doit s'afficher
            
        Raises:
            None
        """
        newGame: bool = False
        credits: bool = False
        if pause:
            numberOfOptions = 3
        else:
            numberOfOptions = 2

        goTogame: bool = False
        for event in keyEvent:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selectedOption == numberOfOptions:
                        self.selectedOption = 0
                    else:
                        self.selectedOption += 1

                if event.key == pygame.K_UP:
                    if self.selectedOption == 0:
                        self.selectedOption = numberOfOptions
                    else:
                        self.selectedOption -= 1

                if event.key == SELECT_KEY:
                    if pause:
                        if self.selectedOption == 0:
                            goTogame = True
                        elif self.selectedOption == 1:
                            newGame = True
                            goTogame = True
                        elif self.selectedOption == 2:
                            credits = True
                        elif self.selectedOption == 3:
                            pygame.quit()
                            exit(0)
                    else:
                        if self.selectedOption == 0:
                            goTogame = True
                            newGame = True
                        elif self.selectedOption == 1:
                            credits = True
                        elif self.selectedOption == 2:
                            pygame.quit()
                            exit(0)

                if event.key == pygame.K_q:
                    pygame.quit()
                    exit(0)

        self.screen.blit(self.texture, (0, 0))

        delta = 100 if pause else 0

        if pause:
            text_surface = FONT.render('REPRENDRE', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            text_surface = FONT.render('NOUVELLE PARTIE', False, (0, 0, 0))
            self.screen.blit(text_surface, (SCREEN_WIDTH //
                                            2, SCREEN_HEIGHT // 2 + 100))
        else:
            text_surface = FONT.render('COMMENCER', False, (0, 0, 0))
            self.screen.blit(
                text_surface, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
        text_surface = FONT.render(
            'BALL BLAST', False, (0, 0, 0))
        
        self.screen.blit(text_surface, (SCREEN_WIDTH //
                                        2, (SCREEN_HEIGHT // 2) - 200))

        text_surface = FONT.render(
            'CRÉDITS', False, (0, 0, 0))  # Merci
        self.screen.blit(text_surface, (SCREEN_WIDTH //
                                        2, (SCREEN_HEIGHT // 2) + 100 + delta))

        text_surface = FONT.render('QUITTER', False, (0, 0, 0))
        self.screen.blit(text_surface, (SCREEN_WIDTH //
                                        2, (SCREEN_HEIGHT // 2) + 200 + delta))

        pygame.draw.circle(self.screen, WHITE, ((SCREEN_WIDTH // 2) - 50,
                           (SCREEN_HEIGHT // 2) + 100 * self.selectedOption + 25), 5)

        return goTogame, newGame, credits
    
    def showCredits(self) -> bool:
        """
        Affiche l'écran des crédits et gère la navigation
        
        Returns:
            bool: True si l'écran des crédits doit rester affiché, False pour revenir au menu
            
        Raises:
            None
        """
        self.screen.blit(self.texture, (0, 0))
        
        # Titre "PRODUIT PAR:"
        title_text = FONT.render('PRODUIT PAR:', False, (0, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title_text, title_rect)
        
        # Premier développeur
        dev1_text = FONT.render('Justin FONTAINE', False, (0, 0, 0))
        dev1_rect = dev1_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(dev1_text, dev1_rect)
        
        # Deuxième développeur
        dev2_text = FONT.render('Arnaud WISSOCQ', False, (0, 0, 0))
        dev2_rect = dev2_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(dev2_text, dev2_rect)
        
        # Instruction pour revenir
        back_text = FONT.render('Appuyez sur Retour pour revenir', False, (0, 0, 0))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(back_text, back_rect)
        
        if is_pressed(BACK_KEY):
            return False
        
        return True