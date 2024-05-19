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
    
    def calculate(self):
        return self.curSide.getCalculate()

class Side:
    def __init__(self, value, color):
        self.pips = []
        self.modEnum = None
        self.color = color
        for _ in range(value):
            self.pips.append(Pip())
    
    def getCalculate(self):
        score = 0
        for pip in self.pips:
            match pip.gem:
                case Mod.ATK:
                    score += 2
                # case Mod.DEF:
                #     break
                # case Mod.GOLD:
                #     break
                case Mod.BASE:
                    score += 1
        return score
    
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
        match random.randint(0,2):
            case 0:
                self.gem = Mod.BASE
            case 1:
                self.gem = Mod.ATK
            # case 2:
            #     self.gem = Mod.DEF
            # case 3:
            #     self.gem = Mod.GOLD


    def getPipColor(self):
        return self.gem.value

class Mod(Enum):
    ATK = pg.Color(255,0,0,230)
    # DEF = pg.Color(0,100,255,230)
    # GOLD = pg.Color(255,215,0,230)
    BASE = pg.Color(0,0,0,230)
    # ATK  = pg.Color(0,0,0,230)

    # DEF  = pg.Color(0,0,0,230)
    # GOLD = pg.Color(0,0,0,230)