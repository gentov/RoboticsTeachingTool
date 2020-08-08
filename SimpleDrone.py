import numpy as np

class SimpleDrone():
    def __init__(self, mass, pos):
        self.mass = mass
        self.pos = pos
        self.power = 0
        self.gravity = 9.81
        self.gravityForce = self.mass*self.gravity
        self.minPower = -100
        self.maxPower = 100000000 # I want to limit how much power to make 2.5 times weight

    def fly(self, power, t):
        if power > self.maxPower:
            power = self.maxPower
        if power < self.minPower:
            power = self.minPower
        self.pos = self.pos + (power - self.gravityForce)*t
