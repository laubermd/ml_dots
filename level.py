from difficulty import Difficulty
import checkpoint
import obstacle

class Level:
    myCanvas=None
    obstacles=[]
    checkpoints=[]
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
            case Difficulty.MAZE:
                self.startMazeLevel()
        
        for obstacle in self.obstacles:
            obstacle.resetCanvas()

    def startEasyLevel(self):
        self.obstacles = []
        self.checkpoints = []

    def startMediumLevel(self):
        self.obstacles = [
            obstacle.Obstacle(200,247,300,252, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,252,500,253,5)
        ]

    def startHardLevel(self):
        self.obstacles = [
            obstacle.Obstacle(150,397,350,402, self.myCanvas),
            obstacle.Obstacle(150,97,350,102, self.myCanvas),
            obstacle.Obstacle(10,247,200,252, self.myCanvas),
            obstacle.Obstacle(300,247,490,252, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,402,500,403,5),
            checkpoint.Checkpoint(0,102,500,103,15),
            checkpoint.Checkpoint(0,252,500,253,10)
        ]

    def startMazeLevel(self):
        self.obstacles = [
            obstacle.Obstacle(0,397,350,402, self.myCanvas),
            obstacle.Obstacle(150,247,500,252, self.myCanvas),
            obstacle.Obstacle(150,97,350,102, self.myCanvas),
            obstacle.Obstacle(150,0,155,102, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(350,397,500,402,5),
            checkpoint.Checkpoint(0,247,150,252,10),
            checkpoint.Checkpoint(150,102,155,252,15),
            checkpoint.Checkpoint(350,97,500,102,20)
        ]

    def checkCollision(self, dot):
        collision = False
        for obstacle in self.obstacles:
            collision = collision or obstacle.checkCollision(dot)

        for checkpoint in self.checkpoints:
            if checkpoint.checkCollision(dot):
                dot.setBonus(checkpoint.getBonus())

        return collision