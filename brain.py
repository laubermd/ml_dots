import math
import random

import vector

class Brain:
    step = 0
    size = 0
    directions = []

    def __init__(self, size):
        self.size = size
        self.directions = [self.getRandomStep() for _ in range(size)]

    def getRandomStep(self):
        randomAngle = random.randrange(628)/10 #approx 2PI
        # assume acc radius of 1
        accX = math.sin(randomAngle)
        accY = math.cos(randomAngle)

        return vector.Vector(x=accX, y=accY)

    def incrementStep(self):
        self.step+=1
    
    def hasSteps(self):
        return self.step < self.size

    def getNextStep(self):
        return self.directions[self.step]