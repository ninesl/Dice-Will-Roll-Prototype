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
    STARTING_ROCKS = 0
    GOING = True

    playerGold = 100
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
        if self.rangeDieMin <= 0:
            self.rangeDieMin = 0
        if self.rangeDieMax <= 15:
            self.rangeDieMax = 15

        randRGBVals = [ rand.randint(self.rangeDieMin, self.rangeDieMax), 
                        rand.randint(0, self.rangeDieMax), 
                        rand.randint(int(self.rangeDieMin/2), self.rangeDieMax)]

        dieColor = pg.Color(rand.choice(randRGBVals),
                            rand.choice(randRGBVals),
                            rand.choice(randRGBVals))
        self.playerDice.append(dice.Die(6, dieColor))
        self.rangeDieMin -= rand.randint(15,25)
        self.rangeDieMax -= rand.randint(5,15)

    numStartDice = 1
    def setDice(self):
        self.playerDice = []
        self.rangeDieMin, self.rangeDieMax = 250,255
        for _ in range(self.numStartDice):
            self.newDice()
        for die in self.playerDice:
            die.rollDie()

    def levelSelect(self):
        d = self.EventService.holdDie(self.dicePipSideRect[0])
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
        self.LogicService.updateGoldPips()
        self.LogicService.score()

    def resetLevel(self):
        self.goldPipsThisLevel = 0
        self.LogicService.startLevel(self.STARTING_ROCKS)
    
    def harderLevel(self):
        # self.LogicService.unselectAll()
        # self.LogicService.rollDice()
        self.BACKGROUND_COLOR_RANGE -= rand.randint(5,15)
        if self.BACKGROUND_COLOR_RANGE <= self.DrawService.BACKGROUND_COLOR_RANGE_DIFF:
            self.BACKGROUND_COLOR_RANGE = self.DrawService.BACKGROUND_COLOR_RANGE_DIFF
        self.STARTING_ROCKS = int(self.STARTING_ROCKS * 1.25)

    goldPipsThisLevel = 0
    def levelLoop(self):
        #returns list of (die, rect) for EventService
        self.dicePipSideRect = self.DrawService.drawDice(self.playerDice, self.LogicService.scoringHandDice)

        self.EventService.dieHovered(self.dicePipSideRect[0])
        self.LogicService.findHand()
        self.DrawService.drawPreviousHands()

        self.scoreButtonRect = self.DrawService.drawButtons(self.levelButtons)

        if self.LogicService.isNextLevel():
            self.interest, self.stageClearBonus, self.goldPipsThisLevel = self.LogicService.calculateGold(self.playerGold)
            self.goldToAdd = self.interest + self.goldPipsThisLevel + self.stageClearBonus + self.LogicService.handsLeft
            
            self.DrawService.drawText(2, "Level Completed!", 0,-self.DrawService.heightGrid * 1.5, center=True)

            self.DrawService.drawText(1, f"stage clear:          ${self.stageClearBonus}", 0,-self.DrawService.heightGrid // 2, center=True)
            self.DrawService.drawText(1, f"gold pips:            ${self.goldPipsThisLevel}",   0,0, center=True)
            self.DrawService.drawText(1, f"$1 every $5 owned:    ${self.interest}",   0,self.DrawService.heightGrid // 2, center=True)
            self.DrawService.drawText(1, f"hands left:           ${self.LogicService.handsLeft}",    0,self.DrawService.heightGrid, center=True)
            self.DrawService.drawText(1, f"------------------------",      0,self.DrawService.heightGrid * 1.25, center=True)
            self.DrawService.drawText(1, f"total gained:         ${self.goldToAdd}",          0,self.DrawService.heightGrid * 1.5, center=True)
            
            self.levelButtons = self.otherButtons
            return
        
        self.DrawService.drawLevelText(self.LogicService)
        self.AnimateService.animateScoringHand(self.LogicService)

    def shopLoop(self):
        self.gameMsg = f"{self.goldPipsThisLevel} gold pips this level"
        self.goldToAdd, self.playerGold = self.AnimateService.updateGold(self.playerGold, self.goldToAdd, self.WIDTH, self.HEIGHT)
        self.dicePipSideRect = self.DrawService.drawAllDiceFaces(self.playerDice) #pips
        self.shopButtonRect = self.DrawService.drawButtons(self.shopButtons)

    def shopSelect(self):
        startGold = self.playerGold
        pip = self.EventService.selectPip(self.dicePipSideRect[1])
        side = self.EventService.selectSide(self.dicePipSideRect[2])
        objAddingMod = None
        if side:
            objAddingMod = side
        if pip: #pip rect above side
            objAddingMod = pip
        if objAddingMod and self.playerGold > 0:
            if self.modGoldYes != None:
                #TODO other system
                if self.modGoldYes:
                    print(f"{type(objAddingMod)} gold")
                    objAddingMod.addGOLDMod()
                    self.playerGold -= self.goldModPrice
                else:
                    print(f"{type(objAddingMod)} atk")
                    objAddingMod.addATKMod()
                    self.playerGold -= self.atkModPrice
            elif self.removingSide != None:
                print("got here")
                if objAddingMod is side:
                    objAddingMod.parentDie.sides.remove(side)#deletes side forever
                    self.playerGold -= self.removeSidePrice
                    self.removeSidePrice *= 2
            self.modGoldYes = None
            self.removingSide = None
            objAddingMod = None
        button = self.EventService.selectButton(self.shopButtonRect)
        if button:
            button.action(self)
        if self.playerGold < startGold:
            self.SoundService.shopDict["ding"].play()
        self.updateShopText()

    def pickGOLDMod(self):
        if self.playerGold - self.goldModPrice >= 0:
            self.modGoldYes = True

    def pickATKMod(self):
        if self.playerGold - self.atkModPrice >= 0:
            self.modGoldYes = False

    def gameLoop(self):
        self.gameMsg = f"{self.goldPipsThisLevel} gold pips this level"
        self.DrawService.resetFrame()
        self.DrawService.drawText(2, f"{self.gameMsg}", 0,self.HEIGHT//2 - self.DrawService.marginY * 10, center=True)
        self.DrawService.drawText(2, f"${self.playerGold}", 0,self.HEIGHT//2 - self.DrawService.marginY * 20, color=pg.Color(218,165,32), center=True)
        match self.currentState:
            case LevelState.LEVEL:
                self.levelLoop()
            case LevelState.SHOP:
                self.shopLoop()

    def buyDie(self):
        if self.playerGold - self.diePrice >= 0:
            self.playerGold -= self.diePrice
            self.newDice()
            self.diePrice *= 2
            
    def buyRoll(self):
        if self.playerGold - self.rollPrice >= 0:
            self.playerGold -= self.rollPrice
            self.LogicService.STARTING_ROLLS += 1
            self.rollPrice *= 2

    def buyHand(self):
        if self.playerGold - self.handPrice >= 0:
            self.playerGold -= self.handPrice
            self.LogicService.STARTING_HANDS += 1
            self.handPrice *= 2

    def removeSide(self):
        if self.playerGold - self.removeSidePrice >= 0:
            self.removingSide = True

    def goToShop(self):
        self.LogicService.unselectAll()
        self.harderLevel() #set up next level
        self.modsAvailable = self.startingModsAvailable
        self.setShopButtons()

        self.interest = 0
        self.goldPipsThisLevel = 0
        self.currentState = LevelState.SHOP
        
    def goToLevel(self):
        self.resetLevel()
        self.levelButtons = self.DrawService.setButtons(["roll", "score"])
        self.levelButtons[0].setAction(self.rollDice)
        self.levelButtons[1].setAction(self.scoreDice)

        self.otherButtons = self.DrawService.setButtons(["shop"])
        self.otherButtons[0].setAction(self.goToShop)

        self.currentState = LevelState.LEVEL

    startingModsAvailable = 3
    modsAvailable = 0
    modGoldYes = None
    removingSide = None
    goldModPrice = 2
    atkModPrice = 1
    handPrice = 10
    rollPrice = 5
    diePrice = 5
    removeSidePrice = 30
    
    shopButtonActions = [
        buyDie,
        buyHand,
        buyRoll,
        pickGOLDMod,
        pickATKMod,
        removeSide,
        goToLevel
    ]
    def setShopText(self):
        self.buttonTexts =[
            f"${self.diePrice} buy □",
            f"${self.handPrice} buy hand",
            f"${self.rollPrice} buy roll",
            f"${self.goldModPrice} gold mod",
            f"${self.atkModPrice} atk mod",
            f"${self.removeSidePrice} remove side",
            f"next level"]

    def setShopButtons(self):
        self.setShopText()
        self.shopButtons = self.DrawService.setButtons(self.buttonTexts, vertical = True)
        for button, action in zip(self.shopButtons, self.shopButtonActions):
            button.setAction(action)

    def updateShopText(self):
        self.setShopText()
        for button, buttonText in zip(self.shopButtons, self.buttonTexts):
            print("updating", buttonText)
            button.updateText(buttonText)

    def getCurrentState(self):
        return self.currentState.value
class LevelState(Enum):
    SHOP  = "stage_shop"
    LEVEL = "stage_level"