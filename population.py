import dot
import vector
import random

class Population:
    fitnessSum=0
    generation=1
    bestDot=0
    minStep=1000
    allDotsDead = False

    def __init__(self, size, width, height, screen):
        self.width,self.height,self.size = width,height,size
        self.dots = []
        self.screen = screen
        self.resetScreen()

    def addDot(self):
        newDot = dot.Dot(vector.Vector(x=self.width/2, y=self.height-10), self.screen)
        self.dots.append(newDot)
        return newDot

    def getDots(self):
        return self.dots

    def setAllDotsDead(self, allDotsDead):
        self.allDotsDead = allDotsDead

    def areAllDotsDead(self):
        return self.allDotsDead

    def setBestDot(self):
        topFitness = 0
        winnerIndex = 0
        for index in range(len(self.dots)):
            if self.dots[index].getFitness() > topFitness:
                topFitness = self.dots[index].getFitness()
                winnerIndex = index
        self.bestDot = winnerIndex
        self.dots[winnerIndex].setBestDot(True)

    def selectParent(self):
        randomFitness = random.uniform(0,self.fitnessSum)
        runningSum = 0
        for dot in self.dots:
            runningSum += dot.getFitness()
            if runningSum > randomFitness:
                return dot.clone(vector.Vector(x=self.width/2, y=self.height-10))
        print("error!!!!")
        return None

    def reset(self):
        self.dots = []
        self.allDotsDead = False
        # # self.setBestDot()
        # # self.calculateFitnessSum()

        # newDots[len(newDots)-1] = self.dots[self.bestDot].clone(vector.Vector(x=self.width/2, y=self.height-10))
        # newDots[len(newDots)-1].setBestDot(True)

        # for index in range(0, len(newDots)-1):
        #     parent = self.selectParent()
        #     newDots[index] = parent.clone(vector.Vector(x=self.width/2, y=self.height-10))

        self.generation+=1
        # self.dots = newDots.copy()

    def getGeneration(self):
        return self.generation

    def resetScreen(self):
        for dot in self.dots:
            dot.resetScreen()

    def move(self, dotIndex):
        self.dots[dotIndex].move()