import random

class AnimateService:
    def __init__(self, DrawService, clock):
        self.DrawService = DrawService
        self.clock = clock

    def shakeDice(self, playerDice):
        oldDiceX = self.DrawService.diceX
        oldDiceY = self.DrawService.diceY

        shake_duration = 10  # Total shakes
        max_shake_range = 15  # Max pixels to shake

        dieToShake = []
        dieToKeep = []
        for die in playerDice:
            if not die.isSelected:
                dieToShake.append(die)
            else:
                dieToKeep.append(die)
            

        # Redraw the dice at new position
        # self.DrawService.drawDice(dieToKeep)

        # self.DrawService.diceY += int(self.DrawService.dieSide * 1.5)


        for _ in range(shake_duration):
            for die in dieToShake:
                    die.rollDie()
                    pixelShakeX = random.randint(-max_shake_range, max_shake_range)
                    pixelShakeY = random.randint(-max_shake_range, max_shake_range)

                    # Temporarily update dice positions
                    self.DrawService.diceX += pixelShakeX
                    self.DrawService.diceY += pixelShakeY

                    # Redraw the dice at new position
                    self.DrawService.drawDice(dieToShake)
                    
                    # Reset dice positions
                    self.DrawService.diceX -= pixelShakeX
                    self.DrawService.diceY -= pixelShakeY
                    
        # Ensure dice positions are reset after shaking
        self.DrawService.diceX = oldDiceX
        self.DrawService.diceY = oldDiceY