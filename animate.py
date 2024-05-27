import random
import pygame as pg

class AnimateService:
    def __init__(self, DrawService, clock, fps, SoundService):
        self.DrawService = DrawService
        self.clock = clock
        self.SoundService = SoundService
        self.fps = fps * 10 #fps miliseconds
        self.resetAnimationTrackers()

    def resetAnimationTrackers(self):
        self.startingFrame = None
        self.scoreString = ""

        self.scoreStringIndex = 0
        self.scoreIndex = 0
        self.totalScore = -1

        self.levelCompleteIndex = 0
        self.gameOverIndex = 0

        self.showHoveredDieIndex = 0

    def showHoveredDie(self, die):
        oldDieSide = self.DrawService.dieSide
        self.DrawService.dieSide = self.DrawService.HEIGHT / 14
        print(oldDieSide)
        # xSpacing = 0
        ySpacing = 0
        currentSide = die.curSide
        i = 0
        for sideIndex in range(die.getNumSides()):
            die.curSide = die.sides[sideIndex]
            if self.showHoveredDieIndex >= 1:
                self.DrawService.drawDie(die, self.DrawService.WIDTH - self.DrawService.dieSide - self.DrawService.marginX, self.DrawService.marginY + ySpacing)
                i += 1
            if self.showHoveredDieIndex >= 2:
                self.DrawService.drawDie(die, self.DrawService.WIDTH - self.DrawService.dieSide - self.DrawService.marginX, self.DrawService.marginY + ySpacing)
                i += 1
            if self.showHoveredDieIndex >= 3:
                self.DrawService.drawDie(die, self.DrawService.WIDTH - self.DrawService.dieSide - self.DrawService.marginX, self.DrawService.marginY + ySpacing)
                i += 1
            if self.showHoveredDieIndex >= 4:
                self.DrawService.drawDie(die, self.DrawService.WIDTH - self.DrawService.dieSide - self.DrawService.marginX, self.DrawService.marginY + ySpacing)
                i += 1
            if self.showHoveredDieIndex >= 5:
                self.DrawService.drawDie(die, self.DrawService.WIDTH - self.DrawService.dieSide - self.DrawService.marginX, self.DrawService.marginY + ySpacing)
                i += 1
            # xSpacing += self.dieSide + self.marginX
            ySpacing += self.DrawService.dieSide + self.DrawService.marginY
        die.curSide = currentSide
        self.dieSide = oldDieSide


        self.DrawService.drawDieInfoFaces(die)
        
        if not self.startingFrame:#updating info
            # print(self.gameOverIndex)
            self.startingFrame = pg.time.get_ticks()
            self.SoundService.diceDict["preview"].play()
            #play sound
        elif self.startingFrame + self.fps // 6 < pg.time.get_ticks():#animation change
            self.showHoveredDieIndex += 1
            self.startingFrame = None


    def updateGold(self, playerGold, goldToAdd):
        incr = 1
        tempGold = goldToAdd
        while tempGold > 30:#counts by 1 at 30
            tempGold /= 10
            incr *= 10 #ups every tens place
        

        if goldToAdd > 0:
            goldToAdd -=  incr
            playerGold += incr
            self.SoundService.shopDict["ding"].play()
            # print(goldToAdd, playerGold)
        return goldToAdd, playerGold
    
    pipChars = ["□","⚀","⚁","⚂","⚃","⚄","⚅","ⅶ","ⅷ",
                "ⅸ","ⅹ","ⅺ","ⅻ","*"]
    def selectedScoreString(self, scoringHandDice):
        handVals = []
        for die in scoringHandDice:
            handVals.append(f"{self.pipChars[die.curSide.getNum()]}")
        return handVals
    
    def animateLevelCompleteHand(self, gc):
            self.DrawService.drawText("Level Completed!",0,-self.DrawService.heightGrid * 1.5, center=True, fontIndex = 2)
            if self.levelCompleteIndex > 0:
                    self.DrawService.drawText(f"stage clear:",-self.DrawService.widthGrid * 3,-self.DrawService.heightGrid // 2, center=True, fontIndex=1)
            if self.levelCompleteIndex > 1:
                    self.DrawService.drawText(f"${gc.stageClearBonus}",0,-self.DrawService.heightGrid // 2, center=True, fontIndex=1)
            if self.levelCompleteIndex > 2:
                self.DrawService.drawText(f"gold pips:", -self.DrawService.widthGrid * 3,0, center=True, fontIndex=1)
            if self.levelCompleteIndex > 3:
                self.DrawService.drawText(f"${gc.goldPipsThisLevel}",0,0, center=True, fontIndex=1)
            if self.levelCompleteIndex > 4:
                interestMsg = f"$1 every ${gc.LogicService.interestThreshold} owned ({gc.LogicService.interestMaxPerLevel} max):"
                self.DrawService.drawText(interestMsg, -self.DrawService.widthGrid * 3,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
            if self.levelCompleteIndex > 5:
                self.DrawService.drawText(f"${gc.interest}",0,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
            if self.levelCompleteIndex > 6:
                self.DrawService.drawText(f"hands left:",-self.DrawService.widthGrid * 3,self.DrawService.heightGrid, center=True, fontIndex=1)
            if self.levelCompleteIndex > 7:
                self.DrawService.drawText(f"${gc.LogicService.handsLeft}",0,self.DrawService.heightGrid, center=True, fontIndex=1)
            if self.levelCompleteIndex > 8:
                self.DrawService.drawText(f"------------------------",0,self.DrawService.heightGrid * 1.25, center=True, fontIndex=1)
                self.DrawService.drawText(f"total gained:",-self.DrawService.widthGrid * 3,self.DrawService.heightGrid * 1.5, center=True, fontIndex=1)
            if self.levelCompleteIndex > 9:
                self.DrawService.drawText(f"${gc.goldToAdd}",0,self.DrawService.heightGrid * 1.5, center=True, fontIndex=1)
            if self.levelCompleteIndex > 10:
                return True
            

            if not self.startingFrame:#updating info
                self.startingFrame = pg.time.get_ticks()
                self.SoundService.hitDict["light"].play()
                #play sound
            elif self.startingFrame + self.fps // 2 < pg.time.get_ticks():#animation change
                self.levelCompleteIndex += 1
                self.startingFrame = None
                
    # def animateLevelCompleteHand(self, gc):
    #         self.DrawService.drawText("Level Completed!",0,-self.DrawService.heightGrid * 1.5, center=True, fontIndex = 2)
    #         if self.levelCompleteIndex > 0:
    #                 self.DrawService.drawText(f"stage clear:",-self.DrawService.widthGrid * 3,-self.DrawService.heightGrid // 2, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 1:
    #                 self.DrawService.drawText(f"${gc.stageClearBonus}",0,-self.DrawService.heightGrid // 2, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 2:
    #             self.DrawService.drawText(f"gold pips:", -self.DrawService.widthGrid * 3,0, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 3:
    #             self.DrawService.drawText(f"${gc.goldPipsThisLevel}",0,0, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 4:
    #             interestMsg = f"$1 every ${gc.LogicService.interestThreshold} owned ({gc.LogicService.interestMaxPerLevel} max):"
    #             self.DrawService.drawText(interestMsg, -self.DrawService.widthGrid * 3,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 5:
    #             self.DrawService.drawText(f"${gc.interest}",0,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 6:
    #             self.DrawService.drawText(f"hands left:",-self.DrawService.widthGrid * 3,self.DrawService.heightGrid, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 7:
    #             self.DrawService.drawText(f"${gc.LogicService.handsLeft}",0,self.DrawService.heightGrid, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 8:
    #             self.DrawService.drawText(f"------------------------",0,self.DrawService.heightGrid * 1.25, center=True, fontIndex=1)
    #             self.DrawService.drawText(f"total gained:",-self.DrawService.widthGrid * 3,self.DrawService.heightGrid * 1.5, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 9:
    #             self.DrawService.drawText(f"${gc.goldToAdd}",0,self.DrawService.heightGrid * 1.5, center=True, fontIndex=1)
    #         if self.levelCompleteIndex > 10:
    #             return True
            

    #         if not self.startingFrame:#updating info
    #             self.startingFrame = pg.time.get_ticks()
    #             self.SoundService.hitDict["light"].play()
    #             #play sound
    #         elif self.startingFrame + self.fps // 2 < pg.time.get_ticks():#animation change
    #             self.levelCompleteIndex += 1
    #             self.startingFrame = None

    def gameOverAnimation(self, numDice = None):
            if self.gameOverIndex >= 0:
                self.DrawService.drawText(f"GAME",   0,-self.DrawService.    heightGrid, center=True, fontIndex=3)
            if self.gameOverIndex >= 1:
                self.DrawService.drawText(f"OVER",   0,-self.DrawService.    heightGrid // 2, center=True, fontIndex=3)

            if numDice == 0:
                if self.gameOverIndex == 2:
                    self.DrawService.drawText(f"Bro.",   0,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
                if self.gameOverIndex == 3:
                    self.DrawService.drawText(f"Bro..",   0,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
                if self.gameOverIndex > 3:
                    self.DrawService.drawText(f"Bro...",   0,self.DrawService.heightGrid // 2, center=True, fontIndex=1)
                if self.gameOverIndex > 4:
                    self.DrawService.drawText(f"no dice??",   0,self.DrawService.heightGrid, center=True, fontIndex=1)
                    print("achievement")
                if self.gameOverIndex > 5:
                    return True
            else:
                # if self.gameOverIndex >= 2:
                #     self.DrawService.drawText(f"keep rolling to score your best hand, no multiplier",   0,0, center=True, fontIndex=1)
                if self.gameOverIndex >= 2:
                    return True

            if not self.startingFrame:#updating info
                # print(self.gameOverIndex)
                self.startingFrame = pg.time.get_ticks()
                self.SoundService.hitDict["none"].play()
                #play sound
            elif self.startingFrame + self.fps < pg.time.get_ticks():#animation change
                self.gameOverIndex += 1
                self.startingFrame = None
            
    def animateScoringHand(self, LogicService):
        self.scoreString = list(self.scoreString)
        if LogicService.isScoring:
            scoreMatches = self.totalScore == LogicService.selectedScoreTotal()
            
            if not self.startingFrame:#updating info
                self.startingFrame = pg.time.get_ticks()

                if not scoreMatches:
                    self.SoundService.diceDict["deselect"].play()
                    curDieCalcNum = LogicService.scoringHandDice[self.scoreIndex].calculate()
                    curDieCalcNum = int(curDieCalcNum)
                    self.scoreString[self.scoreStringIndex] = f"{curDieCalcNum} "
                    self.DrawService.deleteRocks(curDieCalcNum)

                    self.scoreStringIndex += len(str(curDieCalcNum)) + 1
                    self.scoreIndex += 1

            elif self.startingFrame + self.fps // 1.5 < pg.time.get_ticks():#animation change
                self.startingFrame = None

                if scoreMatches:
                    numRocksToDelete = self.totalScore - LogicService.selectedScoreTotal(handMult = False)
                    self.DrawService.deleteRocks(numRocksToDelete)
                    self.totalScore = 0
                    #Only stop scoring after animation is completed
                    LogicService.stopScoring(self.SoundService)
                    self.shakeDice(LogicService.playerDice, selected=True)
                elif self.scoreStringIndex == len(self.scoreString):
                    self.SoundService.hitSound(LogicService.selectedScoreTotal())
                    self.scoreIndex = 0
                    self.scoreStringIndex = 0
                    self.totalScore = LogicService.selectedScoreTotal()
                    self.scoreString = [str(self.totalScore)]
        else:
            self.scoreString = self.selectedScoreString(LogicService.scoringHandDice)

        self.scoreString = "".join(self.scoreString)
        self.DrawService.drawHandText(LogicService, self.scoreString.strip())
        
    def shakeDice(self, playerDice, selected=True):
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