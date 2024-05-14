import pygame as pg

class DrawService:
    transparent = pg.Color(0,0,0,0)
    shadow = pg.Color(0,0,0,105)
    selectedColor = pg.Color(255,100,50,34)
    screenColor = pg.Color(40,40,40)

    dieRadius = 15

    def __init__(self, WIDTH, HEIGHT):
        self.gridWidth = 14
        self.shadowLength = int(WIDTH / 400)
        
        self.setScreen(WIDTH, HEIGHT)

        # self.screenColor = self.transparent
        
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.resetFrame()

    def setScreen(self, WIDTH, HEIGHT):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)
        self.dieSide = int(WIDTH / self.gridWidth)
        self.dieSpacing = int(self.dieSide * 1.5)

        self.diceX = int(self.dieSide * self.gridWidth / 2.5) #starting row of dice
        self.diceY = self.dieSide

        self.gameFont = pg.font.Font("assets/ringfont.ttf", int(WIDTH / 25))

    def resetFrame(self):
        self.screen.fill(self.screenColor)
        # background = pg.image.load('assets/background.png')
        # self.screen.blit(background, (0,0))

    def drawDieFace(self, x, y, die):
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
    
    def drawDice(self, dice):
        diceAndRect = [] #(d, dieRect)
        x = self.diceX
        y = self.diceY
        for die in dice:
            diceAndRect.append(self.drawDie(die, x, y))
            x += self.dieSpacing # num grid spaces over
        return diceAndRect

    def drawDie(self, d, x, y):
        # check for die attributes, color pips etc..
        pipGridNum = 7
        pipGrid = self.getPipGrid(d, pipGridNum)

        dieRect = self.drawDieFace(x, y, d)
        self.drawPips(x, y, pipGrid, d)

        #for clickable obj
        return (d, dieRect)

    def drawValue(self, num):
        x = self.dieSide
        y = self.dieSide
        self.drawText(num, x, y)

    def drawText(self, text, x, y):
        img = self.gameFont.render(str(text), True, self.shadow)
        self.screen.blit(img, (x+2,y+2))
        img = self.gameFont.render(str(text), True, pg.Color(255,255,255))
        self.screen.blit(img, (x,y))

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
                    outline_rect = pg.Rect(pipX - pipSize * .15,
                                       pipY- pipSize * .14,
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