import pygame as pg
from collections import Counter

class LogicService:
    def __init__(self):
        self.total = 0
        self.hand = "No Hand"

    def addDice(self, playerDice):
        self.total = 0
        for die in playerDice:
            if die.isSelected:
                self.total += die.num
    
    def rollDice(self, playerDice):
        self.total = 0
        for die in playerDice:
            if die.isSelected:
                self.total += die.num
            else:
                die.rollDie()

    def findHand(self, playerDice):
        # handDicePips = []
        # for die in playerDice:
        #     if die.isSelected:
        #         handDicePips.append(die.curSide.getPips())
        
        handDicePips = [die.curSide.getPips() for die in playerDice if die.isSelected]

        count = Counter(handDicePips)
        values = list(count.values())
        uniqueVals = sorted(set(handDicePips))
        
        # Define a helper to check for straights
        def is_straight(uniqueVals, length):
            return any(all(x in uniqueVals for x in range(start, start + length)) for start in range(min(uniqueVals), max(uniqueVals) - length + 2))
        
        if not handDicePips:
            self.hand = "No Hand"
            return
    
        else:
            if 5 in values:
                hand = "Five of a Kind"
            elif 4 in values:
                hand = "Four of a Kind"
            elif 3 in values and 2 in values:
                hand = "Full House"
            elif is_straight(uniqueVals, 5):
                hand = "Large Straight"
            elif is_straight(uniqueVals, 4):
                hand = "Small Straight"
            elif 3 in values:
                hand = "Three of a Kind"
            elif values.count(2) == 2:
                hand = "Two Pair"
            elif 2 in values:
                hand = "One Pair"
            elif 1 in values:
                hand = "High Die"

        self.hand = hand
        
        

        

        

        
        

        