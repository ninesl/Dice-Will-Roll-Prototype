from collections import Counter
from enum import Enum
import math

class DiceHand(Enum):
    NO_HAND         = ["No Hand",        0]
    HIGH_DIE        = ["High Die",       1]
    ONE_PAIR        = ["One Pair",       1]
    TWO_PAIR        = ["Two Pair",       3]#bc you start with 1
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
    CROWDED_HOUSE   = ["Crowded House", 10]
    SIX_OF_A_KIND   = ["Six of a Kind", 10]
    STRAIGHT_LARGER = ["Larger Straight", 10] #6 range 
    TWO_THREE_OF_A_KIND= ["Threes a Crowd", 10]
    #7 dice
    OVERPOPULATED_HOUSE= ["Overpopulated House", 10]
    STRAIGHT_LARGEST= ["Ultra Straight", 15] #7 range
    FULLER_HOUSE   = ["Fullest House", 10]
    SEVEN_OF_A_KIND   = ["Seven of a Kind", 15]
    #ultimate deck. have to spend $$$ to make it real
    SEVEN_SEVENS = ["Lucky Sevens", 77]

class LogicService:
    handsRevealed = {
        DiceHand.NO_HAND.value[0] : DiceHand.NO_HAND.value[1]
    }

    STARTING_ROLLS = 2
    STARTING_HANDS = 3

    REVEAL_HAND_WHEN_SCORING = True
    
    interestThreshold = 5
    interestMaxPerLevel = 5
    stageClearBonus = 4

    handsThisRun = 0
    rollsThisRun = 0

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

    def isAllPlayerDiceSelected(self):
        for die in self.playerDice:
            if not die.isSelected:
                return False
        return True

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
    
    #Could be a powerup/idol
    def selectedScoreTotal(self, handMult = True, gameOverCalculation = None):
        total = 0
        if gameOverCalculation:
            self.selectAll()
            # self.findHand(otherDice=self.playerDice, returningBestDice=True)
            self.findHand()
             #for best hand

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

        self.handsThisRun += 1

        self.subtractHealth(self.recentHandScoreNum)

    def score(self):
        if self.REVEAL_HAND_WHEN_SCORING == False:
            self.handsRevealed[self.hand[0]] = self.hand[1]
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
        #glitch idol idea. Don't roll dice and the playerdice will be set the right most die face on the shop screen
        self.rollAllDice()
        ####################################
        #self.rollDice() #glitch idol
        #self.resetRolls()
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
    
    def rollDice(self, rollClickMode = None):
        # print(rollClickMode)
        rollsSubtracted = False #hacky
        if self.rollsLeft > 0:
            for die in self.playerDice:
                if die.isSelected and rollClickMode == "Select":
                    die.rollDie()
                if not die.isSelected and rollClickMode == "Hold":
                    die.rollDie()
            
                if die.isSelected and rollClickMode == "Select" and not rollsSubtracted:
                    print("select roll")
                    self.rollsThisRun += 1
                    self.rollsLeft -= 1
                    rollsSubtracted = True
                if not die.isSelected and rollClickMode == "Hold" and not rollsSubtracted:
                    print("hold roll")
                    self.rollsThisRun += 1
                    self.rollsLeft -= 1
                    rollsSubtracted = True
                    

    # def endRolls(self):
    #     score        
    def rollAllDice(self):
        if self.rollsLeft > 0:
            for die in self.playerDice:
                die.rollDie()

    def getSelectedDice(self):
        return [die for die in self.playerDice if die.isSelected]
    
    def getUnselectedDice(self):
        return [die for die in self.playerDice if not die.isSelected]
    
    def unselectAll(self):
        for die in self.getSelectedDice():
            die.select()

    def selectAll(self):
        for die in self.playerDice:
            if not die.isSelected:
                die.select()

    def isNextLevel(self):
        return not self.isScoring and self.rockHealth <= 0

    def findHand(self, otherDice = None, returningBestDice = False):
        findingDice = self.getSelectedDice()
        if otherDice:
            findingDice = otherDice
        handDicePips = [die.curSide.getNum() for die in findingDice]

        count = Counter(handDicePips)
        values = list(count.values())
        uniqueVals = sorted(set(handDicePips))
        
        # helper that checks for straights
        #Hand calculations. Figures out the hand and then sets scoringHandDice depending on the hand. Weighted by hand rank
        def is_straight(uniqueVals, length):
            for start in range(min(uniqueVals), max(uniqueVals) - length + 2):
                if all(x in uniqueVals for x in range(start, start + length)):
                    return range(start, start + length)
            return None

        if not handDicePips:
            self.hand = DiceHand.NO_HAND
            findingDice = []
        elif 7 in values:
            seven = max(count, key=count.get)
            if seven == 7:  # Check if the pair is 7s
                self.hand = DiceHand.SEVEN_SEVENS
                findingDice = [die for die in findingDice if die.curSide.getNum() == seven]
            else:
                self.hand = DiceHand.SEVEN_OF_A_KIND
                findingDice = [die for die in findingDice if die.curSide.getNum() == seven]
        elif is_straight(uniqueVals, 7):
            self.hand = DiceHand.STRAIGHT_LARGEST
            straight = is_straight(uniqueVals, 7)
            findingDice = [die for die in     findingDice if die.curSide.getNum() in straight]
        elif 6 in values:
            self.hand = DiceHand.SIX_OF_A_KIND
            target_value = max(count, key=count.get)
            findingDice = [die for die in     findingDice if die.curSide.getNum() == target_value]
        elif is_straight(uniqueVals, 6):
            self.hand = DiceHand.STRAIGHT_LARGER
            straight = is_straight(uniqueVals, 6)
            findingDice = [die for die in     findingDice if die.curSide.getNum() in straight]
        elif 5 in values and 2 in values:
            self.hand = DiceHand.OVERPOPULATED_HOUSE
            five_kind = [k for k, v in count.items() if v == 5]
            pair = [k for k, v in count.items() if v == 2]
            findingDice = [die for die in findingDice if die.curSide.getNum() in five_kind + pair]
        elif values.count(3) == 2:
            self.hand = DiceHand.TWO_THREE_OF_A_KIND
            three_kinds = [k for k, v in count.items() if v == 3]
            findingDice = [die for die in findingDice if die.curSide.getNum() in three_kinds]
        elif 4 in values and 3 in values:
            self.hand = DiceHand.FULLER_HOUSE
            four_kind = [k for k, v in count.items() if v == 4]
            three_kind = [k for k, v in count.items() if v == 3]
            findingDice = [die for die in findingDice if die.curSide.getNum() in four_kind + three_kind]
        elif 5 in values:
            self.hand = DiceHand.FIVE_OF_A_KIND
            target_value = max(count, key=count.get)
            findingDice = [die for die in findingDice if die.curSide.getNum() == target_value]
        elif values.count(2) == 3:
            self.hand = DiceHand.THREE_PAIR
            pairs = [k for k, v in count.items() if v == 2]
            findingDice = [die for die in findingDice if die.curSide.getNum() in pairs]
        elif 4 in values:
            if values.count(2) == 1:
                self.hand = DiceHand.CROWDED_HOUSE  # Added this block
                four_kind = [k for k, v in count.items() if v == 4]
                pair = [k for k, v in count.items() if v == 2]
                findingDice = [die for die in findingDice if die.curSide.getNum() in four_kind + pair]
            else:
                self.hand = DiceHand.FOUR_OF_A_KIND
                target_value = max(count, key=count.get)
                findingDice = [die for die in findingDice if die.curSide.getNum() == target_value]
        elif 3 in values and 2 in values:
            self.hand = DiceHand.FULL_HOUSE
            three_kind = [k for k, v in count.items() if v == 3]
            two_kind = [k for k, v in count.items() if v == 2]
            findingDice = [die for die in findingDice if die.curSide.getNum() in three_kind + two_kind]
        elif is_straight(uniqueVals, 5):
            self.hand = DiceHand.STRAIGHT_LARGE
            straight = is_straight(uniqueVals, 5)
            findingDice = [die for die in findingDice if die.curSide.getNum() in straight]
        elif is_straight(uniqueVals, 4):
            self.hand = DiceHand.STRAIGHT_SMALL
            straight = is_straight(uniqueVals, 4)
            findingDice = [die for die in findingDice if die.curSide.getNum() in straight]
        elif 3 in values:
            self.hand = DiceHand.THREE_OF_A_KIND
            target_value = max(count, key=count.get)
            findingDice = [die for die in findingDice if die.curSide.getNum() == target_value]
        elif values.count(2) == 2:
            self.hand = DiceHand.TWO_PAIR
            pairs = [k for k, v in count.items() if v == 2]
            findingDice = [die for die in findingDice if die.curSide.getNum() in pairs]
        elif 2 in values:
            pair = max(count, key=count.get)
            if pair == 1:  # Check if the pair is Snake Eyes
                self.hand = DiceHand.SNAKE_EYES
                findingDice = [die for die in findingDice if die.curSide.getNum() == pair]
            else:
                self.hand = DiceHand.ONE_PAIR
                findingDice = [die for die in findingDice if die.curSide.getNum() == pair]
        else:
            self.hand = DiceHand.HIGH_DIE
            findingDice = [max(findingDice, key=lambda die: die.curSide.getNum())]
            
        if not otherDice:
            self.scoringHandDice = []
            self.scoringHandDice = findingDice
            #just if you select them.
            if self.REVEAL_HAND_WHEN_SCORING == False:
                self.handsRevealed[self.hand[0]] = self.hand[1]

        if returningBestDice:
            return self.scoringHandDice

        return self.hand.value
