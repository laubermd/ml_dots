import math
import random
import vector

class Brain:
    step = 0
    size = 0
    directions = []
    mutateRate = .01

    def __init__(self, size, mutateRate, directions=[]):
        self.size = size
        self.mutateRate = mutateRate
        if (directions):
            self.directions = directions.copy()
        else:
            self.directions = [self.getRandomStep() for _ in range(size)]

    def getRandomStep(self):
        randomAngle = random.randrange(628)/10 #approx 2PI
        accX = math.sin(randomAngle)
        accY = math.cos(randomAngle)
        return vector.Vector(x=accX, y=accY)

    def incrementStep(self):
        self.step+=1
    
    def hasSteps(self):
        return self.step < self.size

    def getNextStep(self):
        return self.directions[self.step]

    def getStepCount(self):
        return self.step

    def clone(self):
        clonedBrain = Brain(self.size, self.mutateRate, self.directions.copy())
        return clonedBrain

    def mutate(self):
        for index in range(self.size):
            rand = random.random()
            if (self.mutateRate > rand):
                self.directions[index] = self.getRandomStep()