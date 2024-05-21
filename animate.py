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
        self.DrawService.drawHandInfo(LogicService, self.scoreString.strip())
        

    def shakeDice(self, playerDice, selected = False):
        oldDiceX = self.DrawService.diceX
        oldDiceY = self.DrawService.diceY

        shake_duration = 10  # Total shakes
        max_shake_range = 15  # Max pixels to shake

        # Redraw the dice at new position
        # self.DrawService.drawDice(dieToKeep)

        # self.DrawService.diceY += int(self.DrawService.dieSide * 1.5)
        y = self.DrawService.diceY
        for _ in range(shake_duration):
            x = self.DrawService.diceX
            for die in playerDice:
                if not die.isSelected and not selected or die.isSelected and selected:
                    # die.rollDie()
                    pixelShakeX = random.randint(-max_shake_range, max_shake_range)
                    pixelShakeY = random.randint(-max_shake_range, max_shake_range)
                    # Temporarily update dice positions
                    x += pixelShakeX
                    y += pixelShakeY
                    # Redraw the die at new position
                    self.DrawService.drawDie(die, x, y)
                    # Reset dice positions
                    x -= pixelShakeX
                    y -= pixelShakeY

                x += self.DrawService.dieSpacing
            
            pg.display.update()
                    
        # Ensure dice positions are reset after shaking
        self.DrawService.diceX = oldDiceX
        self.DrawService.diceY = oldDiceY