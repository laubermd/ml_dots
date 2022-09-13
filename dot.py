import radar
import vector
import math
import pygame

class Dot:
    dotRadius,limit,fitness,bonus,stepCount = 2,5,0,1,0
    alive,reachedGoal,isBest = True,False,False

    def __init__(self, pos, mutateRate, screen):
        self.screen = screen
        self.mutateRate = mutateRate
        self.pos,self.vel,self.acc = pos,vector.Vector(0, 0),vector.Vector(0, 0)
        self.radars = [
            radar.Radar(self.pos, 30, 0, self.screen),
            radar.Radar(self.pos, 30, 90, self.screen),
            radar.Radar(self.pos, 30, 180, self.screen),
            radar.Radar(self.pos, 30, 270, self.screen)
        ]

    def getRadars(self):
        return self.radars

    def getPosition(self):
        return self.pos

    def getRadius(self):
        return self.dotRadius

    def isAlive(self):
        return self.alive

    def move(self, step):
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

    def getData(self):
        data = [self.radars[0].isClose(),
                self.radars[1].isClose(),
                self.radars[2].isClose(),
                self.radars[3].isClose(),
                0,0
        ]
        return data

    def drawRadar(self):
        for radar in self.radars:
            radar.draw(self.pos)

    def resetScreen(self):
        pygame.draw.circle(self.screen, (0, 0, 0), [self.pos.getX(),self.pos.getY()], 3)
        if (self.alive):
            self.drawRadar()