import vector
import math
import pygame

class Dot:
    dotRadius,limit,fitness,bonus,stepCount = 2,5,0,1,0
    alive,reachedGoal,isBest = True,False,False
    radars = []

    def __init__(self, pos, mutateRate, screen):
        self.screen = screen
        self.mutateRate = mutateRate
        self.pos,self.vel,self.acc = pos,vector.Vector(0, 0),vector.Vector(0, 0)

    def addRadar(self, radar):
        self.radars.append(radar)

    def getRadars(self):
        return self.radars

    def getCoord(self):
        x = self.pos.getX()
        y = self.pos.getY()
        return x-self.dotRadius, y+self.dotRadius, x+self.dotRadius, y-self.dotRadius

    def getPosition(self):
        return self.pos

    def getRadius(self):
        return self.dotRadius

    def getVelocity(self):
        return self.vel

    def isAlive(self):
        return self.alive

    def move(self, step):
        # TODO only move forward and/or turn
        self.acc=step
        self.vel.add(step)
        self.vel.limit(self.limit)
        self.pos.add(self.vel)
        self.stepCount+=1
        if self.stepCount > 200:
            self.unalive()

    def unalive(self):
        self.alive = False

    def setReachedGoal(self, reachedGoal):
        self.reachedGoal = reachedGoal

    def getReachedGoal(self):
        return self.reachedGoal

    def getStepCount(self):
        return self.stepCount

    def setBonus(self, bonus):
        self.bonus = bonus

    def getBonus(self):
        return self.bonus

    def setFitness(self, fitness):
        self.fitness = fitness

    def getFitness(self):
        return self.fitness

    def setBestDot(self, isBest):
        self.isBest = isBest

    def isBestDot(self):
        return self.isBest

    def clone(self, pos):
        clone = Dot(pos, self.mutateRate, self.screen)
        return clone

    # TODO init some radars
    def getData(self):
        data = [self.radars.copy()[0][1],
                self.radars.copy()[1][1],
                self.radars.copy()[2][1],
                self.radars.copy()[3][1],
                0,0
        ]
        return data

    # TODO move to radar object
    def drawRadar(self):
        for r in self.radars:
            pos, dist = r
            pygame.draw.line(self.screen, (0, 255, 0), [self.pos.getX(),self.pos.getY()], pos, 1)
            pygame.draw.circle(self.screen, (0, 255, 0), pos, 2)

    def resetScreen(self):
        pygame.draw.circle(self.screen, (0, 0, 0), [self.pos.getX(),self.pos.getY()], 3)
        if (self.alive):
            self.drawRadar()