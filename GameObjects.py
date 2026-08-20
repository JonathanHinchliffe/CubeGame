from abc import ABC, abstractmethod
from ast import Tuple
from tkinter import *
import math
import threading
import random
import time
import datetime
import os


class Game_Object(ABC):
    
    remove = False

    @abstractmethod
    def frame_update(self):
        pass

    @abstractmethod
    def render(self):
        pass


class Collision_Model(ABC):

    @abstractmethod
    def collision_check(self):
        pass

class Collision_Rectangle(Collision_Model):

    def __init__(self, width, height, position= dict(x = 0, y = 0)):
        self.width = width
        self.height = height
        self.position = position
        self.calculate_outline()

    def calculate_outline(self):
        #vertex
        #top left, top right, bottom left, bottom right
        vertexs = dict(top_left = (round(self.position["x"]-(self.width//2)), round(self.position["y"]-(self.height//2))),
                    top_right = (round(self.position["x"]+(self.width//2)), round(self.position["y"]-(self.height//2))),
                    bottom_left = (round(self.position["x"]-(self.width//2)), round(self.position["y"]+(self.height//2))),
                    bottom_right = (round(self.position["x"]+(self.width//2)), round(self.position["y"]+(self.height//2))))
        #edges
        #top, left, right, bottom
        #each edge contains min/max and opp
        edges = dict(top = dict(min_x = vertexs["top_left"][0],max_x = vertexs["top_right"][0],y = vertexs["top_left"][1]),
                     left = dict(min_y =vertexs["top_left"][1],max_y = vertexs["bottom_left"][1],x = vertexs["top_left"][0]), 
                     right = dict(min_y =vertexs["top_right"][1],max_y =vertexs["bottom_right"][1], x = vertexs["top_right"][0]),
                     bottom = dict(min_x =vertexs["bottom_left"][0],max_x=vertexs["bottom_right"][0], y = vertexs["bottom_right"][1]))
        self.vertices = vertexs
        self.edges = edges

    def collision_check(self, objects = []):
        self.calculate_outline()
        collisions = []
        for o in objects:
            if isinstance(o, Border):
                border_collisions = self.border_collision_check(o)
                    #there has been a collision
            elif isinstance(o, Player):
                for key, value in o.game_object.vertices.items():
                    if (self.edges["top"]["min_x"] <= value[0] <= self.edges["top"]["max_x"]) and (self.edges["left"]["min_y"]<= value[1] <= self.edges["left"]["max_y"]):
                        #vertex is within this cube
                        collisions.append([o, key])
            elif o == self:
                continue
            else:
                ## PLAYER NEEDS o.game_object.vertices
                for key, value in o.vertices.items():
                    if (self.edges["top"]["min_x"] <= value[0] <= self.edges["top"]["max_x"]) and (self.edges["left"]["min_y"]<= value[1] <= self.edges["left"]["max_y"]):
                        #vertex is within this cube
                        collisions.append([o, key])
                        
        #print(self.edges)
        return (border_collisions, collisions)
    
    def border_collision_check(self,o):
        pass

class Velocity:


    def __init__(self, angle = 0, speed = 0):
        self.speed = speed
        self.angle = angle
        #print(speed, angle)
        if self.speed != 0:
            self.update_components(message="Speed not 0 on init")
        else:
            self.update_components(message="Stationary")
        
    def calculate_x(self):
        if self.speed == 0:
            return 0
        if self.angle == 0 or self.angle == 180:
            #print("What?")
            return 0
        elif self.angle == 90:
            return self.speed
        elif self.angle == 270:
            return -self.speed
        else:
            #print(self.angle)
            if (0 < self.angle < 90) or (180 < self.angle < 270):
                x = self.speed * (math.sin((math.radians(self.angle%90))))
                #print("Opp")
            elif (90 < self.angle < 180) or (270 < self.angle < 360):
                x = self.speed * (math.cos(math.radians(self.angle%90)))
            if self.angle > 180:
                x = -x
            return round(x,2)
        
    def calculate_y(self):
        if self.speed == 0:
            return 0
        if self.angle == 90 or self.angle == 270:
            return 0
        elif self.angle == 0:
            return -self.speed
        elif self.angle == 180:
            return self.speed
        else:
            if (90 < self.angle < 180) or (270 < self.angle < 360):
                y = self.speed * (math.sin(math.radians(self.angle%90)))
            elif (0 < self.angle < 90) or (180 < self.angle < 270):
                y = self.speed * (math.cos(math.radians(self.angle%90)))
            if 90 > self.angle or self.angle > 270:
                y = -y
            return round(y,2)

    def update_components(self, message=""):
        show_message = False
        if message != "" and show_message:
            print(message)
        self.x = self.calculate_x()
        self.y = self.calculate_y()

    def set_speed(self, speed):
        self.speed = speed
        self.update_components(message="Changed speed")

    def set_angle(self, angle):
        if angle < 0:
            angle = 360-angle
        if angle >= 360:
            angle -= 360
        self.angle = angle
        self.update_components(message="Changed angle")



class Cube(Game_Object, Collision_Rectangle):

    def __init__(self, size, position = dict(x = 0, y = 0), velocity = Velocity(0,0), colour="grey"):
        self.size = size #size in px
        super().__init__(size, size,position = position)
        self.position = position
        self.velocity = velocity
        self.colour = colour
        self.can_bounce = True

    def frame_update(self, objects = [], frame_rate = 30):
        self.position_update()
        collisions = self.collision_check(objects)
        #print(collisions)
        if type(collisions[0]) != bool and self.can_bounce:
            #print(collisions[0])
            self.wall_bounce(collisions[0])
        if type(collisions[1] != [] and self.can_bounce):
            for collision in collisions[1]:
                if isinstance(collision[0], Player) == False:
                    self.bounce(hit_object = collision[0], vertex = collision[1])
                else:
                    collision[0].hit = True



    def position_update(self,frame_rate = 30):
        ## TODO
        ## need collision method
        ##some way for framerate to become independent of velocity


        self.position["x"] = round(self.position["x"] + (self.velocity.x),2)
        self.position["y"] = round(self.position["y"] + (self.velocity.y),2)
        

    def wall_bounce(self, collisions):
        #print("BOUNCE!", collisions)
        #left right top bottom
        #T/F   T/F  T/F  T/F
        if (collisions[0] == True or collisions[1] == True) and (collisions[2] or collisions[3]):
            #corner bounce
            self.velocity.set_angle( round((self.velocity.angle+180)%360))
            self.position_update()
            return
        
        if self.velocity.angle == 0 or self.velocity.angle == 90 or self.velocity.angle == 180 or self.velocity.angle == 270:
            #tangent bounce
            self.velocity.set_angle(round((self.velocity.angle+180)%360))
            self.position_update()
            return
        
        if collisions[0]:
            #print(self.velocity.angle, "Before bounce")
            #left bounce
            #angle is between 181 and 359 but not 270
            if self.velocity.angle > 270:
                self.velocity.set_angle(round(360-self.velocity.angle))
            if self.velocity.angle < 270:
                self.velocity.set_angle(round(self.velocity.angle-90))

            #print(self.velocity.angle, "After bounce")
            self.position_update()
            return

        if collisions[1]:
            #right bounce
            #angle is between 1 and 179 but not 90
            #print(self.velocity.angle, "Before bounce")
            if self.velocity.angle > 90:
                self.velocity.set_angle(round(360-self.velocity.angle))
            if self.velocity.angle < 90:
                self.velocity.set_angle(round(360-self.velocity.angle))
            self.position_update()
            #print(self.velocity.angle, "After bounce")
        
        if collisions[2]:
            #top bounce
            #angle is betweem 1 and 90 or 270 and 360
            if self.velocity.angle < 90:
                self.velocity.set_angle(round(180-self.velocity.angle))
            if self.velocity.angle > 270:
                self.velocity.set_angle(round(540-self.velocity.angle))
            self.position_update()
            return
        
        if collisions[3]:
            #bottom bounce
            #angle is between 91 and 269 but not 180
            if self.velocity.angle < 180:
                self.velocity.set_angle(round(180-self.velocity.angle))
            if self.velocity.angle > 180:
                self.velocity.set_angle(round(540-self.velocity.angle))
                #print("Bounce", self.velocity.angle, self.velocity.x)
            self.position_update()
            return


    def bounce(self, hit_object, vertex):
        if self.velocity.x == 0 or self.velocity.y == 0:
            self.velocity.set_angle(self.velocity.angle+180)
            self.position_update()
            return
        elif hit_object.velocity.x == 0 or hit_object.velocity.y == 0:
            hit_object.velocity.set_angle(hit_object.velocity.angle)
            hit_object.position_update()
            return
        else:
            self_gradient = self.velocity.y / self.velocity.x
            object_gradient = hit_object.velocity.y / hit_object.velocity.x
            if (self.velocity.y / self.velocity.x)*(hit_object.velocity.y / hit_object.velocity.x) != 1:
                intercept_angle = math.degrees(math.atan((object_gradient-self_gradient)/(1-(object_gradient*self_gradient))))
            else:
                intercept_angle = 90
            #if intercept_angle < 0 and ((90 < self.velocity.angle < 180) or (270 < self.velocity.angle < 360)) and ((90 < hit_object.velocity.angle < 180) or (270 < hit_object.velocity.angle < 360)):
            if self_gradient > object_gradient and (0 < self.velocity.angle < 180):
                self.velocity.set_angle(self.velocity.angle + 180 - intercept_angle)
                hit_object.velocity.set_angle(hit_object.velocity.angle - 180 + intercept_angle)
                self.position_update()
                return
            if self_gradient > object_gradient and (180 < self.velocity.angle < 360):
                self.velocity.set_angle(self.velocity.angle - 180 + intercept_angle)
                hit_object.velocity.set_angle(hit_object.velocity.angle + 180 - intercept_angle)
                self.position_update()
                return
            if self_gradient < object_gradient and (0 < self.velocity.angle < 180):
                self.velocity.set_angle(self.velocity.angle - 180 + intercept_angle)
                hit_object.velocity.set_angle(hit_object.velocity.angle + 180 - intercept_angle)
                self.position_update()
                return
            if self_gradient < object_gradient and (180 < self.velocity.angle < 360):
                self.velocity.set_angle(self.velocity.angle + 180 - intercept_angle)
                hit_object.velocity.set_angle(hit_object.velocity.angle - 180 + intercept_angle)
                self.position_update()
                return

        pass
        
    def border_collision_check(self, o):
        left_collision = False
        right_collision = False
        top_collision = False
        bottom_collision = False
        if self.edges["left"]["x"] <= 0:
            left_collision = True
        if self.edges["right"]["x"] >= o.width:
            right_collision = True
        if self.edges["top"]["y"] <= 0:
            top_collision = True
        if self.edges["bottom"]["y"] >= o.height:
            bottom_collision = True

        #if there has been a collision return which sides collided
        if left_collision == True or right_collision == True or top_collision ==True or bottom_collision == True:
            return (left_collision, right_collision, top_collision,bottom_collision)
        else:
            return (False)

    def closest_object(self, objects) -> tuple:
        closest = None
        distance = 0
        for obj in objects:
            if type(obj) == Player:
                dx = obj.game_object.position["x"] - self.position["x"]
                dy = obj.game_object.position["y"] - self.position["y"]
                if math.sqrt((dx**2)+(dy**2)) < 100:
                    closest = obj
                    distance = 1
            elif type(obj) == Border:
                pass
            else:
                dx = obj.position["x"] - self.position["x"]
                dy = obj.position["y"] - self.position["y"]
            if dx < 0:
                dx *= -1
            if dy < 0:
                dy *= -1

            dist = math.sqrt((dx**2)+(dy**2))
            if dist > distance:
                closest = obj
                distance = dist
        return (closest, distance)

    def render(self, canvas):
        canvas.create_rectangle(self.position["x"]-(self.size//2), self.position["y"]-(self.size//2), self.position["x"]+(self.size//2), self.position["y"]+(self.size//2), fill=self.colour)

class Border(Collision_Rectangle):

    def __init__(self, width, height):
        super().__init__(width, height)

    def calculate_outline(self):
        vertexs = ((0,0), (self.width,0), (0,self.height), (self.width, self.height))
        edges = ((vertexs[0],vertexs[1]),(vertexs[0],vertexs[2]),(vertexs[1],vertexs[3]),(vertexs[2],vertexs[3]))

        self.vertices = vertexs
        self.edges = edges

    def collision_check(self):
        return super().collision_check()

class Player(Game_Object):

    remove_enemy_on_collision = False

    def __init__(self, game_object = None):
        self.game_object = game_object
        self.game_object.can_bounce = False
        self.hit = False

    def render(self, canvas):
        if self.game_object != None:
            self.game_object.render(canvas)

    def position_update(self, event, objects=[], frame_rate=30):
        if self.game_object != None:
            self.game_object.position["y"] = event.y
            self.game_object.position["x"] = event.x
            collisions = self.game_object.collision_check(objects)
            if collisions != (False, []):
                #player has hit something
                #game over
                #print("Player Hit!")
                #self.game_object.colour="green"
                self.hit == True
                for collision in collisions[1]:
                    collision_object = collision[0]
                    if issubclass(type(collision_object), Item):
                        collision_object.on_player_collision(self)
                        collision_object.remove = True
                        self.hit = False
                    if self.remove_enemy_on_collision:
                        collision_object.remove = True
                        self.hit = False

    def frame_update(self):
        pass


class Item(Cube):

    def __init__(self, size = 40, position=dict(x=0, y=0), velocity=Velocity(0, 0), colour="grey"):
        #print(position)
        super().__init__(size = size, position = position, velocity = velocity, colour=colour)
        self.info = ["Start Time", "On Player Collision Time", "End Effect Time"]
    def on_player_collision(self):
        pass

class Timed_Effect(ABC):

    #length in milliseconds
    effect_length: int
    effect_active = False

    @abstractmethod
    def start_effect(self):
        pass

    @abstractmethod
    def end_effect(self):
        pass

class Change_Colour_Powerup(Item):

    def __init__(self, size=40, position=dict(x=0, y=0), velocity=Velocity(0, 0), colour="pink"):
        super().__init__(size = size, position = position, velocity = velocity, colour = colour)

    def on_player_collision(self, player):
        self.remove = True
        player.game_object.colour = self.colour
        print("Player Hit Power up")
        pass

class Temp_Change_Colour_Powerup(Change_Colour_Powerup, Timed_Effect):

    def __init__(self, info, effect_length = 5000,size = 40, position=dict(x=0, y=0), velocity=Velocity(0, 0), colour="pink"):
        super().__init__(size = size, position = position, velocity = velocity, colour = colour)
        self.effect_length = effect_length
        self.game_timer = info["game_timer"]
        self.info[0] = time.time() - self.game_timer
        info["powerup_data"][self.__class__.__name__].append(self.info)

    def on_player_collision(self, player):
        self.info[1] = time.time() - self.game_timer
        self.start_effect(player)

    def start_effect(self, player):
        if self.effect_active == False:
            print("START EFFECT")
            self.player_original_colour = player.game_object.colour
            self.effect_active = True
            player.game_object.colour = self.colour
            timer = threading.Timer((self.effect_length/1000), lambda self=self, player=player: self.end_effect(player))
            timer.start()


    def end_effect(self, player):
        self.effect_active = False
        self.info[2] = time.time() - self.game_timer
        print("END EFFECT")
        player.game_object.colour = self.player_original_colour

class Eat_Enemy_Powerup(Item, Timed_Effect):

    def __init__(self, info, effect_length = 5000, size = 40, position=dict(x=0, y=0), velocity=Velocity(0, 0), colour="purple"):
        super().__init__(size = size, position = position, velocity = velocity, colour = colour)
        self.effect_length = effect_length
        self.game_timer = info["game_timer"]
        self.info[0] = time.time() - self.game_timer
        info["powerup_data"][self.__class__.__name__].append(self.info)

    def on_player_collision(self, player):
        self.info[1] = time.time() - self.game_timer
        self.start_effect(player)

    def start_effect(self, player):
        if self.effect_active == False:
            print("START EFFECT")
            player.remove_enemy_on_collision = True
            self.effect_active == True
            timer = threading.Timer((self.effect_length/1000), lambda self=self, player=player: self.end_effect(player))
            timer.start()

    def end_effect(self, player):
        self.effect_active = False
        self.info[2] = time.time() - self.game_timer
        print("END EFFECT")
        player.remove_enemy_on_collision = False


class Score_Increase_Powerup(Item, Timed_Effect):

    def __init__(self, info, effect_length = 5000, size = 40, position=dict(x=0, y=0), velocity=Velocity(0, 0), colour="cyan"):
        super().__init__(size = size, position = position, velocity = velocity, colour = colour)
        self.effect_length = effect_length
        self.score = info["score"]
        self.game_timer = info["game_timer"]
        self.info[0] = time.time() - self.game_timer
        info["powerup_data"][self.__class__.__name__].append(self.info)

    def on_player_collision(self, player):
        self.info[1] = time.time() - self.game_timer
        self.start_effect(self.score)

    def start_effect(self, score):
        if self.effect_active == False:
            print("EFFECT START")
            self.effect_active = True
            score.score_increase = score.score_increase *2
            timer = threading.Timer((self.effect_length/1000), lambda self=self, score=score: self.end_effect(score))
            timer.start()

    def end_effect(self, score):
        print("EFFECT END")
        self.info[2] = time.time() - self.game_timer
        self.effect_active = False
        if score.score_increase %2:
            score.score_increase = (score.score_increase//2)+1
        else:
            score.score_increase = score.score_increase//2


class Score(Game_Object):

    score = 0

    def __init__(self, score_increase = 1):
        self.score_increase = score_increase

    def frame_update(self):
        self.score += self.score_increase

    def render(self):
        pass

class Score_Increase(Timed_Effect):

    def __init__(self, increase = 1, effect_length = 5000):
        self.effect_length = effect_length
        self.increase = increase
        #self.start_effect(score)

    def start_effect(self, info):
        #print("EFFECT START")
        info["score"].score_increase += 1
        timer = threading.Timer((self.effect_length/1000), lambda score=info["score"]: self.end_effect(score))
        timer.start()

    def end_effect(self, score):
        #print("EFFECT END")
        self.start_effect(dict(score = score))

class Powerup_Spawner(Timed_Effect):

    effect_length = 7500

    def start_effect(self, info):
        #print(info)
        #print("EFFECT START")
        timer = threading.Timer((Powerup_Spawner.effect_length/1000), lambda info=info: self.end_effect(info))
        timer.start()

    def end_effect(self, info):
        powerup = info["powerups"][random.randint(0,len(info["powerups"])-1)]
        #print(info["objects"][1])
        new_powerup = powerup(info, position=dict(x=random.randint(25,info["objects"][1].width-25),y=random.randint(25,info["objects"][1].height-25)))
        i = 0
        while i < 20:
            if new_powerup.closest_object(info["objects"])[1] > 50:
                i += 50
                info["objects"].append(new_powerup)
                new_powerup.position["x"] = random.randint(25,info["objects"][1].width-25)
                new_powerup.position["y"] = random.randint(25,info["objects"][1].height-25)
            i += 1
        self.start_effect(info)

class Game:

    def __init__(self, canvas:Canvas, effects:tuple[Timed_Effect,...], enemy_types:tuple[Game_Object,...], powerups:tuple[Item,...] = (), player = Player(Cube(size=40, position=dict(x=700,y=400),colour="blue")), border=Border(1280,720), max_enemies = 20, frame_rate = 10):
        self.canvas = canvas
        self.effects = effects
        self.enemy_types = enemy_types
        self.powerups = powerups
        self.max_enemies = max_enemies
        self.player = player
        self.border = border
        self.objects = [self.player, self.border]
        self.score = Score()
        self.frame_rate = frame_rate
        self.powerup_data = dict()
        for p in self.powerups:
            self.powerup_data[p.__name__] = []

    def start_game(self):
        self.game_timer = time.time()
        print("START GAME")
        self.frame_update()
        for effect in self.effects:
            effect.start_effect(info = dict(score = self.score, objects = self.objects, powerups=self.powerups, powerup_data=self.powerup_data, game_timer = self.game_timer))

    def frame_update(self):
        self.canvas.delete("all")
        if len(self.objects) < self.max_enemies:
            self.spawn_enemy()
            
        for obj in self.objects:
            if obj.__class__.__name__ == "Border":
                pass
            elif obj.__class__.__name__ == "Player":
                obj.render(self.canvas)
            elif obj.remove:
                self.objects.remove(obj)
            else:
                obj.frame_update(objects=self.objects)
                obj.render(self.canvas)
        if self.player.hit == False:
            self.canvas.master.after((1000//self.frame_rate), self.frame_update)
            self.score.frame_update()
        else:
            self.end_game()

    def spawn_enemy(self):
        x = 0
        while x < 20:
            vel = Velocity(angle=random.randint(0,359), speed=random.randint(5,30))
            new_enemy = Cube(size=random.randint(10,40), position=dict(x=random.randint(100,self.canvas.winfo_width()-4),y=random.randint(50,self.canvas.winfo_height()-4)), velocity=vel)
            if new_enemy.closest_object(self.objects)[1] > 50:
                self.objects.append(new_enemy)
                x + 50
            x += 1

    def canvas_update(self):
        pass

    def end_game(self):
        game_version = os.path.getmtime("CubeGame.py")
        game_version = datetime.datetime.fromtimestamp(game_version)
        date = datetime.datetime.now()
        time_survived = time.time() - self.game_timer
        file = open("Data/game-results.csv", "a")
        file.write(str(game_version) + "," +  str(date) + "," + str(time_survived) + "," + str(self.score.score) + "\n")
        file.close()
        self.save_powerup_data(game_version, date)

    def save_powerup_data(self ,game_version,  date):
        file = open("Data/powerup-data.csv", "a")
        for key in self.powerup_data.keys():
            if self.powerup_data[key] != []:
                for item in self.powerup_data[key]:
                    #what reach record should be
                    #date, powerup_name, spawn_time, activated_time, end_time
                    if item[0] == "Start Time":
                        # This item is wrong don't save to csv
                        continue
                    file.write(f"{date},{key},{item[0]},")
                    if item[1] == "On Player Collision Time":
                        #Powerup was never activated
                        file.write(",")
                    else: 
                        file.write(f"{item[1]},")
                    if item[2] == "End Effect Time":
                        #Powerup effect never ended
                        file.write("\n")
                    else:
                        file.write(f"{item[2]}\n")