#! /usr/bin/env python3

import math
from vector import Vector


class SpaceObject(object):

    def __init__(self, **kwargs):
        self.__object = None
        if 'actor' in kwargs:
            self.__object = kwargs['actor']

        self.width = 100
        if 'width' in kwargs:
            self.width = kwargs['width']

        self.height = 100
        if 'height' in kwargs:
            self.height = kwargs['height']

        self.speed = Vector(0,0)
        if 'speed' in kwargs:
            value = kwargs['speed']
            if isinstance(value, Vector):
                self.speed = value
            elif isinstance(value, int) or isinstance(value, float):
                self.speed = Vector(value, value)

    def draw(self):
        self.__object.draw()

    @property
    def x(self) -> float:
        return self.__object.x
    
    @x.setter
    def x(self, value: float):
        self.__object.x = value
    
    @property
    def y(self) -> float:
        return self.__object.y
    
    @y.setter
    def y(self, value: float):
        self.__object.y = value

    @property
    def center(self) -> tuple:
        return self.__object.center
    
    @center.setter
    def center(self, value: tuple):
        self.__object.center = value
    
    @property
    def position(self) -> Vector:
        return Vector(self.__object.x, self.__object.y)
    
    @position.setter
    def position(self, value: Vector):
        self.__object.x = value.x
        self.__object.y = value.y
    
    @property
    def angle(self) -> float:
        return self.__object.angle
    
    @angle.setter
    def angle(self, value: float):
        self.__object.angle = value

    @property
    def screen_angle(self) -> float:
        new_angle = self.__object.angle + 90
        if new_angle >= 360:
            new_angle -= 360
        return new_angle

    @property
    def heading(self) -> Vector:
        screen_angle = self.screen_angle
        angle_in_radians = math.radians(screen_angle)
        if screen_angle == 0:
            return Vector(1, 0)
        elif 0 < screen_angle < 90:
            x = math.cos(angle_in_radians)
            y = math.sin(angle_in_radians)
            return Vector(x, -1 * y)
        elif screen_angle == 90:
            return Vector(0, -1)
        elif 90 < screen_angle < 180:
            angle_in_radians = math.radians(180 - screen_angle)
            x = math.cos(angle_in_radians)
            y = math.sin(angle_in_radians)
            return Vector(-1 * x, -1 * y)
        elif screen_angle == 180:
            return Vector(-1, 0)
        elif 180 < screen_angle < 270:
            angle_in_radians = math.radians(screen_angle - 180)
            x = math.cos(angle_in_radians)
            y = math.sin(angle_in_radians)
            return Vector(-1 * x, y)
        elif screen_angle == 270:
            return Vector(0, 1)
        elif 270 < screen_angle < 360:
            angle_in_radians = math.radians(360 - screen_angle)
            x = math.cos(angle_in_radians)
            y = math.sin(angle_in_radians)
            return Vector(x, y)
        else:
            return Vector(1, 0)

    @property
    def image(self):
        return self.__object.image

    @image.setter
    def image(self, value: str):
        self.__object.image = value

    @property
    def onscreen(self) -> bool:
        if self.x >= 0 and self.x <= self.width and \
            self.y >= 0 and self.y <= self.height:
            return True
        return False

    def update_x_and_y(self, distance):
        self.position += distance

        if self.x > self.width:
            self.x = 0
        elif self.x < 0:
            self.x = self.width

        if self.y > self.height:
            self.y = 0
        elif self.y < 0:
            self.y = self.height

    def update(self):
        pass
