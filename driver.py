import checkpoint
from difficulty import Difficulty
import goal
import level
import radar
import vector
import math
import neat
import obstacle
import population
import pygame

class Driver:

    config_path = "./neat-config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    def __init__(self, difficulty, width, height, showCheckpoints):
        self.width,self.height = width,height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255,255,255))
        self.clock = pygame.time.Clock()
        self.population = population.Population(self.config.pop_size, width, height, self.screen)
        self.level = level.Level(difficulty, self.screen, showCheckpoints)

        # TODO reconcile p and population
        self.p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.p.add_reporter(stats)
        winner = self.p.run(self.runGeneration, 10)

        print('\nBest genome:\n{!s}'.format(winner))

        # node_names = {
        #     -1: 'E Rad',
        #     -2: 'N Rad',
        #     -3: 'W Rad',
        #     -4: 'S Rad',
        #     -5: 'X Dist',
        #     -6: 'Y Dist',
        #     0: 'Move X',
        #     1: 'Move Y'}
        # visualize.draw_net(self.config, winner, True, node_names=node_names)
        # # visualize.draw_net(self.config, winner, True, node_names=node_names, prune_unused=True)
        # visualize.plot_stats(stats, ylog=False, view=True)
        # visualize.plot_species(stats, view=True)

        # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
        # p.run(self.runGeneration, 10)

    def runGeneration(self, genomes, config):
        self.nets = []
        self.genomes = genomes
        self.population.reset()
        for id, g in genomes:
            self.population.addDot()
            self.nets.append(neat.nn.FeedForwardNetwork.create(g, config))
            g.fitness = 0

        while not self.population.areAllDotsDead():
            self.movePopulation()

    def checkCollision(self, dot):
        collision = self.level.checkObsticalCollisions(dot.getPosition().getX(),dot.getPosition().getY())
        if collision:
            dot.unalive()

        self.level.checkCheckpointCollisions(dot)

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
        while not self.level.checkObsticalCollisions(x,y) and len < 30:
            # extends radar line until white is detected
            len = len + 1
            x = int(xPos + math.cos(math.radians(360 - (myRadar.getAngle()))) * len)
            y = int(yPos + math.sin(math.radians(360 - (myRadar.getAngle()))) * len)

        pos = vector.Vector(x,y)
        dist = int(math.sqrt(math.pow(x - xPos, 2) + math.pow(y - yPos, 2)))
        myRadar.setCenter(dot.getPosition())
        myRadar.setDist(dist)
        myRadar.setPosition(pos)

    def calculateReward(self, dot):
        reward = 0
        if (dot.getReachedGoal()):
            reward = dot.getBonus()/(dot.getStepCount())
        else:
            reward = 500 - self.level.getDistanceToGoal(dot) + dot.getBonus()
        return reward

    def movePopulation(self):
        self.clock.tick(100)
        pygame.display.update()
        self.screen.fill((255,255,255))
        self.level.draw()

        allDotsDead = True # trust, but verify
        allDots = self.population.getDots()
        for index, dot in enumerate(allDots):
            if dot.isAlive():
                allDotsDead = False
                netInput = dot.getData()
                netInput[4]=self.level.getXToGoal(dot)
                netInput[5]=self.level.getYToGoal(dot)
                output = self.nets[index].activate(netInput)
                step = vector.Vector(output[0],output[1])
                dot.move(step)
                pos = dot.getPosition()
                self.checkCollision(dot)
                self.genomes[index][1].fitness = self.calculateReward(dot)
            dot.resetScreen()
        if (allDotsDead):
            self.population.setAllDotsDead(True)

if __name__ == "__main__":
    Driver(Difficulty.MEDIUM, 500, 500, False)