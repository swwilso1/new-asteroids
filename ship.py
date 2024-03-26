from space_object import SpaceObject
from vector import Vector


class Ship(SpaceObject):

    ROTATE_NEUTRAL = 0
    ROTATE_LEFT = 1
    ROTATE_RIGHT = 2

    def __init__(self, **kwargs):
        SpaceObject.__init__(self, **kwargs)

        self.__rotate_factor = 0
        if 'rotate_factor' in kwargs:
            self.__rotate_factor = kwargs['rotate_factor']
        
        self.__acceleration = 1.0
        if 'acceleration' in kwargs:
            self.__acceleration = kwargs['acceleration']
        
        self.center = self.width / 2, self.height / 2
        
        self.__rotate = False
        self.__rotate_direction = Ship.ROTATE_NEUTRAL
        self.__thrust = False
        self.__shield = False

        self.__missile_position_right = True

    @property
    def rotate(self) -> bool:
        return self.__rotate
    
    @rotate.setter
    def rotate(self, value: bool):
        self.__rotate = value

    @property
    def rotate_direction(self) -> int:
        return self.__rotate_direction

    @rotate_direction.setter
    def rotate_direction(self, value: int):
        self.__rotate_direction = value

    @property
    def thrust(self) -> bool:
        return self.__thrust
    
    @thrust.setter
    def thrust(self, value: bool):
        self.__thrust = value

    @property
    def shield(self) -> bool:
        return self.__shield

    @shield.setter
    def shield(self, value: bool):
        self.__shield = value

    @property
    def laser_position(self) -> Vector:
        return self.position + self.heading * 50

    @property
    def missile_position(self) -> Vector:
        larger_offset = 20
        smaller_offset = 15

        if self.screen_angle == 0:
            if self.__missile_position_right:
                position = Vector(self.x, self.y + larger_offset)
            else:
                position = Vector(self.x, self.y - larger_offset)
        elif 0 < self.screen_angle < 90:
            if self.__missile_position_right:
                position = self.position + smaller_offset
            else:
                position = self.position - smaller_offset
        elif self.screen_angle == 90:
            if self.__missile_position_right:
                position = Vector(self.x + larger_offset, self.y)
            else:
                position = Vector(self.x - larger_offset, self.y)
        elif 90 < self.screen_angle < 180:
            if self.__missile_position_right:
                position = Vector(self.x + smaller_offset, self.y - smaller_offset)
            else:
                position = Vector(self.x - smaller_offset, self.y + smaller_offset)
        elif self.screen_angle == 180:
            if self.__missile_position_right:
                position = Vector(self.x, self.y - larger_offset)
            else:
                position = Vector(self.x, self.y + larger_offset)
        elif 180 < self.screen_angle < 270:
            if self.__missile_position_right:
                position = self.position - smaller_offset
            else:
                position = self.position + smaller_offset
        elif self.screen_angle == 270:
            if self.__missile_position_right:
                position = Vector(self.x - larger_offset, self.y)
            else:
                position = Vector(self.x + larger_offset, self.y)
        else:  # ship.screen_angle > 270
            if self.__missile_position_right:
                position = Vector(self.x - smaller_offset, self.y + smaller_offset)
            else:
                position = Vector(self.x + smaller_offset, self.y - smaller_offset)
        
        self.__missile_position_right = not self.__missile_position_right

        return position

    def update(self):
        if self.rotate:
            if self.rotate_direction == Ship.ROTATE_LEFT:
                self.angle += self.__rotate_factor
            elif self.rotate_direction == Ship.ROTATE_RIGHT:
                self.angle -= self.__rotate_factor
            if self.angle > 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360

        if self.thrust:
            self.speed += self.heading * self.__acceleration

        distance = self.speed * (1 / 60)  # update fires 60/second

        self.update_x_and_y(distance)
