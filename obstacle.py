import pygame

class Obstacle:

    def __init__(self, x1, y1, x2, y2, screen):
        self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
        self.screen = screen
        self.draw()

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))

    def checkCollision(self, dot):
        pos = dot.getPosition()
        return ((pos.getX() + dot.getRadius() > self.x1 and pos.getX() - dot.getRadius() < self.x2) and
                (pos.getY() + dot.getRadius() > self.y1 and pos.getY() - dot.getRadius() < self.y2))

    def checkRadarCollision(self, xPos, yPos):

        return ((xPos > self.x1 and xPos < self.x2) and
                (yPos > self.y1 and yPos < self.y2))