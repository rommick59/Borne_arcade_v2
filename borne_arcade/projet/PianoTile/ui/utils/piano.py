import pygame, random
from ui.utils.note import Note

class Piano:
    def __init__(self, gameview):
        self.__gameView = gameview
        self.__filepath = "./assets/music/" + self.__gameView.getWindowManager().getMusicSelect().lower().replace('play musique ', '').replace(' ', '').replace("'", '').replace(',', '') + ".mp3"
        self.__difficulty = 1
        self.__notes = self.generate_notes()

    def getNotes(self):
        return self.__notes

    def setNotes(self, notes):
        self.__notes = notes

    def increaseDifficulty(self):
        self.__difficulty += 1

    def play(self):
        pygame.mixer.music.load(self.__filepath)
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def generate_notes(self):
        # Génération allégée des notes : on limite la fenêtre temporelle
        # et le nombre de notes pour réduire mémoire/CPU sur la borne (1 Go RAM).
        song_length = 60.0
        max_window = min(song_length, 30.0)  # ne générer que 30s max

        tempo_bpm = 80  # tempo réduit pour moins d'objets à l'écran
        beat_interval = 60.0 / tempo_bpm

        notes = []
        current_time = 0.0
        while current_time <= max_window:
            # Une seule note par temps pour réduire la charge
            position = random.choice(["left", "middle", "right", "top"])
            notes.append(Note(gameview=self.__gameView, position=position, timestamp=current_time))
            current_time += beat_interval

        return notes

    def getCurrentTime(self):
        return pygame.mixer.music.get_pos() / 1000.0
