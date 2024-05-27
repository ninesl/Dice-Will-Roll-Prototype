import pygame as pg

class SoundService:
    def __init__(self):
        self.music = pg.mixer.Sound("assets/audio/theme.mp3")
        self.masterVolume = .05

        self.diceDict = {
            "roll": pg.mixer.Sound("assets/audio/dice/rollDice.wav"),
            "stop": pg.mixer.Sound("assets/audio/dice/stopRollDice.wav"),
            "select": pg.mixer.Sound("assets/audio/dice/selectDie.wav"),
            "deselect": pg.mixer.Sound("assets/audio/dice/deselectDie.wav"),
            "tap": pg.mixer.Sound("assets/audio/dice/tap.wav"),
            "error": pg.mixer.Sound("assets/audio/dice/error.wav"),
            "preview": pg.mixer.Sound("assets/audio/dice/preview.wav")
        }
        self.hitDict = {
            "light": pg.mixer.Sound("assets/audio/hit/lightHit.wav"),
            "mid":   pg.mixer.Sound("assets/audio/hit/midHit.wav"),
            "big":   pg.mixer.Sound("assets/audio/hit/bigHit.wav"),
            "none":   pg.mixer.Sound("assets/audio/hit/noHit.wav")
        }
        self.shopDict = {
            "ding": pg.mixer.Sound("assets/audio/shop/ding.wav")
        }

    def playMusic(self):
        self.music.play(-1)
        self.music.set_volume(self.masterVolume)

    def selectDiceSound(self, isSelected):
        soundToPlay = self.diceDict["deselect"]
        if isSelected:
            soundToPlay = self.diceDict["select"]
        soundToPlay.play()
        # soundToPlay.set_volume(self.masterVolume * 3)

    def diceRollSound(self, rollsLeft):
        soundToPlay = self.diceDict["stop"]
        if rollsLeft > 0:
            soundToPlay = self.diceDict["roll"]
        soundToPlay.play()
        # soundToPlay.set_volume(self.masterVolume)

    def hitSound(self, scoredHandNum):
        soundToPlay = self.hitDict["none"]
        soundToPlay.set_volume(self.masterVolume)

        if scoredHandNum:
            if scoredHandNum >= 35:
                soundToPlay = self.hitDict["big"]
            elif scoredHandNum >= 15:
                soundToPlay = self.hitDict["mid"]
            else:
                soundToPlay = self.hitDict["light"]

        soundToPlay.play()