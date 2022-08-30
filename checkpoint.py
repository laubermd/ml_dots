class Checkpoint:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    bonus = 0

    def __init__(self, x1, y1, x2, y2, bonus, showCheckpoint, myCanvas):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.bonus = bonus
        self.myCanvas = myCanvas
        if showCheckpoint:
            self.resetCanvas()

    def resetCanvas(self):
        self.rectangle = self.myCanvas.create_rectangle((self.x1, self.y1, self.x2, self.y2), fill="teal")

    def getBonus(self):
        return self.bonus

    def checkCollision(self, dot):
        pos = dot.getPosition()
        return ((pos.getX() + dot.getRadius() > self.x1 and pos.getX() - dot.getRadius() < self.x2) and
                (pos.getY() + dot.getRadius() > self.y1 and pos.getY() - dot.getRadius() < self.y2))