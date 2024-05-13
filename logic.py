import pygame as pg
from collections import Counter
from enum import Enum, auto

class DiceHand(Enum):
    NO_HAND = "No Hand"
    ONE_PAIR = "One Pair"
    TWO_PAIR = "Two Pair"
    THREE_OF_A_KIND = "Three of a Kind"
    STRAIGHT_SMALL = "Small Straight"
    STRAIGHT_LARGE = "Large Straight"
    FULL_HOUSE = "Full House"
    FOUR_OF_A_KIND = "Four of a Kind"
    FIVE_OF_A_KIND = "Five of a Kind"
    HIGH_DIE = "High Die"

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
        
        

        

        

        
        

        