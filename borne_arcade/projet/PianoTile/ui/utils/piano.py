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
        print("Generation des notes (sans librosa) depuis :", self.__filepath)

        # On estime la duree de la piste pour espacer les notes
        try:
            track = pygame.mixer.Sound(self.__filepath)
            song_length = track.get_length()
        except Exception as exc:  # pragma: no cover - depend des codecs dispo
            print("Impossible de lire la duree du morceau, fallback 60s:", exc)
            song_length = 60.0

        tempo_bpm = 120  # rythme par defaut
        beat_interval = 60.0 / tempo_bpm

        notes = []
        current_time = 0.0
        while current_time <= song_length:
            nb_notes = min(self.__difficulty, random.randint(1, 3))
            for _ in range(nb_notes):
                position = random.choice(["left", "middle", "right", "top"])
                notes.append(Note(gameview=self.__gameView, position=position, timestamp=current_time))
            current_time += beat_interval

        print(f"{len(notes)} notes generees sur {song_length:.1f}s (tempo {tempo_bpm} BPM).")
        return notes

    def getCurrentTime(self):
        return pygame.mixer.music.get_pos() / 1000.0
