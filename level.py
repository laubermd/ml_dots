from difficulty import Difficulty
import checkpoint
import goal
import radar
import vector
import math
import neat
import obstacle
import population
import pygame

class Level:

    config_path = "./neat-config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    def __init__(self, difficulty, dotCount, width, height, mutationRate, showCheckpoints):
        self.width,self.height = width,height
        self.showCheckpoints = showCheckpoints
        self.difficulty,self.dotCount = difficulty,dotCount

                # Init game
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255,255,255))
        self.clock = pygame.time.Clock()
        # generation_font = pygame.font.SysFont("Arial", 70)
        # font = pygame.font.SysFont("Arial", 30)
        # map = pygame.image.load('map.png')

        self.obstacles,self.checkpoints,self.population = [],[],population.Population(dotCount, width, height, mutationRate, self.screen)







        self.resetScreen()



        # Add reporter for fancy statistical result
        # TODO reconcile p and population
        self.p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.p.add_reporter(stats)
        # self.p.run(self.movePopulation, self.size)
        winner = self.p.run(self.runDot, 100)




    def runDot(self, genomes, config):

        # Init NEAT
        self.nets = []
        self.genomes = genomes

        # TODO move to level/population
        
        self.population.reset()
        self.population.setAllDotsDead(False)
        for id, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            dot = self.population.addDot()
            self.checkCollision(dot)
            self.nets.append(net)
            g.fitness = 0
        
        # Main loop
        while not self.population.areAllDotsDead():
            self.movePopulation()



    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.drawLevel()

    def resetScreen(self):
        self.drawLevel()
        self.goal.resetScreen()
        self.population.resetScreen()

    def drawLevel(self):
        match self.difficulty:
            case Difficulty.EASY:
                self.startEasyLevel()
            case Difficulty.MEDIUM:
                self.startMediumLevel()
            case Difficulty.HARD:
                self.startHardLevel()
            case Difficulty.MAZE:
                self.startMazeLevel()
            case Difficulty.EZAM:
                self.startEzamLevel()
        
        if self.showCheckpoints:
            for checkpoint in self.checkpoints:
                checkpoint.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

    def startEasyLevel(self):
        self.obstacles = []
        self.checkpoints = []
        self.goal = goal.Goal(self.width/2,10,self.screen)

    # TODO make obstacles relative to width/height
    def startMediumLevel(self):
        self.obstacles = [
            obstacle.Obstacle(200,247,300,252, self.screen)
        ]

        self.checkpoints = [
            checkpoint.Checkpoint(0,247,500,252,5,self.showCheckpoints,self.screen)
        ]

        self.goal = goal.Goal(self.width/2,10,self.screen)

    def startHardLevel(self):
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

        self.goal = goal.Goal(self.width/2,10,self.screen)

    def startMazeLevel(self):
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

        self.goal = goal.Goal(self.width/2,10,self.screen)

    def startEzamLevel(self):
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

        self.goal = goal.Goal(self.width/2,10,self.screen)

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

        radars = dot.getRadars()
        for myRadar in dot.getRadars():
            self.checkRadar(dot, myRadar)

    # TODO move some logic to radar object
    def checkRadar(self, dot, myRadar):
        len = 0
        xPos = int(dot.getPosition().getX())
        yPos = int(dot.getPosition().getY())

        x=xPos
        y=yPos
        while not self.checkRadarCollision(x,y) and len < 30:
            # extends radar line until white is detected
            len = len + 1
            x = int(xPos + math.cos(math.radians(360 - (myRadar.getAngle()))) * len)
            y = int(yPos + math.sin(math.radians(360 - (myRadar.getAngle()))) * len)

        pos = vector.Vector(x,y)
        dist = int(math.sqrt(math.pow(x - xPos, 2) + math.pow(y - yPos, 2)))
        myRadar.setCenter(dot.getPosition())
        myRadar.setDist(dist)
        myRadar.setPosition(pos)

    def checkRadarCollision(self, xPos, yPos):
        collision = False
        radius = 0
        collision = (xPos < radius or yPos < radius or 
                    xPos > self.width - radius or 
                    yPos > self.height - radius)

        for obstacle in self.obstacles:
            collision = collision or obstacle.checkRadarCollision(xPos,yPos)

        return collision

    def calculateReward(self, dot):
        reward = 0
        if (dot.getReachedGoal()):
            reward = dot.getBonus()/(dot.getStepCount())
        else:
            pos = dot.getPosition()
            goalPos = self.goal.getPosition()
            xDistance = goalPos.getX() - pos.getX()
            yDistance = goalPos.getY() - pos.getY()
            distanceSq = xDistance**2 + yDistance**2
            reward = 500 - math.sqrt(distanceSq) + dot.getBonus()
        return reward

    def movePopulation(self):
        self.clock.tick(50)
        pygame.display.update()
        self.screen.fill((255,255,255))
        self.goal.resetScreen()
        self.drawLevel()

        allDotsDead = True # trust, but verify
        allDots = self.population.getDots()
        for index, dot in enumerate(allDots):
            if dot.isAlive():
                allDotsDead = False
                netInput = dot.getData()
                netInput[4]=self.goal.getPosition().getX()-dot.getPosition().getX()
                netInput[5]=self.goal.getPosition().getY()-dot.getPosition().getY()
                output = self.nets[index].activate(netInput)
                step = vector.Vector(output[0],output[1])
                
                dot.move(step)
                pos = dot.getPosition()
                self.checkCollision(dot)
                self.genomes[index][1].fitness = self.calculateReward(dot)
            dot.resetScreen()
        if (allDotsDead):
            self.population.setAllDotsDead(True)
