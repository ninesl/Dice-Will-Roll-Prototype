# import enum
import random
import pygame as pg
from enum import Enum

class Die:
    def __init__(self, sides, color):
        self.isSelected = False
        self.num = -1
        self.isHovered = False

        self.sides = []
        for i in range(sides):
            self.sides.append( Side(i + 1, color) ) # create a side with i+1 pips
        self.curSide = self.sides[0]
    
    def getNumSides(self):
        return len(self.sides)
    
    def select(self):
        self.isSelected = not self.isSelected #invert selection flag

    #returns value of a calculated side
    def rollDie(self):
        iSide = self.rollSide()
        self.curSide = iSide

        self.num = iSide.getCalculate()
        return self.num

    # returns random side
    def rollSide(self):
        return self.sides[random.randint(0, self.getNumSides() - 1)]
    
    def getColor(self):
        if self.isHovered:
            self.curSide.color.a = 150 #slightly transparent
        else:
            self.curSide.color.a = 255 #set to opaque
        return self.curSide.color

class Side:
    def __init__(self, value, color):
        self.pips = []
        self.modEnum = None
        self.color = color
        for i in range(value):
            self.pips.append(Pip())
    
    def getCalculate(self):
        #todo pip calculations
        return len(self.pips)
    
    def getPips(self):
        #todo return pips for gem in DrawService graphics.py
        return self.pips
    
    def getNum(self):
        return len(self.pips)
    
    # USE Mod ATK,DEF,GOLD etc
    # def setModSide(self, modEnum):
    #     self.modEnum = modEnum
        
class Pip:
    def __init__(self):
        self.gem = Mod.BASE
    def getPipColor(self):
        return self.gem.value

class Mod(Enum):
    BASE = pg.Color(0,0,0,170)
    ATK = pg.Color(255,0,0,170)
    DEF = pg.Color(0,100,255,170)
    GOLD = pg.Color(255,215,0,170)