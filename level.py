from difficulty import Difficulty
import checkpoint
import goal
import obstacle
import population

class Level:

    def __init__(self, difficulty, dotCount, width, height, mutationRate, showCheckpoints, myCanvas):
        self.width,self.height = width,height
        self.myCanvas,self.showCheckpoints = myCanvas,showCheckpoints
        self.difficulty,self.dotCount = difficulty,dotCount
        self.obstacles,self.checkpoints,self.population = [],[],population.Population(dotCount, width, height, mutationRate, myCanvas)
        self.resetCanvas()
        myCanvas.pack()

    def resetCanvas(self):
        self.myCanvas.delete('all')

        match self.difficulty:
            case Difficulty.EASY:
                self.startEasyLevel()
            case Difficulty.MEDIUM:
                self.startMediumLevel()
            case Difficulty.HARD:
                self.startHardLevel()
            case Difficulty.MAZE:
                self.startMazeLevel()
        
        if self.showCheckpoints:
            for checkpoint in self.checkpoints:
                checkpoint.resetCanvas()

        for obstacle in self.obstacles:
            obstacle.resetCanvas()

        self.goal.resetCanvas()
        self.population.resetCanvas()

    def startEasyLevel(self):
        self.obstacles = []
        self.checkpoints = []
        self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    # TODO make obstacles relative to width/height
    def startMediumLevel(self):
        self.obstacles = [
            obstacle.Obstacle(200,247,300,252, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,247,500,252,5,self.showCheckpoints,self.myCanvas)
        ]

        self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    def startHardLevel(self):
        self.obstacles = [
            obstacle.Obstacle(150,397,350,402, self.myCanvas),
            obstacle.Obstacle(150,97,350,102, self.myCanvas),
            obstacle.Obstacle(25,247,200,252, self.myCanvas),
            obstacle.Obstacle(300,247,475,252, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,397,500,402,5,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(0,97,500,102,15,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(0,247,500,252,10,self.showCheckpoints,self.myCanvas)
        ]

        self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    def startMazeLevel(self):
        self.obstacles = [
            obstacle.Obstacle(0,397,350,402, self.myCanvas),
            obstacle.Obstacle(150,247,500,252, self.myCanvas),
            obstacle.Obstacle(150,97,350,102, self.myCanvas),
            obstacle.Obstacle(150,0,155,102, self.myCanvas)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(350,397,500,402,10,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(345,247,350,397,20,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(0,247,150,252,30,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(150,102,155,252,40,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(345,97,350,252,50,self.showCheckpoints,self.myCanvas),
            checkpoint.Checkpoint(350,97,500,102,60,self.showCheckpoints,self.myCanvas)
        ]

        self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    # TODO improve fitness scoring
    def calculateFitness(self, dot):
        fitness = 0
        if (dot.getReachedGoal()):
            fitness = dot.getBonus()/(dot.getStepCount()**2)
        else:
            pos = dot.getPosition()
            goalPos = self.goal.getPosition()
            xDistance = goalPos.getX() - pos.getX()
            yDistance = goalPos.getY() - pos.getY()
            distanceSq = xDistance**2 + yDistance**2
            fitness = dot.getBonus()/distanceSq
        dot.setFitness(fitness)

    def checkCollision(self, dot):
        collision = False
        radius = dot.getRadius()
        pos = dot.getPosition()
        xPos = pos.getX()
        yPos = pos.getY() 
        collision = (xPos < radius or yPos < radius or 
                    xPos > self.width - radius or 
                    yPos > self.height - radius)

        for obstacle in self.obstacles:
            collision = collision or obstacle.checkCollision(dot)

        for checkpoint in self.checkpoints:
            if checkpoint.checkCollision(dot):
                dot.setBonus(checkpoint.getBonus())

        if self.goal.checkCollision(dot):
            dot.setReachedGoal(True)
            dot.setBonus(self.goal.getBonus())
            collision = True

        if collision:
            dot.unalive()
            self.calculateFitness(dot)

    def movePopulation(self):
        if self.population.areAllDotsDead():
            self.population.naturalSelection()
            self.population.setAllDotsDead(False)
            self.population.mutateGeneration()
            self.resetCanvas()
        else:
            allDotsDead = True # trust, but verify
            allDots = self.population.getDots()
            for dotIndex in range(0, len(allDots)):
                if allDots[dotIndex].isAlive():
                    allDotsDead = False
                    self.population.move(dotIndex)
                    pos = allDots[dotIndex].getPosition()
                    xPos = pos.getX()
                    yPos = pos.getY()
                    self.checkCollision(allDots[dotIndex])                        
            if (allDotsDead):
                self.population.setAllDotsDead(True)