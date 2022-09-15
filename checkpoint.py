import pygame

class Checkpoint:

    def __init__(self, x1, y1, x2, y2, bonus, showCheckpoint, screen):
        self.x1,self.y1,self.x2,self.y2,self.bonus,self.showCheckpoint = x1,y1,x2,y2,bonus,showCheckpoint
        self.screen = screen
        self.draw()

    def draw(self):
        if self.showCheckpoint:
            pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))

    def getBonus(self):
        return self.bonus

    def checkCollision(self, dot):
        pos = dot.getPosition()
        return ((pos.getX() + dot.getRadius() > self.x1 and pos.getX() - dot.getRadius() < self.x2) and
                (pos.getY() + dot.getRadius() > self.y1 and pos.getY() - dot.getRadius() < self.y2))