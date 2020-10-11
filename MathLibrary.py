#Library of simple math operations to practice functions and classes.

import math

def sum(a , b):
    return a + b


def substract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def power(a, b):
    return a ** b


class GeometricShapeAreas:
    def __init__(self):
        a = ""

    def __enter__(self):
        a = ""
    def __exit__(self, exc_type, exc_val, exc_tb):
        a = ""

    def square(self, area):
        return power(area, 2)

    def rectangle(self, base, height):
        return base * height

    def triangle(self, base, height):
        return self.rectangle(base, height) / 2.0

    def circle(self, radius):
        return math.pi * pow(radius,2)
