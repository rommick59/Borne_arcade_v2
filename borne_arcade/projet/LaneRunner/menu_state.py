class EtatMenu:
    def __init__(self):
        self.index = 0

    def haut(self):
        self.index = (self.index - 1) % 2

    def bas(self):
        self.index = (self.index + 1) % 2

    @property
    def jouer_selectionne(self) -> bool:
        return self.index == 0
