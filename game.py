import pygame as pg
import dice

d = dice.Die(6)

top = ["Die rolls",1,2,3,4,5,6]
results = ["Die rolls",0,0,0,0,0,0]

for i in range(100):
    results[d.rollDie()] += 1

print(top)
print(results)