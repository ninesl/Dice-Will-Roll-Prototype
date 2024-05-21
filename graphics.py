import pygame as pg
import shapes

class DrawService:
    transparent = pg.Color(0,0,0,0)
    shadow = pg.Color(0,0,0,105)
    scoredColor = pg.Color(100,255,50,34)
    selectedColor = pg.Color(255,255,255,134)

    BACKGROUND_COLOR_RANGE_DIFF = 25

    dieRadius = 15
    allHands = []

    def __init__(self, WIDTH, HEIGHT, NUM_SHAPES = 150, rangeNum = 100):
        self.NUM_SHAPES = NUM_SHAPES
        self.allHands = []

        self.gameFonts = []

        bigFont = int(WIDTH / 25)
        smallFont = int(WIDTH / 40)
        self.gameFonts.append(pg.font.Font("assets/fonts/ringfont.ttf", bigFont))
        self.gameFonts.append(pg.font.Font("assets/fonts/fantasquesansmono.otf", smallFont))
        self.gameFonts.append(pg.font.Font("assets/fonts/Kurland.ttf", bigFont))
        self.gameFonts.append(pg.font.Font("assets/fonts/5x5.ttf", smallFont))
        self.gameFonts.append(pg.font.Font("assets/fonts/amaranth.otf", smallFont))
        
        self.setScreen(WIDTH, HEIGHT, rangeNum)

    def setBackground(self, rangeNum):
        self.BackgroundService = shapes.Background(self.WIDTH, self.HEIGHT, NUM_SHAPES=self.NUM_SHAPES, colorRangeNum=rangeNum)
        self.setBackgroundColors(rangeNum)

    def setBackgroundColors(self, rangeNum, selectedDice = []):
        self.screenColor = shapes.randomColor(rangeNum - self.BACKGROUND_COLOR_RANGE_DIFF)
        self.BackgroundService.setRockColors(rangeNum)
        self.BackgroundService.changeShapeColors(selectedDice)

    def deleteRocks(self, num):
        self.BackgroundService.deleteRocks(num)

    def setScreen(self, WIDTH, HEIGHT, rangeNum = 100):
        self.gridSpaces = 10
        self.heightGrid = HEIGHT/self.gridSpaces
        self.widthGrid = WIDTH/self.gridSpaces
        self.shadowLength = int(WIDTH / 400)
        self.marginX = self.widthGrid * .05
        self.marginY = self.heightGrid * .05

        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.DOUBLEBUF)
        # self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.DOUBLEBUF)
        # self.screen = pg.display.set_mode((0,0), pg.DOUBLEBUF | pg.FULLSCREEN)

        self.dieSide = int(WIDTH / (self.gridSpaces + 5))
        self.dieSpacing = int(self.marginX * 5)

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.levelDiceY = self.dieSide

        self.setBackground(rangeNum)

    def resetFrame(self):
        self.screen.fill(self.screenColor)
        self.BackgroundService.runBackground(self.screen)
        # background = pg.image.load('assets/background.png')
        # self.screen.blit(background, (0,0))

    def drawDieFace(self, x, y, die, isInScoringDice = False):
        dieFace = pg.Surface((self.dieSide, self.dieSide), pg.SRCALPHA)
        
        #TODO find dieFace color. I do not want a pg.Color in dice.py if possible
        dieFaceColor = die.getColor()

        dieFace.fill(self.transparent) #background of surface

        if die.isSelected:
            # Apply scaling and outline for selected die
            outline_thickness = self.dieRadius/3  # Thickness of the outline
            scaled_die_side = int(self.dieSide * 1.2)
            dieFace = pg.transform.scale(dieFace, (scaled_die_side, scaled_die_side))

            outline_rect = pg.Rect(x - self.dieSide * 0.1 - outline_thickness,
                                   y - self.dieSide * 0.1 - outline_thickness,
                                   scaled_die_side + outline_thickness * 2,
                                   scaled_die_side + outline_thickness * 2)
            
            #outline for scoring
            if die.isSelected:
                if isInScoringDice:
                    pg.draw.rect(self.screen, self.scoredColor, outline_rect, border_radius=self.dieRadius)
                else:
                    pg.draw.rect(self.screen, self.selectedColor, outline_rect, border_radius=self.dieRadius)

            x = int(x - self.dieSide * .1)
            y = int(y - self.dieSide * .1)

        #shadow
        pg.draw.rect(dieFace, self.shadow, dieFace.get_rect(), border_radius=self.dieRadius)
        self.screen.blit(dieFace, [x + self.shadowLength, y + self.shadowLength])

        #background for hovering
        pg.draw.rect(dieFace, pg.Color(200,200,200), dieFace.get_rect(), border_radius=self.dieRadius)
        self.screen.blit(dieFace, [x, y])

        #die face
        pg.draw.rect(dieFace, dieFaceColor, dieFace.get_rect(), border_radius=self.dieRadius)
        self.screen.blit(dieFace, [x, y])

        return dieFace.get_rect().move(x,y) #return rect
    
    def getTotalDiceWidth(self, dice):
        return len(dice) * self.dieSide + (len(dice) - 1) * self.dieSpacing

    def drawDice(self, dice, scoredDice=None, x=None, y=None):
        if x is None:
            totalWidth = self.getTotalDiceWidth(dice)
            x = (self.WIDTH - totalWidth) // 2

        if y is None:
            y = self.levelDiceY

        diceAndRect = []  # (d, dieRect)
        for die in dice:
            isInScoringDice = scoredDice and die in scoredDice
            diceAndRect.append(self.drawDie(die, x, y, isInScoringDice))
            x += self.dieSide + self.dieSpacing

        return diceAndRect

    def drawDie(self, die, x, y, isInScoringDice = False):
        # check for die attributes, color pips etc..
        pipGridNum = 7
        pipGrid = self.getPipGrid(die, pipGridNum)

        dieRect = self.drawDieFace(x, y, die, isInScoringDice)
        self.drawPips(x, y, pipGrid, die)

        #for clickable obj
        return (die, dieRect)

    def drawAllDiceFaces(self, playerDice):
        xSpacing = 0
        ySpacing = 0
        diceAndRect = []
        oldDieSide = self.dieSide
        self.dieSide /= 1.25
        for die in playerDice:
            for sideIndex in range(die.getNumSides()):
                die.curSide = die.sides[sideIndex]
                diceAndRect.append(self.drawDie(die, self.marginX + xSpacing, self.marginY + ySpacing))
                xSpacing += self.dieSide + self.marginX
            xSpacing = 0
            ySpacing += self.dieSide + self.marginY
        self.dieSide = oldDieSide
        return diceAndRect

    def drawText(self, index, msg, x, y, color = pg.Color(255,255,255), center = False):
        if center:
            text = self.gameFonts[index].render(str(msg), True, self.shadow)
            rect = text.get_rect(center = (self.WIDTH//2 + 2 + x, self.HEIGHT//2 + 2 + y))
            self.screen.blit(text, rect)

            text = self.gameFonts[index].render(str(msg), True, color)
            rect = text.get_rect(center = (self.WIDTH//2 + x, self.HEIGHT//2 + y))
            self.screen.blit(text, rect)
        else:
            img = self.gameFonts[index].render(str(msg), True, self.shadow)
            self.screen.blit(img, (x+2,y+2))
            img = self.gameFonts[index].render(str(msg), True, color)
            self.screen.blit(img, (x,y))

    def drawHandText(self, LogicService, diceChars):
        currentHandStr = str(f"{LogicService.hand.value[0]}  X {LogicService.hand.value[1]}")
        self.drawText(2, currentHandStr, 0,-self.heightGrid * 1.5, center=True)
        self.drawText(2, f"{diceChars}", 0,-self.heightGrid * .75, center=True)

    def drawLevelText(self, LogicService):
        #game info
        self.drawText(1,f"{LogicService.rollsLeft} rolls", self.marginX,self.marginY, center=True)
        self.drawText(1,f"{LogicService.handsLeft} hands", self.marginX,self.heightGrid * .5 + self.marginY, center=True)
        self.drawText(1,f"{LogicService.rockHealth} rocks",                              self.marginX,self.heightGrid + self.marginY, center=True)

    def drawPreviousHands(self):
        yNum = 9.5
        for strHand in self.allHands:
            self.drawText(1, f"{strHand}", self.marginX, self.heightGrid * yNum - self.marginY)
            yNum -= .5

    def drawControlsText(self, controlList = []):
        #controls
        heightModifier = self.gridSpaces - len(controlList) / 2
        for controlText in controlList:
            self.drawText(1, controlText, self.widthGrid * 8 + self.marginX * 2, self.heightGrid * heightModifier - self.marginY)
            heightModifier += .5

    #draws pips onto face. Call after drawDieFace()
    def drawPips(self, x, y, pipGrid, d):
        pipSize = int(self.dieSide / len(pipGrid))
        sidePips = d.curSide.getPips()

        #TODO pip color find based off pip object

        pipToDraw = pg.Surface((pipSize, pipSize), pg.SRCALPHA)

        pipToDraw.fill(self.transparent) #background of pip

        pipY = y - pipSize
        pipX = x
        
        #iterates through grid, draws a pip if 0 isnt found
        i = 0
        pipRadius = int(self.dieRadius / 2)
        for row in pipGrid:
            pipX = x
            for space in row:
                if space == 1: # pip found
                    # Apply scaling and outline for selected die
                    outline_thickness = 5  # Thickness of the outline
                    scaled_pip = int(pipSize * 1.1)

                    # Calculate outline rectangle position and size
                    outline_rect = pg.Rect(pipX - pipSize * .13,
                                       pipY- pipSize * .13,
                                       scaled_pip + outline_thickness,
                                       scaled_pip + outline_thickness)
                    
                    pg.draw.rect(self.screen, self.shadow, outline_rect, border_radius=pipRadius)
                    # self.screen.blit(pipToDraw, [pipX, pipY])
                    
                    pipToDraw.fill(self.transparent)  # Reset the `pipToDraw` surface
                    pg.draw.rect(pipToDraw, sidePips[i].getPipColor(), pipToDraw.get_rect(), border_radius=pipRadius)
                    self.screen.blit(pipToDraw, [pipX, pipY])

                    i += 1
                # self.screen.blit(pipToDraw, [pipX, pipY])
                pipX += pipSize
            pipY += pipSize

    def getPipGrid(self, d, pipGridNum):
        numPips = d.curSide.getNum()
        pipGrid = [[0]*pipGridNum for _ in range(pipGridNum)] #7x7 array
        
        match numPips:
            case 1:
                pipGrid[4] = [0,0,0,1,0,0,0]
            case 2:
                pipGrid[2] = [0,1,0,0,0,0,0]
                pipGrid[6] = [0,0,0,0,0,1,0]
            case 3:
                pipGrid[2] = [0,0,0,0,0,1,0]
                pipGrid[4] = [0,0,0,1,0,0,0]
                pipGrid[6] = [0,1,0,0,0,0,0]
            case 4:
                pipGrid[2] = [0,1,0,0,0,1,0]
                pipGrid[6] = [0,1,0,0,0,1,0]
            case 5:
                pipGrid[2] = [0,1,0,0,0,1,0]
                pipGrid[4] = [0,0,0,1,0,0,0]
                pipGrid[6] = [0,1,0,0,0,1,0]
            case 6:
                pipGrid[2] = [0,1,0,0,0,1,0]
                pipGrid[4] = [0,1,0,0,0,1,0]
                pipGrid[6] = [0,1,0,0,0,1,0]
            case 7:
                pipGrid[2] = [0,1,0,0,0,1,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[6] = [0,1,0,0,0,1,0]
            case 8:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[4] = [0,1,0,0,0,1,0]
                pipGrid[6] = [0,1,0,1,0,1,0]
            case 9:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[6] = [0,1,0,1,0,1,0]
        return pipGrid