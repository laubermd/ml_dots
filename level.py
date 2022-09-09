from difficulty import Difficulty
import checkpoint
import goal
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
        # self.myCanvas.pack()



        # Add reporter for fancy statistical result
        # TODO reconcile p and population
        self.p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.p.add_reporter(stats)
        # self.p.run(self.movePopulation, self.size)
        self.p.run(self.runDot, self.dotCount)



    def runDot(self, genomes, config):

        # Init NEAT
        self.nets = []
        self.genomes = genomes

        # TODO move to level/population
        for id, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net)
            g.fitness = 0

        # Main loop
        # generation += 1
        while True:
            self.movePopulation()



    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        # self.myCanvas.delete("checkpoint")
        # self.myCanvas.delete("obstacle")
        self.drawLevel()

    def resetScreen(self):
        # self.myCanvas.delete('all')
        self.drawLevel()
        self.goal.resetScreen()
        self.population.resetScreen()

    def resetBrains(self):
        self.population.resetBrains()
        # TODO only reset dots on canvas
        # self.resetCanvas()

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
                checkpoint.resetCanvas()

        for obstacle in self.obstacles:
            obstacle.resetCanvas()

    def startEasyLevel(self):
        self.obstacles = []
        self.checkpoints = []
        self.goal = goal.Goal(self.width/2,10,self.screen)

    # TODO make obstacles relative to width/height
    # def startMediumLevel(self):
    #     self.obstacles = [
    #         # obstacle.Obstacle(200,247,300,252, self.myCanvas)
    #     ]

    #     self.checkpoints = [
    #         # checkpoint.Checkpoint(0,247,500,252,5,self.showCheckpoints,self.myCanvas)
    #     ]

    #     # self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    # def startHardLevel(self):
    #     self.obstacles = [
    #         # obstacle.Obstacle(150,397,350,402, self.myCanvas),
    #         # obstacle.Obstacle(150,97,350,102, self.myCanvas),
    #         # obstacle.Obstacle(25,247,200,252, self.myCanvas),
    #         # obstacle.Obstacle(300,247,475,252, self.myCanvas)
    #     ]

    #     self.checkpoints = [
    #         # checkpoint.Checkpoint(0,397,500,402,5,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(0,97,500,102,15,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(0,247,500,252,10,self.showCheckpoints,self.myCanvas)
    #     ]

    #     # self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    # def startMazeLevel(self):
    #     self.obstacles = [
    #         # obstacle.Obstacle(0,397,350,402, self.myCanvas),
    #         # obstacle.Obstacle(150,247,500,252, self.myCanvas),
    #         # obstacle.Obstacle(150,97,350,102, self.myCanvas),
    #         # obstacle.Obstacle(150,0,155,102, self.myCanvas)
    #     ]

    #     self.checkpoints = [
    #         # checkpoint.Checkpoint(350,397,500,402,10,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(345,247,350,397,20,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(0,247,150,252,30,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(150,102,155,252,40,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(345,97,350,252,50,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(350,97,500,102,60,self.showCheckpoints,self.myCanvas)
    #     ]

    #     # self.goal = goal.Goal(self.width/2,10,self.myCanvas)

    # def startEzamLevel(self):
    #     self.obstacles = [
    #         # obstacle.Obstacle(150,397,500,402, self.myCanvas),
    #         # obstacle.Obstacle(0,247,350,252, self.myCanvas),
    #         # obstacle.Obstacle(150,97,350,102, self.myCanvas),
    #         # obstacle.Obstacle(345,0,350,102, self.myCanvas)
    #     ]

    #     self.checkpoints = [
    #         # checkpoint.Checkpoint(0,397,150,402,10,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(150,247,155,397,20,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(350,247,500,252,30,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(345,102,350,252,40,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(150,97,155,252,50,self.showCheckpoints,self.myCanvas),
    #         # checkpoint.Checkpoint(0,97,150,102,60,self.showCheckpoints,self.myCanvas)
    #     ]

    #     # self.goal = goal.Goal(self.width/2,10,self.myCanvas)

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
        pygame.display.update()
        self.screen.fill((255,255,255))
        self.goal.resetScreen()
        if self.population.areAllDotsDead():
            self.population.naturalSelection()
            self.population.setAllDotsDead(False)
            self.population.mutateGeneration()
            # self.resetCanvas()
        else:
            allDotsDead = True # trust, but verify
            allDots = self.population.getDots()

            for index, dot in enumerate(allDots):
                if dot.isAlive():
                    allDotsDead = False

                    print("index %i - len(nets) %i" % (index, len(self.nets)))
                    output = self.nets[index].activate(dot.getData())
                    i = output.index(max(output))
                    print("output.index(max(output)) %i" % i)
                    # TODO accelerate based on i
                    # if i == 0:
                    #     car.angle += 10
                    # else:
                    #     car.angle -= 10


                    dot.move()
                    pos = dot.getPosition()
                    self.checkCollision(dot)


                    # TODO update dot.checkRadar()
                    self.calculateFitness(dot)
                    self.genomes[i][1].fitness += dot.getFitness()
                dot.resetScreen()
            if (allDotsDead):
                self.population.setAllDotsDead(True)

        self.clock.tick(60)