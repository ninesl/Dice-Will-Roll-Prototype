import pygame as pg
import dice
import graphics

d = dice.Die(6)



# print(top)
# print(results)

pg.init()
pg.display.set_caption("Dwarf Dice")
# music = pg.mixer.Sound("audio/rs.mp3")
# music.play(-1)
# music.set_volume(.3)

clock = pg.time.Clock()

WIDTH = 1920
HEIGHT = 1080
screen = graphics.startScreen(WIDTH, HEIGHT)

going = True
while going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False 