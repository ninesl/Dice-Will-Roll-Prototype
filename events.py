import pygame as pg

class EventService:
    def __init__(self):
        self.update_pos()

    def update_pos(self):
        self.pos = pg.mouse.get_pos()
    
    def holdDie(self, diceRect):
        self.update_pos() # Update the position each time a click is detected
        for die, rect in diceRect:
            if rect.collidepoint(self.pos):
                die.select()
                return die

    def dieHovered(self, dicePipRect):
        self.update_pos()
        for die, rect in dicePipRect:
            if rect.collidepoint(self.pos):
                die.isHovered = True
            if not rect.collidepoint(self.pos):
                die.isHovered = False

    def selectPip(self, pipRect):
        self.update_pos()
        for pipTuples in pipRect:
            for pip, rect in pipTuples:
                if rect.collidepoint(self.pos):
                    return pip
                
    def selectButton(self, buttonRect):
        self.update_pos()
        for button, rect in buttonRect:
            if rect.collidepoint(self.pos):
                return button