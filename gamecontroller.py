import pygame as pg
import random as rand
import dice
import graphics
import events
import logic
import sounds
import animate
from enum import Enum

class GameController:
    BACKGROUND_COLOR_RANGE = 190
    STARTING_ROCKS = 10
    GOING = True

    def __init__(self, monitor, clock, fps):
        self.monitor = monitor
        self.clock = clock
        self.fps = fps

        self.currentState = LevelState.LEVEL

        self.WIDTH  = int(monitor.current_w * 8.5/10)
        self.HEIGHT = int(monitor.current_h * 8.5/10)
        # self.WIDTH = 1600
        # self.HEIGHT = 900

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
        self.AnimateService = animate.AnimateService(self.DrawService, self.clock, self.fps, self.SoundService)

    def isFinishedLoading(self):
        return self.DrawService and self.AnimateService and self.EventService and self.LogicService and self.SoundService

    def setServices(self):
        self.DrawService    = graphics.DrawService(self.WIDTH, self.HEIGHT, NUM_SHAPES=self.STARTING_ROCKS, rangeNum=self.BACKGROUND_COLOR_RANGE)
        self.AnimateService = animate.AnimateService(self.DrawService, self.clock, self.fps, self.SoundService)
        self.EventService   = events.EventService()
        self.LogicService   = logic.LogicService(self.playerDice, self.DrawService)

    def newDice(self):
        self.playerDice.append(dice.Die(6, 
                                        pg.Color(rand.randint(self.rangeDieMin, self.rangeDieMax), 
                                                 rand.randint(self.rangeDieMin, self.rangeDieMax), 
                                                 rand.randint(self.rangeDieMin, self.rangeDieMax))))
        self.rangeDieMin -= 15
        self.rangeDieMax -= 15


    numStartDice = 1
    def setDice(self):
        self.playerDice = []
        self.rangeDieMin, self.rangeDieMax = 250,255
        for _ in range(self.numStartDice):
            self.newDice()
            
            
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
        self.LogicService.score()

    def resetLevel(self):
        self.LogicService.unselectAll()
        self.LogicService.rollDice()
        self.setServices()
    
    def harderLevel(self):
        self.LogicService.unselectAll()
        self.LogicService.rollDice()

        self.BACKGROUND_COLOR_RANGE -= rand.randint(5,15)
        if self.BACKGROUND_COLOR_RANGE <= self.DrawService.BACKGROUND_COLOR_RANGE_DIFF:
            self.BACKGROUND_COLOR_RANGE = self.DrawService.BACKGROUND_COLOR_RANGE_DIFF
        self.STARTING_ROCKS += 25
        
        self.setServices()

    def levelLoop(self):
        #returns list of (die, rect) for EventService
        self.diceAndRect = self.DrawService.drawDice(self.playerDice, self.LogicService.scoringHandDice)
        self.EventService.dieHovered(self.diceAndRect)
        self.LogicService.findHand()
        self.DrawService.drawPreviousHands()

        if self.LogicService.isNextLevel():
            self.DrawService.drawText(2, "Level Completed!", 0,-self.DrawService.heightGrid * 1.5, center=True)
            self.DrawService.drawText(2, f"W to go to the shop", 0,-self.DrawService.heightGrid * .75, center=True)
            return
        
        self.DrawService.drawLevelText(self.LogicService)
        self.AnimateService.animateScoringHand(self.LogicService)

    def shopLoop(self):
        self.diceAndRect = self.DrawService.drawAllDiceFaces(self.playerDice)

    def gameLoop(self):
        self.DrawService.resetFrame()
        self.DrawService.drawControlsText(self.currentState.value)
        match self.currentState:
            case LevelState.LEVEL:
                self.levelLoop()
            case LevelState.SHOP:
                self.shopLoop()

    def goToShop(self):
        self.currentState = LevelState.SHOP
    def goToLevel(self):
        self.currentState = LevelState.LEVEL

class LevelState(Enum):
    SHOP  =["yes"]
    LEVEL =["  hold : click",
            "  roll : space",
            " score : Q key",
        #   " reset : P key",
        #   "harder : O key",
            "  quit :   esc"]