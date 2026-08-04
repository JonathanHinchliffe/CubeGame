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


class Cube(Game_Object):

    def __init__(self, size, position = dict(x = 0, y = 0), velocity = Velocity(0,0), colour="grey"):
        self.size = size #size in px
        self.position = position
        self.velocity = velocity
        self.colour = colour

    def position_update(self, frame_rate = 30):
        ## TODO
        ## need collision method
        ##some way for framerate to become independent of velocity


        self.position["x"] = self.position["x"] + (self.velocity.x)
        self.position["y"] = self.position["y"] + (self.velocity.y)
        print(self.position)

    def render(self, canvas):
        canvas.create_rectangle(self.position["x"]-(self.size//2), self.position["y"]-(self.size//2), self.position["x"]+(self.size//2), self.position["y"]+(self.size//2), fill=self.colour)


