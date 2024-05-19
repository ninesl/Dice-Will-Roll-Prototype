import pygame as pg
import gamecontroller
from enum import Enum

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)


clock = pg.time.Clock()
monitor = pg.display.Info()

WIDTH =  int(monitor.current_w * 3 / 4)
HEIGHT = int(monitor.current_h * 3 / 4)

gc = gamecontroller.GameController(monitor)

# class Controls(Enum):
#     ROLL  = gc.rollDice,
#     SELECT= gc.selectDie,
#     QUIT  = gc.quitGame,
#     SCORE = gc.scoreDice,
#     RESET = gc.resetLevel,
#     HARDER= gc.harderLevel

keyBinds = {
    pg.K_SPACE: "roll",
    1: "select",
    pg.K_ESCAPE: "quit",
    pg.K_q: "score",
    pg.K_p: "reset",
    pg.K_o: "harder"
}

controls = {
    "roll"  :gc.rollDice,
    "select":gc.selectDie,
    "quit"  :gc.quitGame,
    "score" :gc.scoreDice,
    "reset" :gc.resetLevel,
    "harder":gc.harderLevel
}

print("loading", end = ".")
while not gc.isFinishedLoading():
    print(".", end = "")
print("done")
print()

print(" ⚀ ⚁ ⚂ ⚃ ⚄ ⚅")
print("⚀⚁⚂ DWARF ⚃⚄⚅")
print("⚀⚁⚂  DICE ⚃⚄⚅")
print(" ⚀ ⚁ ⚂ ⚃ ⚄ ⚅")

def replaceKeyBind(oldKey, newKey):
    # print(chr(oldKey))
    # print(chr(newKey))
    global keyBinds
    if oldKey in keyBinds:
        action = keyBinds.pop(oldKey)
        keyBinds[newKey] = action
    
# Example of updating key bindings
# Change roll action from space key to 'r' key
# replaceKeyBind(pg.K_SPACE, pg.K_r)

# fpsCount = 1
while gc.GOING:
    for event in pg.event.get():
        try:
            if event.type == pg.QUIT:
                gc.quitGame()
            elif event.type == pg.VIDEORESIZE:
                gc.resizeScreen(event.w, event.h)

            if event.type == pg.MOUSEBUTTONDOWN:
                controls[keyBinds[event.button]]()

            if event.type == pg.KEYDOWN:
                controls[keyBinds[event.key]]()
        except KeyError:
            pass  # Explicitly doing nothing

    gc.levelLoop()

    fps = int(clock.get_fps())
    gc.DrawService.drawText(1, f"{fps} fps", gc.WIDTH/10 * 9.25 - gc.WIDTH/10 * .05, gc.HEIGHT/10 * .05)
    pg.display.update()
    clock.tick(60)
    
    # fpsCount += 1
    # if fpsCount >= 120:
    #     print(f"gc.LogicService.rockHealth : {gc.LogicService.rockHealth}")
    #     print(f"gc.DrawService.NUM_SHAPES  : {gc.DrawService.NUM_SHAPES}")
    #     fpsCount = 0