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

effects = (GameObjects.Score_Increase(), GameObjects.Powerup_Spawner())
powerups = (GameObjects.Eat_Enemy_Powerup, GameObjects.Score_Increase_Powerup, GameObjects.Temp_Change_Colour_Powerup)
game = GameObjects.Game(canvas, effects=effects, enemy_types=(GameObjects.Cube), powerups=powerups)

window.bind("<Motion>",lambda event, objects=game.objects: game.player.position_update(event=event,objects=objects))
#updateCanvas()
#mainloop()
window.update()
game.start_game()
mainloop()