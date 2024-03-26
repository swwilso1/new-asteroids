#! /usr/bin/env python3

from __future__ import division
import math
import sys


class Vector(object):

    """Simple Vector operation class"""

    def __init__(self, *values):
        # Check that all arguments are numeric:
        for i in values:
            if not (isinstance(i, int) or isinstance(i, float)):
                raise ValueError("Argument " + repr(i) + " is not a numeric value.")

        if len(values) > 3 or len(values) < 2:
            raise AssertionError("Too many arguments, only 2D and 3D Vectors supported")

        self.__values = list(values)

    @property
    def x(self):
        return self.__values[0]

    @x.setter
    def x(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Argument " + repr(value) + " is not a numeric value.")
        self.__values[0] = value

    @property
    def y(self):
        return self.__values[1]

    @y.setter
    def y(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Argument " + repr(value) + " is not a numeric value.")
        self.__values[1] = value

    @property
    def z(self):
        if len(self.__values) < 3:
            raise ValueError("Vector does not have a z value")
        return self.__values[2]

    @z.setter
    def z(self, value):
        if len(self.__values) < 3:
            raise ValueError("Vector does not have a z value")
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Argument " + repr(value) + " is not a numeric value.")
        self.__values[2] = value

    @property
    def magnitude(self):
        mag_sum = 0
        for component in self.__values:
            mag_sum += component**2

        return math.sqrt(mag_sum)

    def normalize(self):
        magnitude = self.magnitude
        new_values = []
        for i in range(0, len(self.__values)):
            new_values.append(self.__values[i] / magnitude)

        self.__values = new_values

    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self.__values) != len(other.__values):
                raise ValueError("Vectors have differing dimensions")

            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] + other.__values[i])
            return Vector(*new_values)
        elif isinstance(other, int) or isinstance(other, float):
            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] + other)
            return Vector(*new_values)
        else:

            raise ValueError("No method for adding Vector and objects of " + str(type(other)))

    def __sub__(self, other):
        if isinstance(other, Vector):
            if len(self.__values) != len(other.__values):
                raise ValueError("Vectors have differing dimensions")

            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] - other.__values[i])
            return Vector(*new_values)
        elif isinstance(other, int) or isinstance(other, float):
            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] - other)
            return Vector(*new_values)
        else:

            raise ValueError("No method for subtracting objects of " + str(type(other)) + " from Vector")

    def __mul__(self, scalar):
        new_values = []
        for i in range(0, len(self.__values)):
            new_values.append(self.__values[i] * scalar)
        return Vector(*new_values)

    if sys.version_info[0] > 2:

        def __truediv__(self, scalar):
            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] / scalar)
            return Vector(*new_values)

    else:
        
        def __div__(self, scalar):
            new_values = []
            for i in range(0, len(self.__values)):
                new_values.append(self.__values[i] / scalar)
            return Vector(*new_values)

    def __neg__(self):
        new_values = []
        for i in range(0, len(self.__values)):
            new_values.append(-self.__values[i])
        return Vector(*new_values)

    def __getitem__(self, index):
        return float(self.__values[index])

    def __setitem__(self, index, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError("Right hand side is not a numeric value")

        self.__values[index] = float(value)

    def __len__(self):
        return len(self.__values)

    def __format(self, prefix, format_function):
        the_string = prefix + "("
        for i in range(0, len(self.__values)):
            the_string += format_function(self.__values[i])
            if i < (len(self.__values) - 1):
                the_string += ", "
            
        return the_string + ")"

    def __eq__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                return False
            for i in range(0, len(self)):
                if self[i] != other[i]:
                    return False
            return True
        return False
    
    def __ne__(self, other):
        return not (self == other)        

    def __str__(self):
        return self.__format("", str)

    def __repr__(self):
        return self.__format("Vector", repr)


def vector_from_points(point1, point2):
    if len(point1) != len(point2):
        raise ValueError("Points have different dimensions")

    new_values = []
    for i in range(0, len(point1)):
        new_values.append(point2[i] - point1[i])

    return Vector(*new_values)
