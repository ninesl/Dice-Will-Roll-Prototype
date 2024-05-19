import pygame as pg
import random as rand
import dice
import graphics
import events
import logic
import sounds
import animate

class GameController:
    BACKGROUND_COLOR_RANGE = 150
    STARTING_ROCKS = 200
    GOING = True

    def __init__(self, monitor):
        self.monitor = monitor

        self.WIDTH  = int(monitor.current_w * 3 / 4)
        self.HEIGHT = int(monitor.current_h * 3 / 4)

        self.setDice()
        self.recentHandScore = None

        self.SoundService = sounds.SoundService()
        self.setServices()

        self.SoundService.playMusic()

    def quitGame(self):
        self.GOING = False

    def resizeScreen(self, eventW, eventH):
        self.WIDTH = eventW
        self.HEIGHT = eventH
        self.LogicService.unselectAll()
        
        self.DrawService = graphics.DrawService(self.WIDTH, self.HEIGHT, NUM_SHAPES=self.LogicService.rockHealth, rangeNum=self.BACKGROUND_COLOR_RANGE)
        self.AnimateService = animate.AnimateService(self.DrawService)

    def isFinishedLoading(self):
        return self.DrawService and self.AnimateService and self.EventService and self.LogicService and self.SoundService

    def setServices(self):
        self.DrawService    = graphics.DrawService(self.WIDTH, self.HEIGHT, NUM_SHAPES=self.STARTING_ROCKS, rangeNum=self.BACKGROUND_COLOR_RANGE)
        self.AnimateService = animate.AnimateService(self.DrawService)
        self.EventService   = events.EventService()
        self.LogicService   = logic.LogicService(self.playerDice, self.DrawService)

    def setDice(self):
        self.playerDice = []
        
        rangeMin, rangeMax = 0,255
        self.playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                                    rand.randint(rangeMin, rangeMax),
                                                    rand.randint(rangeMin, rangeMax))))
        self.playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                                    rand.randint(rangeMin, rangeMax),
                                                    rand.randint(rangeMin, rangeMax))))
        self.playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                                    rand.randint(rangeMin, rangeMax),
                                                    rand.randint(rangeMin, rangeMax))))
        self.playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                                    rand.randint(rangeMin, rangeMax),
                                                    rand.randint(rangeMin, rangeMax))))
        self.playerDice.append(dice.Die(6, pg.Color(rand.randint(rangeMin, rangeMax), 
                                                    rand.randint(rangeMin, rangeMax),
                                                    rand.randint(rangeMin, rangeMax))))
            
        for die in self.playerDice:
            die.rollDie()

    def selectDie(self):
        d = self.EventService.selectRectDie(self.diceAndRect)
        if d:
            self.SoundService.selectDiceSound(d.isSelected)
        else:
            self.SoundService.diceDict["tap"].play()
        self.LogicService.addDice()
        self.DrawService.BackgroundService.changeShapeColors(self.LogicService.getSelectedDice(), d)

    def rollDice(self):
        # DrawService.BackgroundService.changeDirection()
        self.AnimateService.shakeDice(self.playerDice)
        self.SoundService.diceRollSound(self.LogicService.rollsLeft)
        self.LogicService.rollDice()


    def scoreDice(self):
        self.AnimateService.shakeDice(self.playerDice, selected=True)
        self.recentHandScore = self.LogicService.score()
        self.SoundService.hitSound(self.recentHandScore)
     
    def resetLevel(self):
        self.LogicService.unselectAll()
        self.LogicService.rollDice()
        self.setServices()
    
    def harderLevel(self):
        self.LogicService.unselectAll()
        self.LogicService.rollDice()

        self.BACKGROUND_COLOR_RANGE -= rand.randint(15,25)
        if self.BACKGROUND_COLOR_RANGE <= 15:
            self.BACKGROUND_COLOR_RANGE = 15
        self.STARTING_ROCKS += 50
        
        self.setServices()

    def levelLoop(self):
        self.DrawService.resetFrame()
        #returns list of (die, rect) for EventService
        self.diceAndRect = self.DrawService.drawDice(self.playerDice)
        self.EventService.dieHovered(self.diceAndRect)
        self.LogicService.findHand()
        self.DrawService.drawTextContent(self.LogicService)