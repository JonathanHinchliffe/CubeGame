from tkinter import *
import random
import GameObjects

window = Tk()
canvasWidth = 1280
canvasHeight = 720
canvas = Canvas(window, width=canvasWidth, height=canvasHeight, bg="white" )
canvas.pack()


#goes top right
vel1 = GameObjects.Velocity(10, 45)
cube1 = GameObjects.Cube(size = 20, position = dict(x=500, y=100),velocity=vel1)

#goes bottom right
vel2 = GameObjects.Velocity(10, 135)
cube2 = GameObjects.Cube(size = 20, position = dict(x=500, y=100),velocity=vel2, colour="blue")

#bottom left
vel3 = GameObjects.Velocity(10, 190)
cube3 = GameObjects.Cube(size = 20, position = dict(x=500, y=100),velocity=vel3, colour="red")

#top right
vel4 = GameObjects.Velocity(10, 315)
cube4 = GameObjects.Cube(size = 20, position = dict(x=500, y=100),velocity=vel4, colour="green")

border = GameObjects.Border(canvasWidth, canvasHeight)
cubes = [cube1,cube2,cube3,cube4]


def updateCanvas():
    canvas.delete("all")
    cube3.frame_update([border])
    cube3.render(canvas)
    #print("render complete")
    window.after(100, updateCanvas)


updateCanvas()
mainloop()