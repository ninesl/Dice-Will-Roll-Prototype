import pygame as pg

class EventService:
    def __init__(self):
        self.update_pos()

    def update_pos(self):
        self.pos = pg.mouse.get_pos()

    def clickable(self, rect):
        print("got here")
        return rect.collidepoint(self.pos)
    
    def findRectClicked(self, diceAndRect):
        self.update_pos()  # Update the position each time a click is detected
        for die, rect in diceAndRect:
            if rect.collidepoint(pg.mouse.get_pos()):
                die.select()
