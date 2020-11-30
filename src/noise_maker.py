from playsound import playsound

class NoiseMaker:
    def __init__(self, path_sound):
        self._path_sound = path_sound
    

    def play(self):
        playsound(self._path_sound)