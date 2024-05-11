import pygame as pg
import dice

# initializes and returns main screen
def startScreen(WIDTH, HEIGHT):
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screenColor = pg.Color(0,0,0)
    screen.fill(screenColor)
    return screen

def drawDice(d, screen):
    screen.blit