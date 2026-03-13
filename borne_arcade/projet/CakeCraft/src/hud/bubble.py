import pygame

class Bubble:
    """Bulle HUD de base avec fond blanc et bordure dorée en dégradé pixel art"""
    
    def __init__(self, x: int, y: int, width: int, height: int, padding: int = 8):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding  # Espacement interne réduit
        self.rect = pygame.Rect(x, y, width, height)
        
        # Couleurs pour le dégradé doré (pixel art style)
        self.gold_colors = [
            (255, 215, 0),   # Or vif
            (255, 200, 0),   # Or moyen
            (255, 180, 0),   # Or foncé
            (255, 160, 0),   # Or très foncé
        ]
        
    def draw(self, screen: pygame.Surface):
        """Dessine la bulle avec fond blanc et bordure dorée dégradée"""
        # Fond blanc
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        
        # Bordure dorée en dégradé pixel art
        self._draw_gradient_border(screen)
        
    def _draw_gradient_border(self, screen: pygame.Surface):
        """Dessine une bordure avec dégradé doré style pixel art"""
        border_width = 3
        
        # Bordure haute (dégradé gauche → droite)
        for i in range(self.width):
            color_index = min(i // (self.width // len(self.gold_colors)), len(self.gold_colors) - 1)
            color = self.gold_colors[color_index]
            for bw in range(border_width):
                pygame.draw.rect(screen, color, (self.x + i, self.y + bw, 1, 1))
                pygame.draw.rect(screen, color, (self.x + i, self.y + self.height - 1 - bw, 1, 1))
        
        # Bordure gauche (dégradé haut → bas)
        for i in range(self.height):
            color_index = min(i // (self.height // len(self.gold_colors)), len(self.gold_colors) - 1)
            color = self.gold_colors[color_index]
            for bw in range(border_width):
                pygame.draw.rect(screen, color, (self.x + bw, self.y + i, 1, 1))
                pygame.draw.rect(screen, color, (self.x + self.width - 1 - bw, self.y + i, 1, 1))
        
        # Coins renforcés pour l'effet pixel art
        corner_size = 4
        for cx in range(corner_size):
            for cy in range(corner_size):
                # Coin haut gauche
                pygame.draw.rect(screen, self.gold_colors[0], (self.x + cx, self.y + cy, 1, 1))
                # Coin haut droit
                pygame.draw.rect(screen, self.gold_colors[-1], (self.x + self.width - 1 - cx, self.y + cy, 1, 1))
                # Coin bas gauche
                pygame.draw.rect(screen, self.gold_colors[-1], (self.x + cx, self.y + self.height - 1 - cy, 1, 1))
                # Coin bas droit
                pygame.draw.rect(screen, self.gold_colors[0], (self.x + self.width - 1 - cx, self.y + self.height - 1 - cy, 1, 1))


class TextBubble(Bubble):
    """Bulle spécialisée pour afficher du texte"""
    
    def __init__(self, x: int, y: int, width: int, height: int, padding: int = 8):
        super().__init__(x, y, width, height, padding)
    
    def draw_text(self, screen: pygame.Surface, text: str, font: pygame.font.Font, 
                  text_color: tuple = (50, 50, 50), centered: bool = True):
        """Dessine du texte dans la bulle avec padding optimisé"""
        text_surface = font.render(text, True, text_color)
        
        if centered:
            text_rect = text_surface.get_rect(center=self.rect.center)
        else:
            text_rect = text_surface.get_rect(topleft=(self.x + self.padding, self.y + self.padding))
            
        screen.blit(text_surface, text_rect)


class ProgressBubble(Bubble):
    """Bulle spécialisée pour afficher une barre de progression"""
    
    def __init__(self, x: int, y: int, width: int, height: int, padding: int = 5):
        super().__init__(x, y, width, height, padding)
    
    def _get_progress_color(self, progress: float) -> tuple:
        """Calcule la couleur de la barre de progression: vert(0-1) -> orange(1-1.5) -> rouge(1.5-2)"""
        if progress <= 1.0:
            # Vert (0% à 100%)
            return (100, 200, 100)
        elif progress <= 1.5:
            # Orange (100% à 150%)
            t = (progress - 1.0) / 0.5  # 0 à 1
            r = int(100 + t * 155)  # 100 -> 255
            g = int(200 - t * 100)  # 200 -> 100
            b = int(100 - t * 100)  # 100 -> 0
            return (r, g, b)
        else:
            # Rouge (150% à 200%)
            return (255, 100, 100)
    
    def draw_progress_bar(self, screen: pygame.Surface, progress: float):
        """Dessine une barre de progression dans la bulle avec dégradé de couleur"""
        bar_height = self.height - 2 * self.padding  # Hauteur avec padding pour ne pas dépasser les bordures
        bar_y = self.y + self.padding  # Position avec padding
        bar_x = self.x + self.padding
        bar_width = self.width - 2 * self.padding  # Largeur avec padding des deux côtés
        
        # Progression avec couleur dynamique
        bar_color = self._get_progress_color(progress)
        
        # Gérer la progression au-delà de 100%
        if progress <= 1.0:
            progress_width = int(bar_width * progress)
        else:
            # La barre reste pleine mais change de couleur
            progress_width = bar_width
            
        # Dessiner seulement la progression (pas de fond)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, progress_width, bar_height))
        
        # Bordure fine autour de la zone de progression
        pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, bar_width, bar_height), 1)


# Fonction de test
def test_bubble():
    """Test d'affichage de deux bulles: texte seul et barre de progression seule"""
    pygame.init()
    screen = pygame.display.set_mode((500, 250))
    pygame.display.set_caption("Test Bubble HUD")
    clock = pygame.time.Clock()
    
    # Créer deux bulles optimisées
    bubble_text = TextBubble(20, 30, 220, 80, padding=8)      # Bulle de texte
    bubble_progress = ProgressBubble(260, 50, 220, 40, padding=5)  # Bulle de progression compacte
    
    font_title = pygame.font.Font(None, 18)
    font_small = pygame.font.Font(None, 14)
    
    progress = 0.0
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    progress = 0.0
        
        # Animation de la barre de progression jusqu'à 200%
        progress = min(progress + dt * 0.3, 2.0)
        
        # Effacer l'écran
        screen.fill((100, 100, 120))
        
        # Bulle 1: Texte seulement
        bubble_text.draw(screen)
        bubble_text.draw_text(screen, "Bubble Texte Seul", font_title, centered=True)
        bubble_text.draw_text(screen, "Contenu texte uniquement", font_small, (80, 80, 80), centered=False)
        
        # Bulle 2: Barre de progression seulement
        bubble_progress.draw(screen)
        bubble_progress.draw_progress_bar(screen, progress)
        
        # Instructions
        inst_font = pygame.font.Font(None, 14)
        inst_text = inst_font.render("SPACE: reset | ESC: quit", True, (255, 255, 255))
        screen.blit(inst_text, (10, screen.get_height() - 20))
        
        # Labels pour identifier les bulles
        label_font = pygame.font.Font(None, 12)
        label1 = label_font.render("Texte:", True, (200, 200, 200))
        label2 = label_font.render("Progression:", True, (200, 200, 200))
        screen.blit(label1, (20, 15))
        screen.blit(label2, (260, 35))
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    test_bubble()
