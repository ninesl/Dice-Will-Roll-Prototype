import random
import pygame as pg

class AnimateService:
    def __init__(self, DrawService):
        self.DrawService = DrawService

    def shakeDice(self, playerDice):
        oldDiceX = self.DrawService.diceX
        oldDiceY = self.DrawService.diceY

        shake_duration = 20  # Total shakes
        max_shake_range = 15  # Max pixels to shake

        # Redraw the dice at new position
        # self.DrawService.drawDice(dieToKeep)

        # self.DrawService.diceY += int(self.DrawService.dieSide * 1.5)

        y = self.DrawService.diceY
        for _ in range(shake_duration):
            x = self.DrawService.diceX
            for die in playerDice:
                if not die.isSelected:
                    die.rollDie()
                    pixelShakeX = random.randint(-max_shake_range, max_shake_range)
                    pixelShakeY = random.randint(-max_shake_range, max_shake_range)
                    # Temporarily update dice positions
                    x += pixelShakeX
                    y += pixelShakeY
                    # Redraw the die at new position
                    self.DrawService.drawDie(die, x, y)
                    # Reset dice positions
                    x -= pixelShakeX
                    y -= pixelShakeY

                x += self.DrawService.dieSpacing
            
            pg.display.update()
                    
        # Ensure dice positions are reset after shaking
        self.DrawService.diceX = oldDiceX
        self.DrawService.diceY = oldDiceY