import vector
import brain

class Dot:
    pos = vector.Vector(x=0,y=0)
    vel = vector.Vector(x=0,y=0)
    acc = vector.Vector(x=0,y=0)
    dotSize = 4
    brain = brain.Brain(1000)

    limit = 5
    alive = True
    reachedGoal = False
    isBest = False

    def __init__(self, pos):
        # self.brain = brain.Brain(1000); # new brain with 1000 instructions

        # start the dots at the bottom of the window with a no velocity or acceleration
        self.pos = pos
        # self.vel = vector.Vector(0, 0)
        # self.acc = vector.Vector(0, 0)

    def getCoord(self):
        x = self.pos.getX()
        y = self.pos.getY()
        print("coord: %d, %d, %d, %d" % (x-2, y, x+2, y-4))
        return x-2, y, x+2, y-4

    def getVelocity(self):
        return self.vel

    def isAlive(self):
        return self.alive

    def move(self):
        if self.brain.hasSteps():
            step = self.brain.getNextStep()
            # apply the acceleration and move the dot
            # self.acc=step
            self.vel.add(step, self.limit)
            self.pos.add(self.vel)
            self.brain.incrementStep()
        else:
            self.alive = False

        