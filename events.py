import pygame as pg

class EventService:
    def __init__(self):
        self.update_pos()

    def update_pos(self):
        self.pos = pg.mouse.get_pos()
    
    def selectRectDie(self, diceAndRect):
        self.update_pos() # Update the position each time a click is detected
        for die, rect in diceAndRect:
            if rect.collidepoint(self.pos):
                die.select()
                return die

    def dieHovered(self, diceAndRect):
        self.update_pos()
        for die, rect in diceAndRect:
            if rect.collidepoint(self.pos):
                die.isHovered = True
            if not rect.collidepoint(self.pos):
                die.isHovered = False