import pygame as pg

class DrawService:
    transparent = pg.Color(0,0,0,0)
    shadow = pg.Color(0,0,0,105)

    def __init__(self, WIDTH, HEIGHT):
        self.gridWidth = 14
        self.shadowLength = int(WIDTH / 400)

        # self.screenColor = self.transparent
        self.screenColor = pg.Color(60,55,45)
        
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.setScreen(WIDTH, HEIGHT)

    def setScreen(self, WIDTH, HEIGHT):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)
        self.dieSide = int(WIDTH / self.gridWidth)

        self.gameFont = pg.font.Font("assets/ringfont.ttf", int(WIDTH / 25))
        self.resetFrame()


    def resetFrame(self):
        self.screen.fill(self.screenColor)
        # background = pg.image.load('assets/background.png')
        # self.screen.blit(background, (0,0))

    def drawDieFace(self, x, y, die):
        dieFace = pg.Surface((self.dieSide, self.dieSide), pg.SRCALPHA)
        
        #TODO find dieFace color. I do not want a pg.Color in dice.py if possible
        dieFaceColor = pg.Color(255,255,255)

        dieFace.fill(self.transparent) #background of surface

        if die.isSelected is True:
            dieFace = pg.transform.scale(dieFace,(int(self.dieSide * 1.2), int(self.dieSide * 1.2)))
            #scaled shadow
            x = int(x - self.dieSide * .1)
            y = int(y - self.dieSide * .1)

        pg.draw.rect(dieFace, self.shadow, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x + self.shadowLength, y + self.shadowLength])
        
        pg.draw.rect(dieFace, dieFaceColor, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x, y])

        return dieFace.get_rect().move(x,y) #return rect
    
    #draws pips onto face. Call after drawDieFace()
    def drawPips(self, x, y, pipGrid):
        pipSize = int(self.dieSide / len(pipGrid))

        #TODO pip color find based off pip object
        pipColor = pg.Color(0,0,0)
        pipToDraw = pg.Surface((pipSize, pipSize), pg.SRCALPHA)

        pipToDraw.fill(self.transparent) #background of pip
        pg.draw.rect(pipToDraw, pipColor, pipToDraw.get_rect(), border_radius=5)

        pipY = y - pipSize
        pipX = x
        
        #iterates through grid, draws a pip if 0 isnt found
        for row in pipGrid:
            pipX = x
            for space in row:
                if space != 0: #regular pip
                    self.setPipColor(pipToDraw, pipColor, 5)
                    if space == 2: #regular pip
                        self.setPipColor(pipToDraw, pg.Color("Purple"), 5)
                        self.screen.blit(pipToDraw, [pipX, pipY])
                    self.screen.blit(pipToDraw, [pipX, pipY])
                pipX += pipSize
            pipY += pipSize
    
    def drawDie(self, d, x, y):
        # check for die attributes, color pips etc..
        pipGridNum = 7
        pipGrid = self.getPipGrid(d, pipGridNum)

        dieRect = self.drawDieFace(x, y, d)
        self.drawPips(x, y, pipGrid)

        #for clickable obj
        return (d, dieRect)

    def setPipColor(self, pipToDraw, color, border_radius):
        pg.draw.rect(pipToDraw, color, pipToDraw.get_rect(), border_radius=border_radius)

    def drawDice(self, dice):
        x = int(self.dieSide * self.gridWidth / 6) #starting row of dice
        y = self.dieSide
        diceAndRect = [] #(d, dieRect)
        for die in dice:
            diceAndRect.append(self.drawDie(die, x, y))
            x += self.dieSide * 2 # two grid spaces over
        
        return diceAndRect

    def drawValue(self, num):
        x = self.dieSide * (self.gridWidth / 2) - (self.dieSide / 2)
        y = self.dieSide * 3
        self.drawText(num, x, y)

    def drawText(self, text, x, y):
        img = self.gameFont.render(str(text), True, self.shadow)
        self.screen.blit(img, (x+2,y+2))
        img = self.gameFont.render(str(text), True, pg.Color(255,255,255))
        self.screen.blit(img, (x,y))


    def getPipGrid(self, d, pipGridNum):
        numPips = d.curSide.getPips()
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