from collections import Counter
from enum import Enum

class DiceHand(Enum):
    NO_HAND         = ["No Hand",        0]
    HIGH_DIE        = ["High Die",       1]
    ONE_PAIR        = ["One Pair",       1]
    TWO_PAIR        = ["Two Pair",       1]
    THREE_OF_A_KIND = ["Three of a Kind",2]
    STRAIGHT_SMALL  = ["Small Straight", 3]
    STRAIGHT_LARGE  = ["Large Straight", 3]
    FULL_HOUSE      = ["Full House",     5]
    FOUR_OF_A_KIND  = ["Four of a Kind", 10]
    FIVE_OF_A_KIND  = ["Five of a Kind", 15]

class LogicService:
    def __init__(self, playerDice, DrawService):
        self.DrawService = DrawService
        self.rockHealth = DrawService.NUM_SHAPES
        self.hand = DiceHand.NO_HAND
        self.playerDice = playerDice


    #TODO SUBTRACTING WHOLE TOTAL, NOT NUM ******
    def subtractHealth(self, num):
        self.rockHealth -= num
        self.DrawService.NUM_SHAPES -= num
        if self.rockHealth <= 0:
            self.rockHealth = 0
            self.DrawService.NUM_SHAPES = 0

    def selectedTotal(self):
        scoreDice = self.getSelectedDice()
        total = 0
        for die in scoreDice:
            total += die.calculate()
        return total

    def score(self):
        if self.rockHealth > 0:
            scoredHandNum = self.selectedTotal() * self.hand.value[1]
            self.subtractHealth(scoredHandNum)

            for die in self.getSelectedDice():
                die.select()
                die.rollDie()

            self.DrawService.deleteRocks(scoredHandNum)
            return scoredHandNum
        else:
            return 0
        
    def addDice(self):
        self.total = 0
        for die in self.playerDice:
            if die.isSelected:
                self.total += die.num
    
    def rollDice(self):
        for die in self.playerDice:
            if not die.isSelected:
                die.rollDie()

    def getSelectedDice(self):
        return [die for die in self.playerDice if die.isSelected]
    
    def unselectAll(self):
        for die in self.getSelectedDice():
            die.select()

    def findHand(self):
        # handDicePips = []
        # for die in playerDice:
        #     if die.isSelected:
        #         handDicePips.append(die.curSide.getPips())
        
        handDicePips = [die.curSide.getNum() for die in self.playerDice if die.isSelected]

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
        
        

        

        

        
        

        