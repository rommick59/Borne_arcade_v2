import pygame, random, subprocess
from ui.utils.note import Note

def _get_audio_duration(filepath):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", filepath],
            capture_output=True, text=True, timeout=5
        )
        return float(result.stdout.strip())
    except Exception:
        return 240.0  # fallback 4 minutes

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
        song_length = _get_audio_duration(self.__filepath)

        tempo_bpm = 80
        beat_interval = 60.0 / tempo_bpm

        notes = []
        current_time = 0.0
        while current_time <= song_length:
            # Une seule note par temps pour réduire la charge
            position = random.choice(["left", "middle", "right", "top"])
            notes.append(Note(gameview=self.__gameView, position=position, timestamp=current_time))
            current_time += beat_interval

        return notes

    def getCurrentTime(self):
        return pygame.mixer.music.get_pos() / 1000.0
