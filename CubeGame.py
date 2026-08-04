from tkinter import *
import random
import GameObjects

window = Tk()
canvasWidth = 1280
canvasHeight = 720
canvas = Canvas(window, width=canvasWidth, height=canvasHeight, bg="white" )
canvas.pack()

vel = GameObjects.Velocity(20, 91)
cube = GameObjects.Cube(size = 20, position = dict(x=500, y=100),velocity=vel)
border = GameObjects.Border(canvasWidth, canvasHeight)

def updateCanvas():
    canvas.delete("all")
    cube.position_update([border])
    cube.render(canvas)
    #print("render complete")
    window.after(100, updateCanvas)


updateCanvas()
mainloop()