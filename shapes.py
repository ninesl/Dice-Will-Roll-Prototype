import random
import pygame as pg
import math

class Background:
    def __init__(self, WIDTH, HEIGHT, NUM_SHAPES = 100, colorRangeNum = 100, oneXthOfRocks = 6):
        #Adjust to set bounds for shapes bouncing
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        #makes NUM_SHAPES to use with speed (.5)
        self.shapes = [self.newShape(.2, colorRangeNum) for _ in range(NUM_SHAPES)]

        #rocks that change colors
        self.numShapesToChange = len(self.shapes) // oneXthOfRocks
        self.changingShapesArray = []
        self.changingShapes = []

    def runBackground(self, screen):
        for shape in self.shapes:
            shape.updatePosition()
            shape.updateColor()
            shape.draw(screen)

    def newShape(self, speed, colorRangeNum):
        size = random.randint(50, 150)
        shapeX = random.randint(0 + size, self.WIDTH - size)
        shapeY = random.randint(0 + size, self.HEIGHT - size)
        return Shape(shapeX, shapeY, speed, size, self.WIDTH, self.HEIGHT, colorRangeNum)

    def changeDirection(self):
        for shape in self.shapes:
            shape.xBack = not shape.xBack
            shape.yBack = not shape.yBack

    # going 'deeper' by the level...
    def setRockColors(self, num):
        for shape in self.shapes:
            shape.setFullColor(num)

    #returns the new shapes to change so they can be removed later
    def addChangingShapes(self, selectedDie):
        #newShapes are the shapes being added to be accessed later
        newShapes = random.sample(self.shapes, self.numShapesToChange)
        #changingShapes is the full list of shapes
        self.changingShapes.extend(newShapes)

        newColor = selectedDie.curSide.color
        # Change the color of the selected shapes to the color of a selected die
        for shape in newShapes:
            shape.setTargetColor(newColor)

        newShapes.append(selectedDie) #die flag

        self.changingShapesArray.append(newShapes)

    def deleteRocks(self):
        self.changingShapesArray = []
        for shape in self.shapes:
            shape.setFullColor(shape.colorRange)

    #takes list of shapes to remove, gotten from addChangingShapes()
    def removeChangingShapes(self, removedShapes):
        removedShapes.pop() # remove dieflag at the end of array
        for shape in removedShapes:
            shape.setFullColor(shape.colorRange)
        self.changingShapesArray.remove(removedShapes)

    def changeShapeColors(self, selectedDice, selectedDie = None):
        if not selectedDie:
            return
        
        #selectedColors = [die.curSide.color for die in selectedDice]

        # finds last element of shapesList, last element is the die used
        # this is done when a die is removed from selectedDice
        if selectedDie not in selectedDice:
            for shapesList in self.changingShapesArray:
                if shapesList[-1] is selectedDie:
                    self.removeChangingShapes(shapesList)
                    return
                
        if not selectedDice:
            return
        
        self.addChangingShapes(selectedDie)


class Shape:
    def __init__(self, x, y, speed, size, WIDTH, HEIGHT, colorRange = 100):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.xy = [x, y]
        self.incr = speed
        self.size = size
        self.color = randomColor(colorRange)
        self.setFullColor(colorRange)
        self.sides = random.randint(3, 8)
        self.relative_points = self.generateRelativePoints()
        self.xBack = random.choice([True, False])
        self.yBack = random.choice([True, False])

    def setFullColor(self, colorRange):
        self.transitionProgress = 0.0
        self.colorRange = colorRange
        self.targetColor = self.color
        self.setTargetColor(randomColor(self.colorRange))

    def draw(self, screen):
        points = [(self.xy[0] + px, self.xy[1] + py) for px, py in self.relative_points]
        pg.draw.polygon(screen, self.color, points)
        
    def generateRelativePoints(self):
        points = []
        angle = 360 / self.sides
        for i in range(self.sides):
            theta = (angle * i) * (math.pi / 180)
            r = random.randint(20, self.size)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        return points

    def updatePosition(self):
        new_x = self.xy[0] - self.incr if self.xBack else self.xy[0] + self.incr
        new_y = self.xy[1] - self.incr if self.yBack else self.xy[1] + self.incr

        new_points = [(new_x + px, new_y + py) for px, py in self.relative_points]

        x_out_of_bounds = any(px < 0 or px > self.WIDTH for px, _ in new_points)
        y_out_of_bounds = any(py < 0 or py > self.HEIGHT for _, py in new_points)

        if not x_out_of_bounds:
            self.xy[0] = new_x
        if not y_out_of_bounds:
            self.xy[1] = new_y

        if x_out_of_bounds:
            self.xBack = not self.xBack
        if y_out_of_bounds:
            self.yBack = not self.yBack

        # if x_out_of_bounds or y_out_of_bounds:
        #     self.setFullColor(self.colorRange)
    
    def setTargetColor(self, targetColor):
        #should avoid redundant assignments
        if self.targetColor != targetColor:
            self.targetColor = targetColor
            self.transitionProgress = 0.0  # Reset transition progress

    def updateColor(self, transIncr = .001):
        if self.transitionProgress <= 1.0:
            self.transitionProgress += transIncr # Adjust the speed of transition here
            r = int(self.color.r + (self.targetColor.r - self.color.r) * self.transitionProgress)
            g = int(self.color.g + (self.targetColor.g - self.color.g) * self.transitionProgress)
            b = int(self.color.b + (self.targetColor.b - self.color.b) * self.transitionProgress)
            self.color = pg.Color(r, g, b)

def randomColor(midRange):
    # Maintain the range for visual feedback while ensuring consistent transition speed
    num = random.randint(midRange - 5, midRange + 5)
    return pg.Color(num, num, num)