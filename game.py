import pygame as pg
import random as rand
import gamecontroller

pg.init()
pg.display.set_caption("Dwarf Dice")
window_icon = pg.image.load("assets/pickaxe.png")
pg.display.set_icon(window_icon)


clock = pg.time.Clock()
monitor = pg.display.Info()

WIDTH =  int(monitor.current_w * 3 / 4)
HEIGHT = int(monitor.current_h * 3 / 4)

gc = gamecontroller.GameController(monitor)

going = True
#TODO FPS math?

print("⚀⚁⚂ DWARF ⚃⚄⚅")
print("⚀⚁⚂  DICE ⚃⚄⚅")

keyBinds = {
    
}

print("loading", end = "...")
while not gc.isFinishedLoading():
    print(".", end = "")

while going:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.VIDEORESIZE:
            gc.resizeScreen(event.w, event.h)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                gc.selectDie()

        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_SPACE:
                    gc.rollDice()
                case pg.K_q:
                    gc.scoreDice()
                case pg.K_ESCAPE:
                    going = False
                case pg.K_p:
                    gc.resetLevel()
                case pg.K_o:
                    gc.harderLevel()

    gc.levelLoop()

    fps = int(clock.get_fps())
    gc.DrawService.drawText(1, f"{fps} fps", WIDTH/10 * 9.25 - WIDTH/10 * .05, HEIGHT/10 * .05)
    pg.display.update()
    clock.tick(60)