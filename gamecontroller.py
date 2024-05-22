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

    playerGold = 4
    goldToAdd = 0
    interest = 0

    def __init__(self, monitor, clock, fps):
        self.monitor = monitor
        self.clock = clock
        self.fps = fps

        self.currentState = LevelState.LEVEL

        self.WIDTH  = int(monitor.current_w * 7/10)
        self.HEIGHT = int(monitor.current_h * 7/10)
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

    def levelSelect(self):
        d = self.EventService.holdDie(self.dicePipRect[0])
        if d:
            self.SoundService.selectDiceSound(d.isSelected)

        button = self.EventService.selectButton(self.scoreButtonRect)
        if button:
            button.action()

        self.LogicService.addDice()
        self.DrawService.BackgroundService.changeShapeColors(self.LogicService.getSelectedDice(), d)

    def rollDice(self):
        self.DrawService.BackgroundService.changeDirection()
        self.AnimateService.shakeDice(self.playerDice)
        self.SoundService.diceRollSound(self.LogicService.rollsLeft)
        self.LogicService.rollDice()

    def scoreDice(self):
        self.LogicService.score()
        self.LogicService.updateGoldPips()

    def resetLevel(self):
        self.LogicService.startLevel(self.STARTING_ROCKS)
    
    def harderLevel(self):
        # self.LogicService.unselectAll()
        # self.LogicService.rollDice()
        self.BACKGROUND_COLOR_RANGE -= rand.randint(5,15)
        if self.BACKGROUND_COLOR_RANGE <= self.DrawService.BACKGROUND_COLOR_RANGE_DIFF:
            self.BACKGROUND_COLOR_RANGE = self.DrawService.BACKGROUND_COLOR_RANGE_DIFF
        self.STARTING_ROCKS = int(self.STARTING_ROCKS * 1.25)

    def levelLoop(self):
        #returns list of (die, rect) for EventService
        self.dicePipRect = self.DrawService.drawDice(self.playerDice, self.LogicService.scoringHandDice)

        self.EventService.dieHovered(self.dicePipRect[0])
        self.LogicService.findHand()
        self.DrawService.drawPreviousHands()

        self.scoreButtonRect = self.DrawService.drawButtons(self.levelButtons)

        if self.LogicService.isNextLevel():
            self.interest, self.goldToAdd, self.goldPipsThisLevel = self.LogicService.calculateGold(self.playerGold)

            self.DrawService.drawText(2, "Level Completed!", 0,-self.DrawService.heightGrid * 1.5, center=True)
            self.DrawService.drawText(1, f"stage clear: {self.goldToAdd} gold", 0,-self.DrawService.heightGrid // 2, center=True)
            self.DrawService.drawText(1, f"gold pips: {self.goldPipsThisLevel} gold", 0,0, center=True)
            self.DrawService.drawText(1, f"1g for every 5g owned - interest: {self.interest} gold", 0,self.DrawService.heightGrid // 2, center=True)
            self.DrawService.drawText(1, f"total gold gained: {self.interest + self.goldPipsThisLevel + self.goldToAdd} gold", 0,self.DrawService.heightGrid, center=True)
            
            self.levelButtons = self.otherButtons
            return
        
        self.DrawService.drawLevelText(self.LogicService)
        self.AnimateService.animateScoringHand(self.LogicService)

    def shopLoop(self):
        self.goldToAdd += self.goldPipsThisLevel
        self.goldPipsThisLevel = 0
        self.goldToAdd, self.playerGold = self.AnimateService.updateGold(self.playerGold, self.goldToAdd, self.WIDTH, self.HEIGHT)
        self.dicePipRect = self.DrawService.drawAllDiceFaces(self.playerDice) #pips
        self.shopButtonRect = self.DrawService.drawButtons(self.shopButtons)

    modGoldYes = None
    goldModPrice = 2
    atkModPrice = 1
    handPrice = 10
    rollPrice = 5
    diePrice = 5
    def shopSelect(self):
        startGold = self.playerGold
        pip = self.EventService.selectPip(self.dicePipRect[1])
        if pip:
            if self.playerGold > 0 and self.modGoldYes != None:
                #TODO other system
                if self.modGoldYes:
                    pip.addGOLDMod()
                    self.playerGold -= self.goldModPrice
                else:
                    pip.addATKMod()
                    self.playerGold -= self.atkModPrice
                self.modGoldYes = None
        button = self.EventService.selectButton(self.shopButtonRect)
        if button:
            button.action()
        if self.playerGold < startGold:
            self.SoundService.shopDict["ding"].play()
        # print(self.modGoldYes)

    def pickGOLDMod(self):
        self.modGoldYes = True

    def pickATKMod(self):
        self.modGoldYes = False

    def gameLoop(self):
        self.DrawService.resetFrame()
        self.DrawService.drawText(3, f"{self.playerGold} gold", 0,self.HEIGHT//2 - self.DrawService.marginY * 5, color=pg.Color(218,165,32), center=True)
        match self.currentState:
            case LevelState.LEVEL:
                self.levelLoop()
            case LevelState.SHOP:
                self.shopLoop()

    def buyDie(self):
        if self.playerGold - self.diePrice >= 0:
            self.playerGold -= self.diePrice
            self.newDice()
            
    def buyRoll(self):
        if self.playerGold - self.rollPrice >= 0:
            self.playerGold -= self.rollPrice
            self.LogicService.STARTING_ROLLS += 1

    def buyHand(self):
        if self.playerGold -   self.handPrice >= 0:
            self.playerGold -= self.handPrice
            self.LogicService.STARTING_HANDS += 1

    def goToShop(self):
        self.LogicService.unselectAll()
        self.harderLevel() #set up next level
        self.goldToAdd += self.interest
        buttonTexts =[f"{self.diePrice}g new die",
                      f"{self.handPrice}g another hand",
                      f"{self.rollPrice}g another roll",
                      f"{self.goldModPrice}g gold pip",
                      f"{self.atkModPrice}g atk pip",
                      f"next level"]
        self.shopButtons = self.DrawService.setButtons(buttonTexts, vertical = True)#,"1g +1 score pip","1g +1 gold pip"])
        self.shopButtons[0].setAction(self.buyDie)
        self.shopButtons[1].setAction(self.buyHand)
        self.shopButtons[2].setAction(self.buyRoll)
        self.shopButtons[3].setAction(self.pickGOLDMod)
        self.shopButtons[4].setAction(self.pickATKMod)
        self.shopButtons[5].setAction(self.goToLevel)

        self.interest = 0
        self.currentState = LevelState.SHOP
        
    def goToLevel(self):
        self.resetLevel()
        self.levelButtons = self.DrawService.setButtons(["roll", "score"])
        self.levelButtons[0].setAction(self.rollDice)
        self.levelButtons[1].setAction(self.scoreDice)

        self.otherButtons = self.DrawService.setButtons(["shop"])
        self.otherButtons[0].setAction(self.goToShop)

        self.currentState = LevelState.LEVEL

    def getCurrentState(self):
        return self.currentState.value

class LevelState(Enum):
    SHOP  = "stage_shop"
    LEVEL = "stage_level"