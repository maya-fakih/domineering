import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "place_v": pygame.mixer.Sound("assets/sounds/place_v.wav"),
            "place_h": pygame.mixer.Sound("assets/sounds/place_h.wav"),
            "win": pygame.mixer.Sound("assets/sounds/win.wav"),
        }

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
