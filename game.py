import pygame as pg
import gamecontroller
from enum import Enum

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)


clock = pg.time.Clock()
monitor = pg.display.Info()
fps = 60

# WIDTH =  int(monitor.current_w * 3 / 4)
# HEIGHT = int(monitor.current_h * 3 / 4)

# WIDTH = 1600
# HEIGHT = 900

gc = gamecontroller.GameController(monitor, clock, fps)

# class Controls(Enum):
#     ROLL  = gc.rollDice,
#     SELECT= gc.selectDie,
#     QUIT  = gc.quitGame,
#     SCORE = gc.scoreDice,
#     RESET = gc.resetLevel,
#     HARDER= gc.harderLevel



print("loading", end = ".")
while not gc.isFinishedLoading():
    print(".", end = "")
print("done")
print()

print(" ⚀ ⚁ ⚂ ⚃ ⚄ ⚅")
print("⚀⚁⚂ DWARF ⚃⚄⚅")
print("⚀⚁⚂  DICE ⚃⚄⚅")
print(" ⚀ ⚁ ⚂ ⚃ ⚄ ⚅")

# def replaceKeyBind(oldKey, newKey):
#     # print(chr(oldKey))
#     # print(chr(newKey))
#     global keyBinds
#     if oldKey in keyBinds:
#         action = keyBinds.pop(oldKey)
#         keyBinds[newKey] = action
    
# # Example of updating key bindings
# # Change roll action from space key to 'r' key
# # replaceKeyBind(pg.K_SPACE, pg.K_r)

keyBinds = {
    "level" : {
        pg.K_SPACE: "roll",
        1: "hold",
        pg.K_ESCAPE: "quit",
        pg.K_q: "score",
        pg.K_p: "reset",
        pg.K_o: "harder",
        pg.K_w: "shop",
        pg.K_r: "newdie"
    },
    "shop" : {
        pg.K_ESCAPE: "quit",
        1: "hold",
        pg.K_e: "level",
        pg.K_r: "newdie"
    }
}

#everything
controls = {
    "roll"  :gc.rollDice,
    "hold"  :gc.selectDie,
    "quit"  :gc.quitGame,
    "score" :gc.scoreDice,
    "reset" :gc.resetLevel,
    "harder":gc.harderLevel,
    "shop"  :gc.goToShop,
    "level" :gc.goToLevel,
    "newdie":gc.newDice
}

GAME_STATE = "level"
currentAction = ""
# fpsCount = 1
while gc.GOING:

    for event in pg.event.get():
        try:
            if event.type == pg.QUIT:
                gc.quitGame()
            #TODO resize while scoring
            # if event.type == pg.VIDEORESIZE:
            #     gc.resizeScreen(event.w, event.h)
                
            if not gc.LogicService.isScoring:
                if event.type == pg.MOUSEBUTTONDOWN:
                    currentAction = keyBinds[GAME_STATE][event.button]
                    controls[currentAction]()

                if event.type == pg.KEYDOWN:
                    currentAction = keyBinds[GAME_STATE][event.key]
                    controls[currentAction]()

                if currentAction in keyBinds:
                    GAME_STATE = currentAction
        except KeyError:
            pass  # Explicitly doing nothing
    gc.gameLoop()


    fps = int(clock.get_fps())
    gc.DrawService.drawText(1, f"{fps} fps", gc.WIDTH/10 * 9.25 - gc.WIDTH/10 * .05, gc.HEIGHT/10 * .05)
    pg.display.update()
    clock.tick(60)
    # clock.tick_busy_loop(fps)
    
    # fpsCount += 1
    # if fpsCount >= 120:
    #     print(f"gc.LogicService.rockHealth : {gc.LogicService.rockHealth}")
    #     print(f"gc.DrawService.NUM_SHAPES  : {gc.DrawService.NUM_SHAPES}")
    #     fpsCount = 0