import pygame
import vector

class Goal:
    radius = 3
    bonus = 1000000

    def __init__(self, x, y, screen):
        self.pos = vector.Vector(x,y)
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, (255, 0, 0), [250,10], 4)

    def checkCollision(self, dot):
        dotPos = dot.getPosition()
        return (abs(self.pos.getX()-dotPos.getX()) < 5 and 
                abs(self.pos.getY()-dotPos.getY()) < 5)

    def getPosition(self):
        return self.pos

    def getBonus(self):
        return self.bonus