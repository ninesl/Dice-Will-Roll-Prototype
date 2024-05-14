import random
import pygame as pg

class Background:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.squares = []
        for i in range(1000):
            self.squares.append(self.newSquare())

    def runBackground(self, screen):
        for iSquare in self.squares:
            screen.blit(iSquare.surf, iSquare.xy)
            iSquare.squarePosition()

    def newSquare(self):
        size = random.randint(100,150)
        squareX = random.randint(0,self.WIDTH)
        squareY = random.randint(0,self.HEIGHT)
        return Square(squareX, squareY, .5, size, self.WIDTH, self.HEIGHT)


class Square:
    def __init__(self, x, y, speed, size, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT #screen size
        self.xy = [x, y]
        self.incr = speed
        self.size = size
        self.surf = pg.Surface((size, size))
        self.surf.fill(randomColor())

        if random.randint(0,2) == 1:
            self.xBack = True
        else:
            self.xBack = False

        if random.randint(0,2) == 1:
            self.yBack = True
        else:
            self.yBack = False

    # logic for square direction, changes direction on collision
    def squarePosition(self):
        oldXBack = self.xBack
        oldYBack = self.yBack
        
        if self.xBack: #going left
            x = self.xy[0] - self.incr
            if x <= 0:
                self.xBack = False
        else: #going right
            x = self.xy[0] + self.incr
            if x + self.size >= self.WIDTH:
                x = self.WIDTH - self.size # keeps inbounds
                self.xBack = True

        if self.yBack: #going down
            y = self.xy[1] - self.incr
            self.yBack = y >= 0
        else: #going up
            y = self.xy[1] + self.incr
            if y + self.size >= self.HEIGHT:
                y = self.HEIGHT - self.size # keeps inbounds
                self.yBack = True  # Change direction to up

        #change color on collision. bool only changes when hit
        if oldXBack != self.xBack or oldYBack != self.yBack:
            self.surf.fill(randomColor())

        self.xy = [x, y]

def randomColor():
    # return pg.Color(rand.randint(80,90), 
    #                 rand.randint(55,60),
    #                 rand.randint(25,35))
    num = random.randint(45,80)
    return pg.Color(num, 
                    num,
                    num)
