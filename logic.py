from collections import Counter
from enum import Enum
import math

class DiceHand(Enum):
    NO_HAND         = ["No Hand",        0]
    HIGH_DIE        = ["High Die",       1]
    ONE_PAIR        = ["One Pair",       1]
    TWO_PAIR        = ["Two Pair",       1.5]
    THREE_OF_A_KIND = ["Three of a Kind",2]
    STRAIGHT_SMALL  = ["Small Straight", 5]
    STRAIGHT_LARGE  = ["Large Straight", 5.5]
    FULL_HOUSE      = ["Full House",     5]
    FOUR_OF_A_KIND  = ["Four of a Kind", 5]
    FIVE_OF_A_KIND  = ["Five of a Kind", 7.5]
    #weird hands
    SNAKE_EYES      = ["Snake Eyes",     2]
    #6 dice
    THREE_PAIR      = ["Three Pair",   7.5]
    SIX_OF_A_KIND   = ["Six of a Kind", 10]
    STRAIGHT_LARGER = ["Larger Straight", 12.5] #6 range 
    TWO_THREE_OF_A_KIND= ["Three's a Crowd", 12.5]
    #7 dice
    STRAIGHT_LARGEST= ["Ultra Straight", 15] #7 range
    FULLER_HOUSE   = ["Fullest House", 12.5]
    SEVEN_OF_A_KIND   = ["Seven????", 15]

class LogicService:
    STARTING_ROLLS = 2
    STARTING_HANDS = 3

    interestThreshold = 5
    interestMaxPerLevel = 5
    stageClearBonus = 4

    goldPipsThisLevel = 0

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

    def calculateGold(self, playerGold):
        interest = playerGold // self.interestThreshold
        if interest > self.interestMaxPerLevel:
            interest = self.interestMaxPerLevel
        stageClearBonus = self.stageClearBonus
        if self.isNextLevel():
            # print(self.goldPipsThisLevel)
            return interest, stageClearBonus, self.goldPipsThisLevel
        return 0

    def subtractHealth(self, num):
        self.rockHealth -= num
        self.DrawService.NUM_SHAPES -= num
        if self.rockHealth <= 0:
            self.rockHealth = 0
            self.DrawService.NUM_SHAPES = 0
            return 
        return 0
    
    def updateGoldPips(self):
        for die in self.scoringHandDice:
            for pip in die.curSide.getPips():
                if pip.isGOLDMod():
                    self.goldPipsThisLevel += 1
                    if die.curSide.hasGOLDMod():
                        self.goldPipsThisLevel += 1
    
    def selectedScoreTotal(self, handMult = True):
        total = 0
        for die in self.scoringHandDice:
            adding = die.calculate()
            total += int(adding)#truncate decimal
        if handMult:
            total *= self.hand.value[1]
        return int(math.ceil(total))
    
    def stopScoring(self, SoundService):
        self.isScoring = False
        for die in self.getSelectedDice():
            die.select()
            die.rollDie()
        self.DrawService.allRecentHands.append(f"{self.recentHandScoreNum} : {self.hand.value[0]}")
        SoundService.diceRollSound(rollsLeft=1)
        self.subtractHealth(self.recentHandScoreNum)


    def score(self):
        self.startScoring()

    #returns False if no hand, returns hand num otherwise
    def startScoring(self):
        if self.rockHealth > 0 and self.scoringHandDice:
            if self.handsLeft > 0:
                self.isScoring = True

                self.handsLeft -= 1
                self.recentHandScoreNum = self.selectedScoreTotal()
                self.resetRolls()
                return self.recentHandScoreNum
        return False
    
    def startLevel(self, STARTING_ROCKS):
        self.DrawService.allRecentHands = []
        self.resetRolls()
        self.resetHands()
        self.unselectAll()
        self.rollDice()
        self.resetRolls()
        self.rockHealth = STARTING_ROCKS
        self.DrawService.resetRocks(self.rockHealth)
        self.goldPipsThisLevel = 0

    def resetRolls(self):
        self.rollsLeft = self.STARTING_ROLLS
    def resetHands(self):
        self.handsLeft = self.STARTING_HANDS
        
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

    def isNextLevel(self):
        return not self.isScoring and self.rockHealth <= 0

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
        
        #Hand calculations. Figures out the hand and then sets scoringHandDice depending on the hand. Weighted by hand rank
        if not handDicePips:
            self.hand = DiceHand.NO_HAND
            self.scoringHandDice = []
        elif 7 in values:
            self.hand = DiceHand.SEVEN_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif is_straight(uniqueVals, 7):
            self.hand = DiceHand.STRAIGHT_LARGEST
            straight = is_straight(uniqueVals, 7)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in straight]
        elif 6 in values:
            self.hand = DiceHand.SIX_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif is_straight(uniqueVals, 6):
            self.hand = DiceHand.STRAIGHT_LARGER
            straight = is_straight(uniqueVals, 6)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in straight]
        elif values.count(3) == 2:
            self.hand = DiceHand.TWO_THREE_OF_A_KIND
            three_kinds = [k for k, v in count.items() if v == 3]
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in three_kinds]
        elif 4 in values and 3 in values:
            self.hand = DiceHand.FULLER_HOUSE
            four_kind = [k for k, v in count.items() if v == 4]
            three_kind = [k for k, v in count.items() if v == 3]
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in four_kind + three_kind]
        elif 5 in values:
            self.hand = DiceHand.FIVE_OF_A_KIND
            target_value = max(count, key=count.get)
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == target_value]
        elif values.count(2) == 3:
            self.hand = DiceHand.THREE_PAIR
            pairs = [k for k, v in count.items() if v == 2]
            self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() in pairs]
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
            pair = max(count, key=count.get)
            if pair == 1:  # Check if the pair is Snake Eyes
                self.hand = DiceHand.SNAKE_EYES
                self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == pair]
            else:
                self.hand = DiceHand.ONE_PAIR
                self.scoringHandDice = [die for die in self.getSelectedDice() if die.curSide.getNum() == pair]
        elif 1 in values:
            self.hand = DiceHand.HIGH_DIE
            self.scoringHandDice = [max(self.getSelectedDice(), key=lambda die: die.curSide.getNum())]