import checkpoint
from difficulty import Difficulty
import goal
import obstacle

import math

class Level:

    def __init__(self, difficulty, screen, showCheckpoints):
        self.difficulty,self.screen, self.showCheckpoints = difficulty,screen,showCheckpoints
        match self.difficulty:
            case Difficulty.EASY:
                self.setupEasyLevel()
            case Difficulty.MEDIUM:
                self.setupMediumLevel()
            case Difficulty.HARD:
                self.setupHardLevel()
            case Difficulty.MAZE:
                self.setupMazeLevel()
            case Difficulty.EZAM:
                self.setupEzamLevel()

    def setupEasyLevel(self):
        self.obstacles = []
        self.checkpoints = []
        self.goal = goal.Goal(250,10,self.screen)

    def setupMediumLevel(self):
        self.obstacles = [
            obstacle.Obstacle(200,247,300,252, self.screen)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,247,500,252,5,self.showCheckpoints,self.screen)
        ]

        self.goal = goal.Goal(250,10,self.screen)

    def setupHardLevel(self):
        self.obstacles = [
            obstacle.Obstacle(150,397,350,402, self.screen),
            obstacle.Obstacle(150,97,350,102, self.screen),
            obstacle.Obstacle(25,247,200,252, self.screen),
            obstacle.Obstacle(300,247,475,252, self.screen)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,397,150,402,5,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(350,397,500,402,5,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(0,247,25,252,10,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(200,247,300,252,10,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(475,247,500,252,10,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(0,97,150,102,15,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(350,97,500,102,15,self.showCheckpoints,self.screen)
        ]

        self.goal = goal.Goal(250,10,self.screen)

    def setupMazeLevel(self):
        self.obstacles = [
            obstacle.Obstacle(0,397,350,402, self.screen),
            obstacle.Obstacle(150,247,500,252, self.screen),
            obstacle.Obstacle(150,97,350,102, self.screen),
            obstacle.Obstacle(150,0,155,102, self.screen)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(350,397,500,402,10,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(345,247,350,397,20,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(0,247,150,252,30,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(150,102,155,252,40,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(345,97,350,252,50,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(350,97,500,102,60,self.showCheckpoints,self.screen)
        ]

        self.goal = goal.Goal(250,10,self.screen)

    def setupEzamLevel(self):
        self.obstacles = [
            obstacle.Obstacle(150,397,500,402, self.screen),
            obstacle.Obstacle(0,247,350,252, self.screen),
            obstacle.Obstacle(150,97,350,102, self.screen),
            obstacle.Obstacle(345,0,350,102, self.screen)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,397,150,402,10,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(150,247,155,397,20,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(350,247,500,252,30,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(345,102,350,252,40,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(150,97,155,252,50,self.showCheckpoints,self.screen),
            checkpoint.Checkpoint(0,97,150,102,60,self.showCheckpoints,self.screen)
        ]

        self.goal = goal.Goal(250,10,self.screen)

    def draw(self):
        self.goal.draw()

        for checkpoint in self.checkpoints:
            checkpoint.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

    def checkCheckpointCollisions(self, dot):
        collision = False
        radius = dot.getRadius()
        pos = dot.getPosition()
        xPos = pos.getX()
        yPos = pos.getY()

        for checkpoint in self.checkpoints:
            if checkpoint.checkCollision(dot):
                dot.setBonus(checkpoint.getBonus())

        if self.goal.checkCollision(dot):
            dot.setReachedGoal(True)
            dot.setBonus(self.goal.getBonus())
            collision = True

        if collision:
            dot.unalive()

    def checkObsticalCollisions(self,xPos,yPos):
        radius = 2
        collision = (xPos < radius or yPos < radius or 
                    xPos > 500 - radius or 
                    yPos > 500 - radius)

        for obstacle in self.obstacles:
            collision = collision or obstacle.checkRadarCollision(xPos,yPos)

        return collision

    def getDistanceToGoal(self, dot):
        pos = dot.getPosition()
        goalPos = self.goal.getPosition()
        xDistance = goalPos.getX() - pos.getX()
        yDistance = goalPos.getY() - pos.getY()
        distanceSq = xDistance**2 + yDistance**2
        return math.sqrt(distanceSq)

    def getXToGoal(self, dot):
        return self.goal.getPosition().getX()-dot.getPosition().getX()

    def getYToGoal(self, dot):
        return self.goal.getPosition().getY()-dot.getPosition().getY()