import pygame as pg
import dice
import graphics
import events
import logic
import animate

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)
# music = pg.mixer.Sound("audio/rs.mp3")
# music.play(-1)
# music.set_volume(.3)

clock = pg.time.Clock()

WIDTH = 1920
HEIGHT = 1080

DrawService = graphics.DrawService(WIDTH, HEIGHT)
EventService = events.EventService()
LogicService = logic.LogicService()
AnimateService = animate.AnimateService(DrawService, clock)

going = True

playerDice = []

playerDice.append(dice.Die(6, pg.Color(255,255,255)))
playerDice.append(dice.Die(6, pg.Color(255,0,255)))
playerDice.append(dice.Die(6, pg.Color(255,255,0)))
playerDice.append(dice.Die(6, pg.Color(0,255,255)))
playerDice.append(dice.Die(6, pg.Color(100,100,100)))

total = 0
for die in playerDice:
    die.rollDie()

#TODO FPS math?
while going:
    # playerDice.sort(key=lambda x: x.curSide.getPips(), reverse=True)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.VIDEORESIZE:
            DrawService.setScreen(event.w, event.h)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                EventService.selectRectDie(diceAndRect)
                LogicService.addDice(playerDice)
                
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                AnimateService.shakeDice(playerDice)
                LogicService.rollDice(playerDice)
            if event.key == pg.K_ESCAPE:
                going = False


    DrawService.resetFrame()
    diceAndRect = DrawService.drawDice(playerDice) #returns list of (die, rect) for EventService
    LogicService.findHand(playerDice)
    DrawService.drawValue(LogicService.hand.value)
                
    EventService.dieHovered(diceAndRect)

    pg.display.flip()
    clock.tick(60)
