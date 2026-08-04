from tkinter import *
import random
import GameObjects

window = Tk()
canvasWidth = 1280
canvasHeight = 720
canvas = Canvas(window, width=canvasWidth, height=canvasHeight, bg="white" )
canvas.pack()

vel = GameObjects.Velocity(20, 45)
cube = GameObjects.Cube(size = 20, position = dict(x=0, y=0),velocity=vel)

def updateCanvas():
    canvas.delete("all")
    cube.position_update()
    cube.render(canvas)
    print("render complete")
    window.after(100, updateCanvas)


updateCanvas()
mainloop()