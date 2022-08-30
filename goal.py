import vector

class Goal:
    radius = 3
    bonus = 10000

    def __init__(self, x, y, myCanvas):
        self.pos = vector.Vector(x,y)
        self.myCanvas = myCanvas

    def resetCanvas(self):
        self.arc = self.myCanvas.create_arc(self.getCoord(), start=0, extent=359.9, fill="red")

    def checkCollision(self, dot):
        dotPos = dot.getPosition()
        return (abs(self.pos.getX()-dotPos.getX()) < 5 and 
                abs(self.pos.getY()-dotPos.getY()) < 5)

    def getCoord(self):
        x = self.pos.getX()
        y = self.pos.getY()
        return x-self.radius, y+self.radius, x+self.radius, y-self.radius

    def getPosition(self):
        return self.pos

    def getBonus(self):
        return self.bonus