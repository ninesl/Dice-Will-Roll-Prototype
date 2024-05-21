from collections import Counter
from enum import Enum
import math

class DiceHand(Enum):
    NO_HAND         = ["No Hand",        0]
    HIGH_DIE        = ["High Die",       1]
    ONE_PAIR        = ["One Pair",       1]
    TWO_PAIR        = ["Two Pair",       1.5]
    THREE_OF_A_KIND = ["Three of a Kind",2]
    STRAIGHT_SMALL  = ["Small Straight", 3]
    STRAIGHT_LARGE  = ["Large Straight", 3.5]
    FULL_HOUSE      = ["Full House",     5]
    FOUR_OF_A_KIND  = ["Four of a Kind", 10]
    FIVE_OF_A_KIND  = ["Five of a Kind", 15]

class LogicService:
    STARTING_ROLLS = 3
    STARTING_HANDS = 5

    def __init__(self, playerDice, DrawService):
        self.DrawService = DrawService
        self.rockHealth = DrawService.NUM_SHAPES

        self.hand = DiceHand.NO_HAND
        self.playerDice = playerDice

        self.isScoring = False
        self.scoringHandDice = []
        self.recentHandScoreNum = 0

        self.rollsLeft = self.STARTING_ROLLS
        self.handsLeft = self.STARTING_HANDS

    def subtractHealth(self, num):
        self.rockHealth -= num
        self.DrawService.NUM_SHAPES -= num
        if self.rockHealth <= 0:
            self.rockHealth = 0
            self.DrawService.NUM_SHAPES = 0
    
    def selectedScoreTotal(self, handMult = True):
        total = 0
        for die in self.scoringHandDice:
            total += die.calculate()
        if handMult:
            total *= self.hand.value[1]
        return math.ceil(total)
    
    def stopScoring(self, SoundService):
        self.isScoring = False
        for die in self.getSelectedDice():
            die.select()
            die.rollDie()
        self.DrawService.allHands.append(f"{self.recentHandScoreNum} : {self.hand.value[0]}")
        SoundService.diceRollSound(1)

    #returns False if no hand, returns hand num otherwise
    def score(self):
        if self.rockHealth > 0 and self.scoringHandDice:
            if self.handsLeft > 0:
                self.isScoring = True

                self.handsLeft -= 1
                self.recentHandScoreNum = self.selectedScoreTotal()
                self.subtractHealth(self.recentHandScoreNum)
                self.rollsLeft = self.STARTING_ROLLS
                return self.recentHandScoreNum
        return False
        
    def addDice(self):
        self.total = 0
        for die in self.playerDice:
            if die.isSelected:
                self.total += die.num
    
    def rollDice(self):
        if self.rollsLeft > 0:
            for die in self.playerDice:
                if not die.isSelected:
                    die.rollDie()
            self.rollsLeft -= 1

    def getSelectedDice(self):
        return [die for die in self.playerDice if die.isSelected]
    
    def unselectAll(self):
        for die in self.getSelectedDice():
            die.select()

    def findHand(self):
        handDicePips = [die.curSide.getNum() for die in self.getSelectedDice() if die.isSelected]

        count = Counter(handDicePips)
        values = list(count.values())
        uniqueVals = sorted(set(handDicePips))
        
        # helper that checks for straights
        def is_straight(uniqueVals, length):
            for start in range(min(uniqueVals), max(uniqueVals) - length + 2):
                if all(x in uniqueVals for x in range(start, start + length)):
                    return range(start, start + length)
            return None
        
        #Hand calculations. Figures out the hand and then sets scoringHandDice depending on the hand
        if not handDicePips:
            self.hand = DiceHand.NO_HAND
            self.scoringHandDice = []
        elif 5 in values:
            self.hand = DiceHand.FIVE_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif 4 in values:
            self.hand = DiceHand.FOUR_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif 3 in values and 2 in values:
            self.hand = DiceHand.FULL_HOUSE
            three_kind = [k for k, v in count.items() if v == 3]
            two_kind = [k for k, v in count.items() if v == 2]
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in three_kind + two_kind]
        elif is_straight(uniqueVals, 5):
            self.hand = DiceHand.STRAIGHT_LARGE
            straight = is_straight(uniqueVals, 5)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in straight]
        elif is_straight(uniqueVals, 4):
            self.hand = DiceHand.STRAIGHT_SMALL
            straight = is_straight(uniqueVals, 4)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in straight]
        elif 3 in values:
            self.hand = DiceHand.THREE_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif values.count(2) == 2:
            self.hand = DiceHand.TWO_PAIR
            pairs = [k for k, v in count.items() if v == 2]
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in pairs]
        elif 2 in values:
            self.hand = DiceHand.ONE_PAIR
            pair = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == pair]
        elif 1 in values:
            self.hand = DiceHand.HIGH_DIE
            self.scoringHandDice = [max(self.getSelectedDice(), key=lambda die: die.curSide.getNum())]