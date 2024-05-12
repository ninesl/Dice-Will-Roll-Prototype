import pygame as pg
import dice

class DrawService:
    transparent = pg.Color(0,0,0,0)
    shadow = pg.Color(0,0,0,175)

    def __init__(self, WIDTH, HEIGHT):
        self.gridWidth = 14

        # self.screenColor = self.transparent
        self.screenColor = pg.Color(50,50,50)
        
        # self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.setScreen(WIDTH, HEIGHT)

    def setScreen(self, WIDTH, HEIGHT):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)

        self.dieSide = int(WIDTH / self.gridWidth)

        self.font = pg.font.Font("assets/ringfont.ttf", int(WIDTH / 25))
        self.resetFrame()


    def resetFrame(self):
        self.screen.fill(self.screenColor)
        # background = pg.image.load('assets/background.png')
        # self.screen.blit(background, (0,0))

    def drawDieFace(self, x, y):
        dieFace = pg.Surface((self.dieSide, self.dieSide), pg.SRCALPHA)

        #TODO find dieFace color. I do not want a pg.Color in dice.py if possible
        dieFaceColor = pg.Color(255,255,255)

        dieFace.fill(self.transparent) #background of surface
        pg.draw.rect(dieFace, self.shadow, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x + 4, y + 4]) #shadow
        pg.draw.rect(dieFace, dieFaceColor, dieFace.get_rect(), border_radius=15)
        self.screen.blit(dieFace, [x, y])
    
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

        self.drawDieFace(x, y)
        self.drawPips(x, y, pipGrid)

    def setPipColor(self, pipToDraw, color, border_radius):
        pg.draw.rect(pipToDraw, color, pipToDraw.get_rect(), border_radius=border_radius)


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