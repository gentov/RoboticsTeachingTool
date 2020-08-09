import numpy as np

class SimpleDrone():
    def __init__(self, mass, pos):
        self.mass = mass
        self.pos = pos
        self.velocity = 0
        self.power = 0
        self.gravity = 9.81
        self.gravityForce = self.mass*self.gravity
        # self.minPower = -500
        # self.maxPower = 10000 # I want to limit how much power to make 2.5 times weight

    def fly(self, power, t):
        # if power > self.maxPower:
        #     power = self.maxPower
        # if power < self.minPower:
        #     power = self.minPower
        netForce = power-self.gravityForce
        acceleration = netForce/self.mass
        self.velocity = acceleration*t
        self.pos = self.pos + self.velocity*t

        # self.pos = self.pos + (power - self.gravityForce) * t
