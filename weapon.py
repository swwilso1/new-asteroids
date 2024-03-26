from space_object import SpaceObject

class Weapon(SpaceObject):

    def __init__(self, **kwargs):
        SpaceObject.__init__(self, **kwargs)

        self.__acceleration = 10
        if 'acceleration' in kwargs:
            self.__acceleration = kwargs['acceleration']

    def update(self):
        self.speed += self.heading * self.__acceleration
        self.position += self.speed * (1 / 60)
