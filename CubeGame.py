from tkinter import *
import random
from turtle import pos
import GameObjects
import time

global times

times = []
window = Tk()
canvasWidth = 1280
canvasHeight = 720
canvas = Canvas(window, width=canvasWidth, height=canvasHeight, bg="white" )
canvas.pack()


border = GameObjects.Border(canvasWidth, canvasHeight)
#cubes = [cube1,cube2,cube3,cube4]
colours = ["red", "yellow", "pink", "brown", "grey"]
i = 0
objects = [border]
cubes = []
for i in range(30):
    vel = GameObjects.Velocity(angle=random.randint(0,359), speed=random.randint(5,30))
    cubes.append(GameObjects.Cube(size=random.randint(10,40), position=dict(x=random.randint(100,canvasWidth),y=random.randint(50,canvasHeight)), velocity=vel, colour=colours[i%len(colours)]))
    objects.append(cubes[i])

score = GameObjects.Score()
increase = GameObjects.Score_Increase(score)

player = GameObjects.Player(GameObjects.Cube(size=40, position=dict(x = canvasWidth/2, y = canvasHeight/2), colour="blue"))
power_up = GameObjects.Score_Increase_Powerup(score, effect_length=5000, position = dict(x = 200, y = 200))
objects.append(power_up)
cubes.append(power_up)
print(type(cubes[-1]))


def updateCanvas():
    canvas.delete("all")
    score.frame_update()
    print(score.score)
    for cube in cubes:
        if cube.remove:
            cubes.remove(cube)
            objects.remove(cube)
            #del cube
        else:
            cube.render(canvas)
            cube.frame_update(objects = objects)
    #print("render complete")
    player.render(canvas)
    #print(sum(times)/len(times))
    window.after(100, updateCanvas)


effects = (GameObjects.Score_Increase)
game = GameObjects.Game(canvas, effects=effects)

window.bind("<Motion>",lambda event, objects=objects: player.position_update(event=event,objects=objects))
updateCanvas()
mainloop()
