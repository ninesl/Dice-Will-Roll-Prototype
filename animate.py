import random
import pygame as pg

class AnimateService:
    def __init__(self, DrawService, clock, fps, SoundService):
        self.DrawService = DrawService
        self.clock = clock
        self.SoundService = SoundService
        self.fps = fps * 10 #fps miliseconds

        self.startingFrame = None
        self.scoreString = ""

        self.scoreStringIndex = 0
        self.scoreIndex = 0
        self.totalScore = -1

    def updateGold(self, playerGold, goldToAdd, WIDTH, HEIGHT):
        if goldToAdd > 0:
            goldToAdd -= 1
            playerGold += 1
            self.SoundService.shopDict["ding"].play()

        return goldToAdd, playerGold
    
    def selectedScoreString(self, scoringHandDice):
        pipChars = "⚀⚁⚂⚃⚄⚅"
        handVals = []
        for die in scoringHandDice:
            handVals.append(f"{pipChars[die.curSide.getNum() - 1]}")
        return handVals
    
    def animateScoringHand(self, LogicService):
        self.scoreString = list(self.scoreString)
        if LogicService.isScoring:
            scoreMatches = self.totalScore == LogicService.selectedScoreTotal()
            
            if not self.startingFrame:
                self.startingFrame = pg.time.get_ticks()
                self.SoundService.diceDict["deselect"].play()

                if not scoreMatches:
                    curDieCalcNum = LogicService.scoringHandDice[self.scoreIndex].calculate()
                    curDieCalcNum = int(curDieCalcNum)
                    self.scoreString[self.scoreStringIndex] = f"{curDieCalcNum} "
                    self.DrawService.deleteRocks(curDieCalcNum)

                    self.scoreStringIndex += len(str(curDieCalcNum)) + 1
                    self.scoreIndex += 1

            elif self.startingFrame + self.fps // 1.5 < pg.time.get_ticks():
                self.startingFrame = None

                if scoreMatches:
                    numRocksToDelete = self.totalScore - LogicService.selectedScoreTotal(handMult = False)
                    self.DrawService.deleteRocks(numRocksToDelete)
                    self.SoundService.hitSound(self.totalScore)
                    self.totalScore = 0
                    LogicService.stopScoring(self.SoundService)
                elif self.scoreStringIndex == len(self.scoreString):
                    self.scoreIndex = 0
                    self.scoreStringIndex = 0
                    self.totalScore = LogicService.selectedScoreTotal()
                    self.scoreString = [str(self.totalScore)]
        else:
            self.scoreString = self.selectedScoreString(LogicService.scoringHandDice)

        self.scoreString = "".join(self.scoreString)
        self.DrawService.drawHandText(LogicService, self.scoreString.strip())
        

    def shakeDice(self, playerDice, selected=False):
        # Calculate the initial x position to center the dice
        totalWidth = self.DrawService.getTotalDiceWidth(playerDice)
        oldDiceX = (self.DrawService.WIDTH - totalWidth) // 2

        shake_duration = 10  # Total shakes
        max_shake_range = 15  # Max pixels to shake

        y = self.DrawService.levelDiceY

        for _ in range(shake_duration):
            x = oldDiceX
            for die in playerDice:
                if not die.isSelected and not selected or die.isSelected and    selected:
                    pixelShakeX = random.randint(-max_shake_range,  max_shake_range)
                    pixelShakeY = random.randint(-max_shake_range,  max_shake_range)

                    # Temporarily update dice positions
                    x += pixelShakeX
                    y += pixelShakeY

                    # Redraw the die at new position
                    self.DrawService.drawDie(die, x, y)

                    # Reset dice positions
                    x -= pixelShakeX
                    y -= pixelShakeY

                x += self.DrawService.dieSide + self.DrawService.dieSpacing

            pg.display.update()