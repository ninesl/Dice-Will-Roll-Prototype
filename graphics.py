import pygame as pg
import dice

class DrawService:
    def __init__(self, WIDTH, HEIGHT):
        self.gridWidth = 14

        self.screenColor = pg.Color(0,0,0)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.dieSide = int(WIDTH / self.gridWidth)

        self.dieFace = pg.Surface((self.dieSide, self.dieSide))

        self.font = pg.font.SysFont("Arial", 30)

        self.resetFrame()

    def resetFrame(self):
        self.screen.fill(self.screenColor)
        self.dieFace.fill(pg.Color(255,255,255))

    def drawDie(self, d, x, y):
        # check for die attributes, color dots etc..
        numDots = d.curSide.getDots()
        dotGrid = [[0]*7 for _ in range(7)] #7x7 array
        dotGridNum = 7

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
    
    
        pg.draw.rect(self.dieFace, pg.Color(255, 255, 255), self.dieFace.get_rect(), border_radius=20)
        self.screen.blit(self.dieFace, [x, y])
        
        dotSize = int(self.dieSide / dotGridNum)
        dotToDraw = pg.Surface((dotSize, dotSize))
        # dotToDraw.fill(pg.Color(0,0,0))
        pg.draw.rect(dotToDraw, pg.Color(0, 0, 0), self.dieFace.get_rect(), border_radius=20)

        dotY = y - dotSize
        dotX = x
        for row in dotGrid:
            dotX = x
            for space in row:
                if space == 1: #regular dot
                    self.screen.blit(dotToDraw, [dotX, dotY])
                dotX += dotSize
            dotY += dotSize

    def drawDice(self, dice):
        x = int(self.dieSide * self.gridWidth / 6) #starting row of dice
        y = self.dieSide
        for die in dice:
            self.drawDie(die, x, y)
            x += self.dieSide * 2 # two grid spaces over

    def drawValue(self, num):
        x = self.dieSide * (self.gridWidth / 2)
        y = self.dieSide * (self.gridWidth / 2)
        img = self.font.render(str(num), True, pg.Color(255,255,255))
        self.screen.blit(img, (x,y))
