from tkinter import *
import random
from turtle import pos
import GameObjects
import time

global times

# Version 13

times = []
window = Tk()
canvasWidth = 1280
canvasHeight = 720
canvas = Canvas(window, width=canvasWidth, height=canvasHeight, bg="white" )
canvas.pack()

effects = (GameObjects.Score_Increase(), GameObjects.Powerup_Spawner(), GameObjects.Sweeper_Spawner())
powerups = (GameObjects.Eat_Enemy_Powerup, GameObjects.Score_Increase_Powerup, GameObjects.Temp_Change_Colour_Powerup)
game = GameObjects.Game(canvas, effects=(GameObjects.Powerup_Spawner(),), enemy_types=(GameObjects.Cube), powerups=(GameObjects.Eat_Enemy_Powerup,))

window.bind("<Motion>",lambda event, objects=game.objects: game.player.position_update(event=event,objects=objects))
window.update()
game.start_game()
mainloop()