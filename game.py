import pygame as pg
import random as rand
import dice
import graphics
import events
import logic
import shapes
import animate

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)

# music = pg.mixer.Sound("assets/audio/theme.mp3")
# music.play(-1)
# music.set_volume(.3)


clock = pg.time.Clock()

WIDTH = 1920
HEIGHT = 1080

playerDice = []
rangeMin, rangeMax = 0,255
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))
playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                       rand.randint(rangeMin, rangeMax),
                                       rand.randint(rangeMin, rangeMax))))

EventService = events.EventService()
LogicService = logic.LogicService(playerDice)

BACKGROUND_COLOR_RANGE = 100

DrawService = graphics.DrawService(WIDTH, HEIGHT, rangeNum=BACKGROUND_COLOR_RANGE)
AnimateService = animate.AnimateService(DrawService)


total = 0
for die in playerDice:
    die.rollDie()

going = True
#TODO FPS math?

while going:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.VIDEORESIZE:
            DrawService.setScreen(event.w, event.h)
            LogicService.unselectAll()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                d = EventService.selectRectDie(diceAndRect)
                LogicService.addDice()
            DrawService.BackgroundService.changeShapeColors(LogicService.getSelectedDice(), d)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # DrawService.BackgroundService.changeDirection()
                AnimateService.shakeDice(playerDice)
                LogicService.rollDice()
            #left and right arrow keys change background color
            elif event.key == pg.K_LEFT:
                BACKGROUND_COLOR_RANGE -= 15
                if BACKGROUND_COLOR_RANGE < 5:
                    BACKGROUND_COLOR_RANGE = 5
                else:
                    DrawService.setBackgroundColors(BACKGROUND_COLOR_RANGE, LogicService.getSelectedDice())
                    LogicService.unselectAll()
            elif event.key == pg.K_RIGHT:
                BACKGROUND_COLOR_RANGE += 15
                if BACKGROUND_COLOR_RANGE > 250:
                    BACKGROUND_COLOR_RANGE = 250
                else:
                    DrawService.setBackgroundColors(BACKGROUND_COLOR_RANGE, LogicService.getSelectedDice())
                    LogicService.unselectAll()
            elif event.key == pg.K_ESCAPE:
                going = False

    DrawService.resetFrame()

    #returns list of (die, rect) for EventService
    diceAndRect = DrawService.drawDice(playerDice)

    LogicService.findHand()

    DrawService.drawText(BACKGROUND_COLOR_RANGE, 2,HEIGHT / 10)
    DrawService.drawValue(LogicService.hand.value[0])
                
    EventService.dieHovered(diceAndRect)

    fps = int(clock.get_fps())
    DrawService.drawText(f"fps   {fps}", 2,HEIGHT / 10 * 2)

    pg.display.update()
    clock.tick(60)
