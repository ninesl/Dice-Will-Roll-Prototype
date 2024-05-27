import pygame as pg
import shapes
from dice import blankDie
# pg.font.init()
class DrawService:
    transparentColor = pg.Color(0,0,0,0)
    shadowColor = pg.Color(0,0,0,105)
    scoredColor = pg.Color(100,255,50,34)
    selectedColor = pg.Color(255,255,255,134)

    BACKGROUND_COLOR_RANGE_DIFF = 25

    dieRadius = 15
    allRecentHands = []

    def __init__(self, WIDTH, HEIGHT, NUM_SHAPES = 150, rangeNum = 100):
        self.NUM_SHAPES = NUM_SHAPES

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

    def resetRocks(self, rockHealth):
        self.NUM_SHAPES = rockHealth
        self.BackgroundService.setRocks(rockHealth)

    def setScreen(self, WIDTH, HEIGHT, rangeNum = 100):
        self.gridSpaces = 10
        self.heightGrid = HEIGHT/self.gridSpaces
        self.widthGrid = WIDTH/self.gridSpaces
        self.shadowColorLength = int(WIDTH / 400)
        self.marginX = self.widthGrid * .05
        self.marginY = self.heightGrid * .05

        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.DOUBLEBUF, 32)
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

    def drawDieFace(self, x, y, die, isInScoringDice=False):
        dieFace = pg.Surface((self.dieSide, self.dieSide), pg.SRCALPHA)
        dieFace.fill(self.transparentColor)  # background of surface

        if die.isSelected:
            # Apply scaling and outline for selected die
            outline_thickness = self.dieRadius / 3  # Thickness of the outline
            scaled_die_side = int(self.dieSide * 1.2)
            dieFace = pg.transform.scale(dieFace, (scaled_die_side, scaled_die_side))

            outline_rect = pg.Rect(x - self.dieSide * 0.1 - outline_thickness,
                                   y - self.dieSide * 0.1 - outline_thickness,
                                   scaled_die_side + outline_thickness * 2,
                                   scaled_die_side + outline_thickness * 2)

            # outline for scoring
            if die.isSelected:
                if isInScoringDice:
                    pg.draw.rect(self.screen, self.scoredColor, outline_rect, border_radius=self.dieRadius)
                else:
                    pg.draw.rect(self.screen, self.selectedColor, outline_rect, border_radius=self.dieRadius)

            x = int(x - self.dieSide * .1)
            y = int(y - self.dieSide * .1)

        shadowSurface = pg.Surface(dieFace.get_size(), pg.SRCALPHA)
        shadowSurface.fill(self.transparentColor)

        # Draw the appropriate shape based on the number of sides
        numSides = die.getNumSides()
        if numSides <= 2:
            self.drawCircle(dieFace, die.curSide.color)
            self.drawCircle(shadowSurface, self.shadowColor)
        else:
            self.drawSquare(dieFace, die.curSide.color)
            self.drawSquare(shadowSurface, self.shadowColor)

        self.screen.blit(shadowSurface, [x + self.shadowColorLength, y + self.shadowColorLength])
        self.screen.blit(dieFace, [x, y])

        return dieFace.get_rect().move(x, y)  # return rect

    def drawCircle(self, surface, color):
        radius = surface.get_width() // 2
        pg.draw.circle(surface, color, (radius, radius), radius)

    def drawSquare(self, surface, color):
        pg.draw.rect(surface, color, (0, 0, surface.get_width(), surface.get_height()), border_radius=self.dieRadius)

    def getTotalDiceWidth(self, dice):
        return len(dice) * self.dieSide + (len(dice) - 1) * self.dieSpacing

    def drawDice(self, dice, scoredDice=None, x=None, y=None):
        if x is None:
            totalWidth = self.getTotalDiceWidth(dice)
            x = (self.WIDTH - totalWidth) // 2

        if y is None:
            y = self.levelDiceY

        dieRectsList = []  # To hold tuples of (die, dieRect)
        pipRectsList = []  # To hold lists of tuples of [(pip, pipRect)]

        for die in dice:
            isInScoringDice = scoredDice and die in scoredDice
            (die, dieRect), pipRects = self.drawDie(die, x, y, isInScoringDice)
            dieRectsList.append((die, dieRect))
            pipRectsList.append(pipRects)
            x += self.dieSide + self.dieSpacing

        return dieRectsList, pipRectsList

    def drawDie(self, die, x, y, isInScoringDice = False):
        # check for die attributes, color pips etc..
        pipGridNum = 7
        pipGrid = self.getPipGrid(die, pipGridNum)

        dieRect = self.drawDieFace(x, y, die, isInScoringDice)
        pipAndRect = self.drawPips(x, y, pipGrid, die)

        #for clickable obj
        return (die, dieRect), pipAndRect
    
    def drawDieInfoFaces(self, die):
        oldDieSide = self.dieSide
        self.dieSide = self.HEIGHT / 14
        # xSpacing = 0
        ySpacing = 0
        currentSide = die.curSide
        for sideIndex in range(die.getNumSides()):
            die.curSide = die.sides[sideIndex]
            self.drawDie(die, self.WIDTH - self.dieSide - self.marginX, self.marginY + ySpacing)
            # xSpacing += self.dieSide + self.marginX
            ySpacing += self.dieSide + self.marginY
        die.curSide = currentSide
        self.dieSide = oldDieSide

    def drawAllDiceFaces(self, playerDice):
        xSpacing = 0
        ySpacing = 0

        dieRectsList = []  # To hold tuples of (die, dieRect)
        pipRectsList = []  # To hold lists of tuples of [(pip, pipRect)]
        sideRectsList = [] # To hold lists of tuples of (side, sideRect)

        oldDieSide = self.dieSide
        self.dieSide /= 1 #draw smaller

        for die in playerDice:
            for sideIndex in range(die.getNumSides()):
                die.curSide = die.sides[sideIndex]
                (die, dieRect), pipRects = self.drawDie(die, self.marginX + xSpacing, self.marginY + ySpacing)
                dieRectsList.append((die, dieRect))
                pipRectsList.append(pipRects)
                sideRectsList.append((die.curSide, dieRect))
                xSpacing += self.dieSide + self.marginX
            xSpacing = 0
            ySpacing += self.dieSide + self.marginY

        # for _ in range(5 - len(playerDice)):
        #     for sideIndex in range(blankDie.getNumSides()):
        #         self.drawDie(blankDie, self.marginX + xSpacing, self.marginY + ySpacing)
        #         xSpacing += self.dieSide + self.marginX
        #     xSpacing = 0
        #     ySpacing += self.dieSide + self.marginY

        self.dieSide = oldDieSide

        return dieRectsList, pipRectsList, sideRectsList

    # default_font = pg.font.Font(None, 20)
    def drawText(self, msg, x, y, color = pg.Color(255,255,255), center = False, fontIndex = None):
        if fontIndex != None:
            if center:
                text = self.gameFonts[fontIndex].render(str(msg), True, self.shadowColor)
                rect = text.get_rect(center = (self.WIDTH//2 + 2 + x, self.HEIGHT//2 + 2 + y))
                self.screen.blit(text, rect)
                text = self.gameFonts[fontIndex].render(str(msg), True, color)
                rect = text.get_rect(center = (self.WIDTH//2 + x, self.HEIGHT//2 + y))
                self.screen.blit(text, rect)
            else:
                img = self.gameFonts[fontIndex].render(str(msg), True, self.shadowColor)
                self.screen.blit(img, (x+2,y+2))
                img = self.gameFonts[fontIndex].render(str(msg), True, color)
                self.screen.blit(img, (x,y))

    def drawHandText(self, LogicService, diceChars):
        currentHandStr = f"{LogicService.hand.value[0]}"
        currentHandMultStr = f"x{LogicService.hand.value[1]}"
        self.drawText(currentHandStr, 0,0, center=True, fontIndex=0)
        self.drawText(currentHandMultStr, 0,self.heightGrid//1.5, center=True, fontIndex=1)
        self.drawText(f"{diceChars}", 0,-self.heightGrid * .75, center=True, fontIndex=2)

    def drawLevelText(self, LogicService):
        #game info
        self.drawText(f"{LogicService.rockHealth} rocks",0,-self.heightGrid * 4.5 + self.marginY, center=True, fontIndex=2)
        self.drawLevelInfo(LogicService)

    def drawLevelInfo(self, LogicService):
        self.drawText(f"{LogicService.rollsLeft}/{LogicService.STARTING_ROLLS} rolls", self.widthGrid,-self.heightGrid * 2, center=True, fontIndex=1)
        self.drawText(f"{LogicService.handsLeft}/{LogicService.STARTING_HANDS} hands", -self.widthGrid,-self.heightGrid * 2, center=True, fontIndex=1)

    def drawPreviousHands(self):
        yNum = 0
        for strHand in self.allRecentHands:
            self.drawText(f"{strHand}", self.marginX, self.heightGrid * yNum + self.marginY, fontIndex=1)
            yNum += .5
            
    def drawRevealedHands(self, revealedHandsDict):
        yNum = 0
        for key, value in revealedHandsDict.items():
            self.drawText(f"{key}: x{value}", self.marginX, self.heightGrid * yNum + self.marginY, fontIndex=1)
            yNum += .5

    def drawBestHand(self, bestHandStr):
        self.drawText(f"{bestHandStr}",0,-self.heightGrid * 2.4,fontIndex=1, center=True)

    def drawControlsText(self, controlList = []):
        #controls
        heightModifier = self.gridSpaces - len(controlList) / 2
        for controlText in controlList:
            self.drawText(controlText, self.widthGrid * 8 + self.marginX * 2, self.heightGrid * heightModifier - self.marginY, fontIndex=1)
            heightModifier += .5

    #draws pips onto face. Call after drawDieFace()
    def drawPips(self, x, y, pipGrid, d):
        pipSize = int(self.dieSide / len(pipGrid))
        sidePips = d.curSide.getPips()

        #TODO pip color find based off pip object

        pipToDraw = pg.Surface((pipSize, pipSize), pg.SRCALPHA)

        pipToDraw.fill(self.transparentColor) #background of pip

        pipY = y - pipSize
        pipX = x
        
        #iterates through grid, draws a pip if 0 isnt found
        i = 0
        pipRadius = int(self.dieRadius / 2)
        pipRect = []
        for row in pipGrid:
            pipX = x
            for space in row:
                if space == 1: # pip found
                    # Apply scaling and outline for selected die
                    outline_thickness = 3 # Thickness of the outline
                    scaled_pip = int(pipSize * 1.1)

                    # Calculate outline rectangle position and size
                    outline_rect = pg.Rect(pipX - pipSize * .13,
                                       pipY- pipSize * .13,
                                       scaled_pip + outline_thickness,
                                       scaled_pip + outline_thickness)
                    
                    pg.draw.rect(self.screen, self.shadowColor, outline_rect, border_radius=pipRadius)
                    # self.screen.blit(pipToDraw, [pipX, pipY])
                    
                    pipToDraw.fill(self.transparentColor)  # Reset the `pipToDraw` surface
                    pg.draw.rect(pipToDraw, sidePips[i].getPipColor(), pipToDraw.get_rect(), border_radius=pipRadius)
                    self.screen.blit(pipToDraw, [pipX, pipY])

                    pipRect.append((sidePips[i], outline_rect))
                    i += 1
                # self.screen.blit(pipToDraw, [pipX, pipY])
                pipX += pipSize
            pipY += pipSize
        return pipRect
            
    def getPipGrid(self, d, pipGridNum):
        numPips = d.curSide.getNum()
        pipGrid = [[0]*pipGridNum for _ in range(pipGridNum)] #7x7 array
        # numSides = d.getNumSides()
        match numPips:
            case 1:
                pipGrid[4] = [0,0,0,1,0,0,0]
            case 2:
                pipGrid[2] = [0,0,0,0,0,1,0]
                pipGrid[6] = [0,1,0,0,0,0,0]
            case 3:
                pipGrid[2] = [0,1,0,0,0,0,0]
                pipGrid[4] = [0,0,0,1,0,0,0]
                pipGrid[6] = [0,0,0,0,0,1,0]
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
            case 10:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[3] = [0,0,0,0,1,0,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[5] = [0,0,0,0,0,0,0]
                pipGrid[6] = [0,1,0,1,0,1,0]
            case 11:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[3] = [0,0,0,0,1,0,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[5] = [0,0,1,0,0,0,0]
                pipGrid[6] = [0,1,0,1,0,1,0]
            case 12:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[3] = [0,0,0,0,1,0,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[5] = [0,0,1,0,1,0,0]
                pipGrid[6] = [0,1,0,1,0,1,0]
            case 13:
                pipGrid[2] = [0,1,0,1,0,1,0]
                pipGrid[3] = [0,0,1,0,1,0,0]
                pipGrid[4] = [0,1,0,1,0,1,0]
                pipGrid[5] = [0,0,1,0,1,0,0]
                pipGrid[6] = [0,1,0,1,0,1,0]

        if d.getNumSides() <= 2:
            match numPips:
                case 1:
                    pipGrid[4] = [0,0,0,1,0,0,0]
                case 2:
                    pipGrid[2] = [0,0,0,0,1,0,0]
                    pipGrid[6] = [0,0,1,0,0,0,0]

        return pipGrid
    
    buttons = []
    def setButtons(self, text, vertical=False):
        num_buttons = len(text)
        button_width = self.WIDTH / self.gridSpaces * 4
        button_height = self.HEIGHT / (self.gridSpaces * 1.5)
        spacing = 10  # Adjust spacing as needed
        
        # Calculate total dimensions and starting positions
        if vertical:
            total_height = num_buttons * button_height + (num_buttons - 1) * spacing
            startY = (self.HEIGHT - total_height) / 2 + button_height / 2
            centerX = self.WIDTH / 4 * 3
        else:
            total_width = num_buttons * button_width + (num_buttons - 1) * spacing
            startX = (self.WIDTH - total_width) / 2 + button_width / 2
            centerY = self.HEIGHT / 4 * 3
        
        buttonColor = pg.Color(200, 200, 200, 255)
        font = self.gameFonts[2]
        self.buttons = []  # Reset buttons list

        for string in text:
            if vertical:
                newButton = Button(centerX, startY, button_width, button_height, buttonColor, string, font, self.screen, shadowColor=self.shadowColor, shadowOffset=self.shadowColorLength, borderRadius=self.dieRadius)
                startY += button_height + spacing  # Move to the next position, including spacing
            else:
                newButton = Button(startX, centerY, button_width, button_height, buttonColor, string, font, self.screen, shadowColor=self.shadowColor, shadowOffset=self.shadowColorLength, borderRadius=self.dieRadius)
                startX += button_width + spacing  # Move to the next position, including spacing
            
            self.buttons.append(newButton)

        return self.buttons
        

    def drawButtons(self, buttons):
        buttonRect = []
        for button in buttons:
            buttonRect.append(button.draw())
        return buttonRect

class Button:
    def __init__(self, centerX, centerY, width, height, color, text, font, screen, shadowColor, shadowOffset, borderRadius, action = None, fontColor = pg.Color(255,255,255,255)):
        self.centerX = centerX
        self.centerY = centerY
        self.borderRadius = borderRadius
        self.color = color
        self.text = text
        self.font = font
        self.screen = screen
        self.shadowColor = shadowColor
        self.fontColor = fontColor
        self.shadowOffset = shadowOffset
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.center = (centerX, centerY)
        self.textSurface = self.font.render(self.text, True, self.fontColor)
        self.textShadowSurface = self.font.render(self.text, True, self.shadowColor)
        self.isClicked = False
        self.action = action

    def click(self):
        self.isClicked = not self.isClicked

    def setAction(self, action):
        self.action = action

    def updateText(self, newText):
        self.text = newText
        self.textSurface = self.font.render(self.text, True, self.fontColor)
        self.textShadowSurface = self.font.render(self.text, True, self.shadowColor)

    def draw(self):
        buttonColor = self.color
        if self.isClicked:
            buttonColor = pg.Color(0,0,0)
            
        # Draw button shadow
        shadowRect = self.rect.copy()
        shadowRect.topleft = (self.rect.left + self.shadowOffset, self.rect.top + self.shadowOffset)
        shadowSurface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.rect(shadowSurface, self.shadowColor, shadowSurface.get_rect(), border_radius=self.borderRadius)
        self.screen.blit(shadowSurface, shadowRect.topleft)

        # Draw button
        buttonSurface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.rect(buttonSurface, buttonColor, buttonSurface.get_rect(), border_radius=self.borderRadius)
        self.screen.blit(buttonSurface, self.rect.topleft)

        # Draw text shadow
        textShadowRect = self.textShadowSurface.get_rect(center=self.rect.center)
        textShadowRect.topleft = (textShadowRect.left + self.shadowOffset // 2, textShadowRect.top + self.shadowOffset // 2)
        self.screen.blit(self.textShadowSurface, textShadowRect)

        # Draw text
        textRect = self.textSurface.get_rect(center=self.rect.center)
        self.screen.blit(self.textSurface, textRect)

        return self, self.rect