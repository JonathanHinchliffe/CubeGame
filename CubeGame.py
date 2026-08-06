from tkinter import *
import random
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
colours = ["red", "blue", "green", "yellow", "pink", "brown", "grey"]
i = 0
objects = [border]
cubes = []
for i in range(30):
    vel = GameObjects.Velocity(angle=random.randint(0,359), speed=random.randint(5,30))
    cubes.append(GameObjects.Cube(size=random.randint(10,40), position=dict(x=random.randint(100,canvasWidth),y=random.randint(50,canvasHeight)), velocity=vel, colour=colours[i%len(colours)]))
    objects.append(cubes[i])

def updateCanvas():
    start = time.time()
    canvas.delete("all")
    for cube in cubes:
        cube.render(canvas)
        cube.frame_update(objects = objects)
    #print("render complete")
    end = time.time()
    times.append(end-start)
    print(sum(times)/len(times))
    window.after(100, updateCanvas)


updateCanvas()
mainloop()