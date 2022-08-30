import vector
import brain

class Dot:
    pos = vector.Vector(x=0,y=0)
    vel = vector.Vector(x=0,y=0)
    acc = vector.Vector(x=0,y=0)
    dotSize = 4
    dotBrain = brain.Brain(1)
    limit = 5
    alive = True
    reachedGoal = False
    isBest = False
    fitness = 0

    def __init__(self, pos, dotBrain=None):
        if dotBrain:
            self.dotBrain = dotBrain
        else:
            self.dotBrain=brain.Brain(1000)
        # start the dots at the bottom of the window with a no velocity or acceleration
        self.pos = pos
        self.vel = vector.Vector(0, 0)
        self.acc = vector.Vector(0, 0)

    def getCoord(self):
        x = self.pos.getX()
        y = self.pos.getY()
        return x-2, y+2, x+2, y-2

    def getPosition(self):
        return self.pos

    def getVelocity(self):
        return self.vel

    def isAlive(self):
        return self.alive

    def move(self):
        if self.dotBrain.hasSteps():
            step = self.dotBrain.getNextStep()
            # apply the acceleration and move the dot
            self.acc=step
            self.vel.add(step)
            self.vel.limit(self.limit)
            self.pos.add(self.vel)
            self.dotBrain.incrementStep()
        else:
            self.unalive()

    def unalive(self):
        self.alive = False

    def setReachedGoal(self, reachedGoal):
        self.reachedGoal = reachedGoal

    def getReachedGoal(self):
        return self.reachedGoal

    def getStepCount(self):
        return self.dotBrain.getStepCount()

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def setBestDot(self, isBest):
        self.isBest = isBest

    def isBestDot(self):
        return self.isBest

    def clone(self, pos):
        babyBrain = self.dotBrain.clone()
        baby = Dot(pos, dotBrain=babyBrain)
        return baby

    def mutate(self):
        self.dotBrain.mutate()