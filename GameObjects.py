from abc import ABC, abstractmethod
import math


class Game_Object(ABC):
    
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
        vertexs = ((round(self.position["x"]-(self.width//2)), round(self.position["y"]-(self.height//2))),
                    (round(self.position["x"]+(self.width//2)), round(self.position["y"]-(self.height//2))),
                    (round(self.position["x"]-(self.width//2)), round(self.position["y"]+(self.height//2))),
                    (round(self.position["x"]+(self.width//2)), round(self.position["y"]+(self.height//2))))
        #edges
        #top, left, right, bottom
        edges = ((vertexs[0],vertexs[1]),(vertexs[0],vertexs[2]),(vertexs[1],vertexs[3]),(vertexs[2],vertexs[3]))
        self.vertices = vertexs
        self.edges = edges

    def collision_check(self, objects = []):
        self.calculate_outline()
        collisions = []
        for o in objects:
            if isinstance(o, Border):
                border_collisions = self.border_collision_check(o)
                    #there has been a collision
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
            if (0 < self.angle < 90) or (180 < self.angle < 270):
                x = self.speed * (math.sin((math.radians(self.angle%90))))
                #print("Opp")
            elif (90 < self.angle < 180) or (270 < self.angle < 360):
                x = self.speed * (math.cos(math.radians(self.angle%90)))
            if self.angle > 180:
                print
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
        if angle > 360:
            angle -= 360
        self.angle = angle
        self.update_components(message="Changed angle")



class Cube(Game_Object, Collision_Rectangle):

    def __init__(self, size, position = dict(x = 0, y = 0), velocity = Velocity(0,0), colour="grey"):
        self.size = size #size in px
        super().__init__(size,size, position)
        self.position = position
        self.velocity = velocity
        self.colour = colour
        self.can_bounce = True

    def frame_update(self, objects = [], frame_rate = 30):
        self.position_update()
        collisions = self.collision_check(objects)
        if type(collisions[0]) != bool and self.can_bounce:
            #print(collisions[0])
            self.bounce(collisions[0])

    def position_update(self,frame_rate = 30):
        ## TODO
        ## need collision method
        ##some way for framerate to become independent of velocity


        self.position["x"] = round(self.position["x"] + (self.velocity.x),2)
        self.position["y"] = round(self.position["y"] + (self.velocity.y),2)
        

    def bounce(self, collisions):
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

    def border_collision_check(self, o):
        left_collision = False
        right_collision = False
        top_collision = False
        bottom_collision = False
        if self.vertices[0][0] <= 0:
            left_collision = True
        if self.vertices[3][0] >= o.width:
            right_collision = True
        if self.vertices[0][1] <= 0:
            top_collision = True
        if self.vertices[3][1] >= o.height:
            bottom_collision = True

        #if there has been a collision return which sides collided
        if left_collision == True or right_collision == True or top_collision ==True or bottom_collision == True:
            return (left_collision, right_collision, top_collision,bottom_collision)
        else:
            return (False)

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


