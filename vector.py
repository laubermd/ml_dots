class Vector:
    x = 0
    y = 0

    def __init__(self, x=x, y=x):
        self.x = x
        self.y = y
        print("%f and %f" % (x, y))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def add(self, vel, limit=None):
        self.x += vel.x
        self.y += vel.y

        if limit:
            self.x=min(self.x,limit)
            self.y=min(self.y,limit)