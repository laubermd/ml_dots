import math
import pygame
import vector

class Radar:

    def __init__(self, center, dist, angle, screen):
        self.center,self.dist,self.angle,self.screen = center,dist,angle,screen
        self.pos = vector.Vector(
            int(self.center.getX() + math.cos(math.radians(360 - (self.angle))) * self.dist),
            int(self.center.getY() + math.sin(math.radians(360 - (self.angle))) * self.dist)
        )

    def getDist(self):
        return self.dist

    def setDist(self, dist):
        self.dist = dist

    def isClose(self):
        return int(self.dist < 30)

    def getPosition(self):
        return self.pos

    def setPosition(self, pos):
        self.pos = pos

    def setCenter(self, center):
        self.center = center

    def getAngle(self):
        return self.angle

    def draw(self, center):
        pygame.draw.line(self.screen, (0, 255, 0), [center.getX(),center.getY()], [self.pos.getX(), self.pos.getY()], 1)
        pygame.draw.circle(self.screen, (0, 255, 0), [self.pos.getX(), self.pos.getY()], 2)