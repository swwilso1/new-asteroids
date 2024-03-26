from random import randint
from space_object import SpaceObject


class Asteroid(SpaceObject):

    def __init__(self, **kwargs):
        SpaceObject.__init__(self, **kwargs)

        self.__rotate_factor = 1
        if 'rotate_factor' in kwargs:
            self.__rotate_factor = kwargs['rotate_factor']

        self.__rotate_direction = randint(0, 1)

    def update(self):
        if self.__rotate_direction == 0:
            self.angle += self.__rotate_factor
        else:
            self.angle -= self.__rotate_factor
        
        distance = self.speed * (1 / 60)  # update fires 60/second

        self.update_x_and_y(distance)
