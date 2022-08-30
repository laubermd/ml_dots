class Vector:

    def __init__(self, x=0, y=0):
        self.x,self.y = x,y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def add(self, vel):
        self.x += vel.x
        self.y += vel.y

    def limit(self, limit):
        self.x=min(self.x,limit)
        self.y=min(self.y,limit)
        self.x=max(self.x,limit*-1)
        self.y=max(self.y,limit*-1)