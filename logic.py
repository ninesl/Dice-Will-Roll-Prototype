import pygame as pg

class LogicService:
    def __init__(self):
        self.total = 0

    def addDice(self, playerDice):
        self.total = 0
        for die in playerDice:
            if die.isSelected:
                self.total += die.num
    
    def rollDice(self, playerDice):
        self.total = 0
        for die in playerDice:
            if die.isSelected:
                self.total += die.num
            else:
                die.rollDie()