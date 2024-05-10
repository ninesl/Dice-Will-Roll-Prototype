# import enum
import random

class Die:
    def __init__(self, sides):
        self.sides = []
        for i in range(sides):
            self.sides.append( Side(i + 1) ) # create a side with i+1 dots
    
    def getNumSides(self):
        return len(self.sides)
    
    #returns value of a calculated side
    def rollDie(self):
        iSide = self.rollSide()
        num = iSide.getCalculate()
        return num

    # returns random side
    def rollSide(self):
        return self.sides[random.randint(0, self.getNumSides() - 1)]

class Side:
    def __init__(self, value):
        self.dots = []
        self.modEnum = None
        for i in range(value):
            self.dots.append(Dot())
    
    def getCalculate(self):
        #todo dot calculations
        return len(self.dots)
    
    # USE Mod ATK,DEF,GOLD etc
    # def setModSide(self, modEnum):
    #     self.modEnum = modEnum
        
class Dot:
    def __init__(self):
        self.gem = None
    # def __init__(self, dotMod):
    #     self.gem = dotMod

# class Mod(Enum):
#     ATK = enum.auto()
#     DEF = enum.auto()
#     GOLD = enum.auto()