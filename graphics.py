import pygame as pg
import dice

class DrawService:
    transparent = pg.Color(0,0,0,0)
    shadow = pg.Color(0,0,0,175)

    def __init__(self, WIDTH, HEIGHT):
        self.gridWidth = 14

        # self.screenColor = self.transparent
        self.screenColor = pg.Color(10,10,10)
        
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.setScreen(WIDTH, HEIGHT)

    def setScreen(self, WIDTH, HEIGHT):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)

        self.dieSide = int(WIDTH / self.gridWidth)

        self.font = pg.font.Font("assets/ringfont.ttf", int(WIDTH / 25))
        self.resetFrame()


    def resetFrame(self):
        # self.screen.fill(self.screenColor)
        background = pg.image.load('assets/background.png')
        self.screen.blit(background, (0,0))

    def drawDieFace(self, x, y):
        dieFace = pg.Surface((self.dieSide, self.dieSide), pg.SRCALPHA)

        #TODO find dieFace color. I do not want a pg.Color in dice.py if possible
        dieFaceColor = pg.Color(255,255,255)

        dieFace.fill(self.transparent) #background of surface
        pg.draw.rect(dieFace, self.shadow, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x + 4, y + 4]) #shadow
        pg.draw.rect(dieFace, dieFaceColor, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x, y])
    
    #draws dots onto face. Call after drawDieFace()
    def drawDots(self, x, y, dotGrid):
        dotSize = int(self.dieSide / len(dotGrid))

        #TODO dot color find based off Dot object
        dotColor = pg.Color(0,0,0)
        dotToDraw = pg.Surface((dotSize, dotSize), pg.SRCALPHA)

        dotToDraw.fill(self.transparent) #background of dot
        pg.draw.rect(dotToDraw, dotColor, dotToDraw.get_rect(), border_radius=5)

        dotY = y - dotSize
        dotX = x
        
        #iterates through grid, draws a dot if 0 isnt found
        for row in dotGrid:
            dotX = x
            for space in row:
                if space != 0: #regular dot
                    self.setDotColor(dotToDraw, dotColor, 5)
                    if space == 2: #regular dot
                        self.setDotColor(dotToDraw, pg.Color("Purple"), 5)
                        self.screen.blit(dotToDraw, [dotX, dotY])
                    self.screen.blit(dotToDraw, [dotX, dotY])
                dotX += dotSize
            dotY += dotSize
    
    def drawDie(self, d, x, y):
        # check for die attributes, color dots etc..
        dotGridNum = 7
        dotGrid = self.getDotGrid(d, dotGridNum)

        self.drawDieFace(x, y)
        self.drawDots(x, y, dotGrid)

    def setDotColor(self, dotToDraw, color, border_radius):
        pg.draw.rect(dotToDraw, color, dotToDraw.get_rect(), border_radius=border_radius)


    def drawDice(self, dice):
        x = int(self.dieSide * self.gridWidth / 6) #starting row of dice
        y = self.dieSide
        for die in dice:
            self.drawDie(die, x, y)
            x += self.dieSide * 2 # two grid spaces over

    def drawValue(self, num):
        x = self.dieSide * (self.gridWidth / 2) - (self.dieSide / 2)
        y = self.dieSide * 3
        img = self.font.render(str(num), True, self.shadow)
        self.screen.blit(img, (x+2,y+2))
        img = self.font.render(str(num), True, pg.Color(255,255,255))
        self.screen.blit(img, (x,y))

    def getDotGrid(self, d, dotGridNum):
        numDots = d.curSide.getDots()
        dotGrid = [[0]*dotGridNum for _ in range(dotGridNum)] #7x7 array
        
        match numDots:
            case 1:
                dotGrid[4] = [0,0,0,1,0,0,0]
            case 2:
                dotGrid[2] = [0,1,0,0,0,0,0]
                dotGrid[6] = [0,0,0,0,0,1,0]
            case 3:
                dotGrid[2] = [0,0,0,0,0,1,0]
                dotGrid[4] = [0,0,0,1,0,0,0]
                dotGrid[6] = [0,1,0,0,0,0,0]
            case 4:
                dotGrid[2] = [0,1,0,0,0,1,0]
                dotGrid[6] = [0,1,0,0,0,1,0]
            case 5:
                dotGrid[2] = [0,1,0,0,0,1,0]
                dotGrid[4] = [0,0,0,1,0,0,0]
                dotGrid[6] = [0,1,0,0,0,1,0]
            case 6:
                dotGrid[2] = [0,1,0,0,0,1,0]
                dotGrid[4] = [0,1,0,0,0,1,0]
                dotGrid[6] = [0,1,0,0,0,1,0]
            case 7:
                dotGrid[2] = [0,1,0,0,0,1,0]
                dotGrid[4] = [0,1,0,1,0,1,0]
                dotGrid[6] = [0,1,0,0,0,1,0]
            case 8:
                dotGrid[2] = [0,1,0,1,0,1,0]
                dotGrid[4] = [0,1,0,0,0,1,0]
                dotGrid[6] = [0,1,0,1,0,1,0]
            case 9:
                dotGrid[2] = [0,1,0,1,0,1,0]
                dotGrid[4] = [0,1,0,1,0,1,0]
                dotGrid[6] = [0,1,0,1,0,1,0]

        return dotGrid