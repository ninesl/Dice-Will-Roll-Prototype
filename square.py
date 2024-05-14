import random
import pygame as pg

class Background:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        #create x squares
        self.squares = [self.newSquare() for _ in range(1000)]

    def runBackground(self, screen):
        for iSquare in self.squares:
            screen.blit(iSquare.surf, iSquare.xy)
            iSquare.squarePosition()

    def newSquare(self):
        size = random.randint(100,150)
        squareX = random.randint(0,self.WIDTH - size)
        squareY = random.randint(0,self.HEIGHT - size)
        return Square(squareX, squareY, .5, size, self.WIDTH, self.HEIGHT)
    
    def changeDirection(self):
        for square in self.squares:
            square.xBack = not square.xBack
            square.yBack = not square.yBack


class Square:
    def __init__(self, x, y, speed, size, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT #screen size
        self.xy = [x, y]
        self.incr = speed
        self.size = size
        self.surf = pg.Surface((size, size))
        self.surf.fill(randomColor())

        self.xBack = random.choice([True, False])
        self.yBack = random.choice([True, False])

        # if random.randint(0,2) == 1:
        #     self.xBack = True
        # else:
        #     self.xBack = False

        # if random.randint(0,2) == 1:
        #     self.yBack = True
        # else:
        #     self.yBack = False

    # logic for square direction, changes direction on collision
    def squarePosition(self):
        oldXBack = self.xBack
        oldYBack = self.yBack
        
        if self.xBack:
            self.xy[0] -= self.incr
            if self.xy[0] <= 0:
                self.xy[0] = 0
                self.xBack = False
        else:
            self.xy[0] += self.incr
            if self.xy[0] + self.size >= self.WIDTH:
                self.xy[0] = self.WIDTH - self.size
                self.xBack = True

        if self.yBack:
            self.xy[1] -= self.incr
            if self.xy[1] <= 0:
                self.xy[1] = 0
                self.yBack = False
        else:
            self.xy[1] += self.incr
            if self.xy[1] + self.size >= self.HEIGHT:
                self.xy[1] = self.HEIGHT - self.size
                self.yBack = True

        if oldXBack != self.xBack or oldYBack != self.yBack:
            self.surf.fill(randomColor())

#returns random grey color for square
def randomColor():
    num = random.randint(45,80)
    return pg.Color(num, 
                    num,
                    num)
