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

music = pg.mixer.Sound("assets/audio/theme.mp3")
music.play(-1)
music.set_volume(.3)


clock = pg.time.Clock()

WIDTH = 1920
HEIGHT = 1080
NUM_SHAPES = 250

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

DrawService = graphics.DrawService(WIDTH, HEIGHT)
EventService = events.EventService()
LogicService = logic.LogicService(playerDice)
AnimateService = animate.AnimateService(DrawService)
Background = shapes.Background(WIDTH, HEIGHT, NUM_SHAPES, len(playerDice))


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
            Background = shapes.Background(event.w, event.h, NUM_SHAPES, playerDice)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                EventService.selectRectDie(diceAndRect)
                LogicService.addDice()
                Background.changeShapeColors(LogicService.getSelectedDice())

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # Background.changeDirection()
                AnimateService.shakeDice(playerDice)
                LogicService.rollDice()
            if event.key == pg.K_ESCAPE:
                going = False



    DrawService.resetFrame()
    Background.runBackground(DrawService.screen)
    
    diceAndRect = DrawService.drawDice(playerDice) #returns list of (die, rect) for EventService
    LogicService.findHand()
    DrawService.drawValue(LogicService.hand.value[0])
                
    EventService.dieHovered(diceAndRect)

    pg.display.update()
    clock.tick(60)
