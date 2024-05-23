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
    BACKGROUND_COLOR_RANGE = 200
    STARTING_ROCKS = 7
    MAX_DICE = 7
    GOING = True

    playerGold = 4
    goldToAdd = 0
    interest = 0

    playerDieColors = [
        pg.Color(125,50,183),
        pg.Color(103,152,171),
        pg.Color(103,152,81),
        pg.Color(255,0,124),
        pg.Color(139,0,44),
        pg.Color(10,18,97)
    ]

    def __init__(self, monitor, clock, fps):
        self.monitor = monitor
        self.clock = clock
        self.fps = fps

        self.currentState = LevelState.LEVEL

        self.WIDTH  = int(monitor.current_w * 8/10)
        self.HEIGHT = int(monitor.current_h * 8/10)
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
        # randRGBVals = [ rand.randint(self.rangeDieMin, self.rangeDieMax), 
        #                 rand.randint(0, self.rangeDieMax), 
        #                 rand.randint(int(self.rangeDieMin/2), self.rangeDieMax)]

        # dieColor = pg.Color(rand.choice(randRGBVals),
        #                     rand.choice(randRGBVals),
        #                     rand.choice(randRGBVals))
        # self.rangeDieMin -= rand.randint(15,25)
        # self.rangeDieMax -= rand.randint(5,15)

        dieColor = rand.choice(self.playerDieColors)
        rAdd = rand.randint(-15,15)
        gAdd = rand.randint(-15,15)
        bAdd = rand.randint(-15,15)
        
        if dieColor.r + rAdd >= 255 or dieColor.r + rAdd <= 0:
            rAdd = 0
        if dieColor.g + gAdd >= 255 or dieColor.g + gAdd <= 0:
            gAdd = 0
        if dieColor.b + bAdd >= 255 or dieColor.b + bAdd <= 0:
            bAdd = 0

        dieColor.r += rAdd
        dieColor.g += gAdd
        dieColor.b += bAdd

        self.playerDice.append(dice.Die(6, dieColor))

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
        # self.DrawService.BackgroundService.changeDirection() horrible performance
        self.AnimateService.shakeDice(self.playerDice)
        self.SoundService.diceRollSound(self.LogicService.rollsLeft)
        self.LogicService.rollDice()

    def scoreDice(self):
        self.LogicService.updateGoldPips()
        self.LogicService.score()

    def resetLevel(self):
        self.AnimateService.resetAnimationTrackers()
        self.goldPipsThisLevel = 0
        self.LogicService.startLevel(self.STARTING_ROCKS)
    
    def harderLevel(self):
        self.BACKGROUND_COLOR_RANGE -= rand.randint(10,20)
        if self.BACKGROUND_COLOR_RANGE <= self.DrawService.BACKGROUND_COLOR_RANGE_DIFF:
            self.BACKGROUND_COLOR_RANGE = self.DrawService.BACKGROUND_COLOR_RANGE_DIFF
        self.STARTING_ROCKS = int(self.STARTING_ROCKS * 1.5)
        self.LogicService.stageClearBonus += 1
        self.DrawService.setBackground(self.BACKGROUND_COLOR_RANGE)

    goldPipsThisLevel = 0
    def levelLoop(self):
        self.goldPipsThisLevel = self.LogicService.goldPipsThisLevel
        self.gameMsg = f"{self.goldPipsThisLevel} gold pips this level"
        #returns list of (die, rect) for EventService
        self.dicePipSideRect = self.DrawService.drawDice(self.playerDice, self.LogicService.scoringHandDice)

        self.EventService.dieHovered(self.dicePipSideRect[0])
        self.LogicService.findHand()
        self.DrawService.drawPreviousHands()
        self.scoreButtonRect = self.DrawService.drawButtons(self.levelButtons)

        if self.dieInfo:
            self.DrawService.drawDieInfoFaces(self.dieInfo)

        if self.LogicService.isNextLevel():
            self.levelButtons = []
            self.interest, self.stageClearBonus, self.goldPipsThisLevel = self.LogicService.calculateGold(self.playerGold)
            self.goldToAdd = self.interest + self.goldPipsThisLevel + self.stageClearBonus + self.LogicService.handsLeft
            if self.AnimateService.animateLevelCompleteHand(self):
                # self.levelButtons = [self.otherButtons[0]]
                self.levelButtons = self.otherButtons
            return
        
        if self.LogicService.handsLeft == 0 and self.LogicService.rockHealth > 0 and not self.LogicService.isScoring:
            self.levelButtons = []
            if self.AnimateService.gameOverAnimation():
                self.levelButtons = self.gameOverButtons
            return
        
        self.DrawService.drawLevelText(self.LogicService)
        self.AnimateService.animateScoringHand(self.LogicService)

    startingModsAvailable = 3
    modsAvailable = 0
    def shopLoop(self):
        self.gameMsg = f"{self.modsAvailable}/{self.startingModsAvailable} pip/side mods left."
        self.goldToAdd, self.playerGold = self.AnimateService.updateGold(self.playerGold, self.goldToAdd)
        self.dicePipSideRect = self.DrawService.drawAllDiceFaces(self.playerDice) #pips
        self.shopButtonRect = self.DrawService.drawButtons(self.shopButtons)

    activeButton = None

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
            if (self.activeButtonFlags['modAtkYes'] or self.activeButtonFlags['modGoldYes']) and self.modsAvailable > 0:
                #TODO other system
                if self.activeButtonFlags['modGoldYes']:
                    print(f"{type(objAddingMod)} gold")
                    objAddingMod.addGOLDMod()
                    self.playerGold -= self.goldModPrice
                    self.modsAvailable -= 1
                    self.clearActiveButton()
                if self.activeButtonFlags['modAtkYes']:
                    print(f"{type(objAddingMod)} atk")
                    objAddingMod.addATKMod()
                    self.playerGold -= self.atkModPrice
                    self.modsAvailable -= 1
                    self.clearActiveButton()
            elif self.activeButtonFlags['buyingPip']:
                if objAddingMod:
                    if objAddingMod is pip: #give to parent side
                        objAddingMod = side
                    if objAddingMod.addNewPip():
                        self.playerGold -= self.addPipPrice
                        self.addPipPrice = self.modifyPrice(self.addPipPrice)
                    else:
                        self.clearActiveButton()
            elif self.activeButtonFlags['removingSide']:
                if objAddingMod:
                    # if objAddingMod is pip:
                    side.parentDie.sides.remove(side)#deletes side forever
                    #if you delete them all you can't win. Leaving it in
                    if len(side.parentDie.sides) <= 0:
                        self.playerDice.remove(side.parentDie)
                    self.playerGold -= self.removeSidePrice
                    self.removeSidePrice = self.modifyPrice(self.removeSidePrice)
            self.clearActiveButtonFlags()
            objAddingMod = None
        button = self.EventService.selectButton(self.shopButtonRect)
        if button:
            if self.activeButton:
                self.clearActiveButton()
                self.clearActiveButtonFlags()
            elif self.activeButton == None:
                button.click()
                self.activeButton = button
                button.action(self)
        if self.playerGold < startGold:
            self.SoundService.shopDict["ding"].play()
        self.updateShopText()

    def clearActiveButtonFlags(self):
        self.activeButtonFlags['modGoldYes'] = None
        self.activeButtonFlags['modAtkYes'] = None
        self.activeButtonFlags['removingSide'] = None
        self.activeButtonFlags['buyingPip'] = None

    def pickGOLDMod(self):
        if self.playerGold - self.goldModPrice >= 0:
            self.activeButtonFlags['modGoldYes'] = True

    def pickATKMod(self):
        if self.playerGold - self.atkModPrice >= 0:
            self.activeButtonFlags['modAtkYes'] = True

    gameMsg = ""
    def gameLoop(self):
        self.DrawService.resetFrame()
        match self.currentState:
            case LevelState.LEVEL:
                self.levelLoop()
            case LevelState.SHOP:
                self.shopLoop()
        self.DrawService.drawText(2, f"${self.playerGold}",self.DrawService.marginX,self.HEIGHT / 10 * 8.5, color=pg.Color(218,165,32))
        self.DrawService.drawText(2, f"{self.gameMsg}",self.DrawService.marginX,self.HEIGHT / 10 * 9.2)

    shopModifier = 2.5
    # shopModifier = 0
    def modifyPrice(self, priceToChange):
        shopModifierDiff = rand.random() / 4.0 + .3 #.55 biggest diff
        priceToChange *= rand.choice([self.shopModifier + shopModifierDiff,
                                      self.shopModifier - shopModifierDiff])
        self.clearActiveButton() #active button happens when price changes
        return int(priceToChange)#truncate decimal
    
    def clearActiveButton(self):
        self.activeButton.click()
        self.activeButton = None
    
    def buyDie(self):
        if self.playerGold - self.diePrice >= 0 and len(self.playerDice) < self.MAX_DICE:
            self.playerGold -= self.diePrice
            self.newDice()
            self.diePrice = self.modifyPrice(self.diePrice)
            
    def buyRoll(self):
        if self.playerGold - self.rollPrice >= 0:
            self.playerGold -= self.rollPrice
            self.LogicService.STARTING_ROLLS += 1
            self.rollPrice = self.modifyPrice(self.rollPrice)

    def buyHand(self):
        if self.playerGold - self.handPrice >= 0:
            self.playerGold -= self.handPrice
            self.LogicService.STARTING_HANDS += 1
            self.handPrice = self.modifyPrice(self.handPrice)

    def buyRemoveSide(self):
        if self.playerGold - self.removeSidePrice >= 0:
            self.activeButtonFlags['removingSide'] = True

    def goToShop(self):
        self.LogicService.unselectAll()
        self.modsAvailable = self.startingModsAvailable
        self.setShopButtons()

        self.interest = 0
        self.goldPipsThisLevel = 0
        self.currentState = LevelState.SHOP
        self.harderLevel() #set up next level
        
    def goToLevel(self):
        self.resetLevel()
        self.levelButtons = self.DrawService.setButtons(["roll not held", "score and roll held"])
        self.levelButtons[0].setAction(self.rollDice)
        self.levelButtons[1].setAction(self.scoreDice)

        self.otherButtons = self.DrawService.setButtons(["go to shop"])
        self.gameOverButtons = self.DrawService.setButtons(["reset", "quit"])
        self.otherButtons[0].setAction(self.goToShop)
        self.gameOverButtons[0].setAction(self.goToLevel)
        self.gameOverButtons[1].setAction(self.quitGame)

        self.currentState = LevelState.LEVEL

    dieInfo = None
    rightClicked = False
    def drawDieInfoFaces(self):
        if not self.rightClicked:
            d = self.EventService.dieHovered(self.dicePipSideRect[0])
            if d:
                self.dieInfo = d
            if not d:
                self.dieInfo = None
            self.rightClicked = True
        else:
            self.rightClicked = False
            self.dieInfo = None

    def buyModAvailable(self):
        if self.playerGold - self.addModPrice >= 0:
            self.playerGold -= self.addModPrice
            self.startingModsAvailable += 1
            self.modsAvailable += 1
            self.addModPrice = self.modifyPrice(self.addModPrice)

    def buyAddPip(self):
        if self.playerGold - self.addPipPrice >= 0:
            self.activeButtonFlags['buyingPip'] = True

    activeButtonFlags = {
        'modGoldYes' : None,
        'modAtkYes' : None,
        'removingSide' : None,
        'buyingPip' : None
    }
    addPipPrice = 1
    addModPrice = 5
    goldModPrice = 2
    atkModPrice = 1
    handPrice = 10
    rollPrice = 15
    diePrice = 5
    removeSidePrice = 30
    
    shopButtonActions = [
        buyDie,
        buyHand,
        buyRoll,
        buyModAvailable,
        pickGOLDMod,
        pickATKMod,
        buyRemoveSide,
        buyAddPip,
        goToLevel
    ]
    def setShopText(self):
        self.buttonTexts =[
            f"${self.diePrice} buy □",
            f"${self.handPrice} buy hand",
            f"${self.rollPrice} buy roll",
            f"${self.addModPrice} +1 mod per shop",
            f"${self.goldModPrice} gold mod",
            f"${self.atkModPrice} atk mod",
            f"${self.removeSidePrice} remove side",
            f"${self.addPipPrice} add pip",
            f"next level"]

    def setShopButtons(self):
        self.setShopText()
        self.shopButtons = self.DrawService.setButtons(self.buttonTexts, vertical = True)
        for button, action in zip(self.shopButtons, self.shopButtonActions):
            button.setAction(action)

    def updateShopText(self):
        self.setShopText()
        for button, buttonText in zip(self.shopButtons, self.buttonTexts):
            # print("updating", buttonText)
            button.updateText(buttonText)

    def getCurrentState(self):
        return self.currentState.value
class LevelState(Enum):
    SHOP  = "stage_shop"
    LEVEL = "stage_level"