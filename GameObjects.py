from abc import ABC, abstractmethod
import math

class Velocity():


    def __init__(self, speed = 0, angle = 0):
        self.speed = speed
        self.angle = angle
        self.x = self.calculate_x()
        self.y = self.calculate_y()
        
    def calculate_x(self):
        if self.angle == 0 or self.angle == 180:
            return 0
        else:
            x = self.speed * (math.sin((math.radians(self.angle%90))))
            if self.angle > 180:
                x = -x
            return round(x,2)
        
    def calculate_y(self):
        if self.angle == 90 or self.angle == 270:
            return 0
        else:
            y = self.speed * (math.cos(math.radians(self.angle%90)))
            if 90 < self.angle < 270:
                y = -y
            return round(y,2)

    def update_components(self):
        self.calculate_x()
        self.calculate_y()

    def set_speed(self, speed):
        self.speed = speed
        self.update_components()

    def set_angle(self, angle):
        self.angle = angle
        self.update_components()

class Game_Object(ABC):
    
    @abstractmethod
    def position_update(self):
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
        for o in objects:
            if isinstance(o, Border):
                self.border_collision_check(o)
        #print(self.edges)
    
    def border_collision_check(self,o):
        pass    

class Cube(Game_Object, Collision_Rectangle):

    def __init__(self, size, position = dict(x = 0, y = 0), velocity = Velocity(0,0), colour="grey"):
        self.size = size #size in px
        super().__init__(size,size, position)
        self.position = position
        self.velocity = velocity
        self.colour = colour

    def position_update(self, objects = [],frame_rate = 30):
        ## TODO
        ## need collision method
        ##some way for framerate to become independent of velocity


        self.position["x"] = round(self.position["x"] + (self.velocity.x),2)
        self.position["y"] = round(self.position["y"] + (self.velocity.y),2)
        self.collision_check(objects)
        #print(self.position)

    def border_collision_check(self, o):
        if self.vertices[0][0] < 0 and self.vertices[0][1] > 0 and self.vertices[2][0] < 0 and self.vertices[2][1] < o.height:
            #left wall bounce
            if self.velocity.angle < 270:
                self.velocity.angle -= 90
            else:
                self.velocity.angle = (self.velocity+90)%360
        #top bounce        
        elif self.vertices[0][0] > 0 and self.vertices[0][1] < 0 and self.vertices[1][0] < o.width and self.vertices[1][1] < 0:
            if self.velocity.angle < 90:
                self.velocity.angle += 90
            else:
                self.velocity.angle -= 90

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