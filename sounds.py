import pygame as pg

class SoundService:
    def __init__(self):
        self.music = pg.mixer.Sound("assets/audio/theme.mp3")
        self.music.play(-1)
        self.music.set_volume(.3)