import random
import pygame as pg

class AnimateService:
    def __init__(self, DrawService, clock, fps, SoundService):
        self.DrawService = DrawService
        self.clock = clock
        self.SoundService = SoundService
        self.fps = fps * 10 #fps miliseconds

        self.startingFrame = None

        self.scoreStringIndex = 0
    
    def selectedScoreString(self, scoringHandDice):
        pipChars = "⚀⚁⚂⚃⚄⚅"
        handVals = ""
        for die in scoringHandDice:
            handVals += f"{pipChars[die.curSide.getNum() - 1]}"
        return handVals.strip()
    
    def animateScoringHand(self, LogicService):
        if LogicService.isScoring:
            self.scoreString = list(self.scoreString)
            if not self.startingFrame:
                self.startingFrame = pg.time.get_ticks()

                self.SoundService.diceDict["tap"].play()
                self.startingFrame = pg.time.get_ticks()
            
                curDieNum = LogicService.scoringHandDice[self.scoreStringIndex].curSide.getNum()
                self.scoreString[self.scoreStringIndex] = str(curDieNum)

                self.DrawService.deleteRocks(LogicService.scoringHandDice[self.scoreStringIndex].calculate())

                self.scoreStringIndex += 1
                
            elif self.startingFrame + self.fps < pg.time.get_ticks():
                self.startingFrame = None
                if self.scoreStringIndex == len(self.scoreString):
                    self.scoreStringIndex = 0
                    self.startingFrame = None
                    LogicService.stopScoring()

            self.scoreString = "".join(self.scoreString)
        else:
            self.scoreString = self.selectedScoreString(LogicService.scoringHandDice)

        self.DrawService.drawHandInfo(LogicService, self.scoreString)
        

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