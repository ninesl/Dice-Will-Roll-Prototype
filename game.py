import pygame as pg
import dice
import graphics
import events
import logic

d = dice.Die(6)

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)
# music = pg.mixer.Sound("audio/rs.mp3")
# music.play(-1)
# music.set_volume(.3)

clock = pg.time.Clock()

WIDTH = 1600
HEIGHT = 900

DrawService = graphics.DrawService(WIDTH, HEIGHT)
EventService = events.EventService()
LogicService = logic.LogicService()

going = True

playerDice = []
for i in range(5):
    playerDice.append(dice.Die(6))

total = 0
for die in playerDice:
    die.rollDie()

while going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.VIDEORESIZE:
            DrawService.setScreen(event.w, event.h)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                EventService.findRectClicked(diceAndRect)
                LogicService.addDice(playerDice)
                
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                LogicService.rollDice(playerDice)
            if event.key == pg.K_ESCAPE:
                going = False

    DrawService.resetFrame()
    diceAndRect = DrawService.drawDice(playerDice) #returns list of (die, rect) for EventService
    DrawService.drawValue(LogicService.total)

    pg.display.flip()
    clock.tick(60)
