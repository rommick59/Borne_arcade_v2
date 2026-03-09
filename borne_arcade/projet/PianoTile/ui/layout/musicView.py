import pygame
from ui.utils.image import Image

class MusicView:
    def __init__(self, windowManager):
        self.__windowManager = windowManager

    def affichageListeMusique(self):
        """Affiche une liste defilante de musiques dans une zone scrollable."""

        area = self.__windowManager.getAreaMusic()
        surface = pygame.Surface((area.width, area.height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        title_to_cover = {
            "SUNFLOWER": "SUNFLOWER",
            "SWEATER WEATHER": "SWEATERWEATHER",
            "BELIEVER": "BELIEVER",
            "BLINDING LIGHTS": "BLINDINGLIGHTS",
        }

        for index, music in enumerate(self.__windowManager.getInterface().getGame().getDatabase().getMusicSorted(self.__windowManager.getSorted().getDifficulte(), self.__windowManager.getSorted().getAnnee())):
            top_y = index * 210 - self.__windowManager.getScrollOffset()
            if top_y + 200 < 0 or top_y > area.height:
                continue  # hors de la zone visible

            rect = pygame.Rect(0, top_y, area.width, 200)
            pygame.draw.rect(surface, self.__windowManager.getColor().getRose(), rect)

            cover_key = title_to_cover.get(music[1].upper(), music[1].upper().replace(" ", "").replace("'", "").replace(",", ""))
            cover_img = getattr(Image.Cover, cover_key, Image.Cover.SUNFLOWER)
            surface.blit(cover_img, cover_img.get_rect(left=rect.left, centery=rect.centery))

            title = self.__windowManager.getFontSmall().render(f"{music[1]} - {music[2]}", True, self.__windowManager.getColor().getBlanc())
            surface.blit(title, title.get_rect(left=rect.left + 250, centery=rect.top + 60))

            rect_bouton = pygame.Rect(rect.left + 250, rect.top + 135, 200, 50)
            pygame.draw.rect(surface, self.__windowManager.getColor().getViolet(), rect_bouton)
            detail_button_text = self.__windowManager.getFontSmall().render("Details", True, self.__windowManager.getColor().getBlanc())
            surface.blit(detail_button_text, detail_button_text.get_rect(center=rect_bouton.center))

            if music[5] == "Easy":
                color = self.__windowManager.getColor().getVert()
            elif music[5] == "Medium":
                color = self.__windowManager.getColor().getOrange()
            elif music[5] == "Hard":
                color = self.__windowManager.getColor().getRouge()
            else:
                color = self.__windowManager.getColor().getBlanc()

            pygame.draw.polygon(surface, color, [(rect.right - 210, rect.top), (rect.right - 250, rect.top), (rect.right - 210, rect.top + 49)])
            rect_diff = pygame.Rect(rect.right - 210, rect.top, 210, 50)
            pygame.draw.rect(surface, color, rect_diff)
            label_diff = self.__windowManager.getFontSmall().render(f"{music[5]}", True, self.__windowManager.getColor().getBlanc())
            surface.blit(label_diff, label_diff.get_rect(center=rect_diff.center))

            rect_play = pygame.Rect(rect.right - 210, rect.top + 70, 200, 115)
            pygame.draw.rect(surface, self.__windowManager.getColor().getViolet(), rect_play)
            label_play = self.__windowManager.getFontSmall().render("Play", True, self.__windowManager.getColor().getBlanc())
            surface.blit(label_play, label_play.get_rect(center=rect_play.center))

        self.__windowManager.getWindow().blit(surface, area.topleft, area=pygame.Rect(0, 0, area.width, area.height))
