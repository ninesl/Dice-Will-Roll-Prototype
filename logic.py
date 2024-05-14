import pygame as pg
from collections import Counter
from enum import Enum

class DiceHand(Enum):
    NO_HAND = ["No Hand", 0]
    ONE_PAIR = ["One Pair", 1]
    TWO_PAIR = ["Two Pair", 2]
    THREE_OF_A_KIND = ["Three of a Kind", 3]
    STRAIGHT_SMALL = ["Small Straight", 4]
    STRAIGHT_LARGE = ["Large Straight", 5]
    FULL_HOUSE = ["Full House", 6]
    FOUR_OF_A_KIND = ["Four of a Kind", 7]
    FIVE_OF_A_KIND = ["Five of a Kind", 8]
    HIGH_DIE = ["High Die", 1]

class LogicService:
    def __init__(self):
        self.total = 0
        self.hand = DiceHand.NO_HAND

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
        
        handDicePips = [die.curSide.getNum() for die in playerDice if die.isSelected]

        count = Counter(handDicePips)
        values = list(count.values())
        uniqueVals = sorted(set(handDicePips))
        
        # Define a helper to check for straights
        def is_straight(uniqueVals, length):
            return any(all(x in uniqueVals for x in range(start, start + length)) for start in range(min(uniqueVals), max(uniqueVals) - length + 2))
        
        if not handDicePips:
            self.hand = DiceHand.NO_HAND
        elif 5 in values:
            self.hand = DiceHand.FIVE_OF_A_KIND
        elif 4 in values:
            self.hand = DiceHand.FOUR_OF_A_KIND
        elif 3 in values and 2 in values:
            self.hand = DiceHand.FULL_HOUSE
        elif is_straight(uniqueVals, 5):
            self.hand = DiceHand.STRAIGHT_LARGE
        elif is_straight(uniqueVals, 4):
            self.hand = DiceHand.STRAIGHT_SMALL
        elif 3 in values:
            self.hand = DiceHand.THREE_OF_A_KIND
        elif values.count(2) == 2:
            self.hand = DiceHand.TWO_PAIR
        elif 2 in values:
            self.hand = DiceHand.ONE_PAIR
        elif 1 in values:
            self.hand = DiceHand.HIGH_DIE
        
        

        

        

        
        

        