from difficulty import Difficulty
import obstacle

class Level:
    myCanvas=None
    obstacles=[]
    difficulty = Difficulty.EASY

    def __init__(self, difficulty, myCanvas):
        self.myCanvas = myCanvas
        self.difficulty = difficulty
        self.resetCanvas()

    def resetCanvas(self):
        match self.difficulty:
            case Difficulty.EASY:
                self.startEasyLevel()
            case Difficulty.MEDIUM:
                self.startMediumLevel()
            case Difficulty.HARD:
                self.startHardLevel()
        
        for obstacle in self.obstacles:
            obstacle.resetCanvas()

    def startEasyLevel(self):
        self.obstacles = []

    def startMediumLevel(self):
        self.obstacles = [
            obstacle.Obstacle(200,247,300,252, self.myCanvas)
        ]

    def startHardLevel(self):
        print("not implemented!")

    def checkCollision(self, dot):
        collision = False
        for obstacle in self.obstacles:
            collision = collision or obstacle.checkCollision(dot)
            
        return collision