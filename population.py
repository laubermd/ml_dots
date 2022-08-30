import dot
import vector
import random

class Population:
    dots = []
    fitnessSum=0
    generation=1
    bestDot=0
    minStep=1000
    allDotsDead = False
    width = 0
    height = 0
    # myCanvas=None
    # arcs=None

    def __init__(self, size, width, height):
        self.width = width
        self.height = height
        self.dots = [dot.Dot(vector.Vector(x=self.width/2, y=self.height-10)) for _ in range(size)]
        # self.myCanvas = myCanvas
        # self.arcs = [self.myCanvas.create_arc(self.getStartCoord(), start=0, extent=359.9, fill="black") for _ in range(size)]


    def getStartCoord(self):
        return self.dots[0].getCoord()

    def getDots(self):
        return self.dots

    def setAllDotsDead(self, allDotsDead):
        self.allDotsDead = allDotsDead

    def areAllDotsDead(self):
        return self.allDotsDead

    def calculateFitnessSum(self):
        fitnessSum = 0
        for dot in self.dots:
            fitnessSum += dot.getFitness()

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

    def naturalSelection(self):
        newDots = [dot.Dot(vector.Vector(x=self.width/2, y=self.height-10)) for _ in range(len(self.dots))]
        self.setBestDot()
        self.calculateFitnessSum()

        newDots[0] = self.dots[self.bestDot].clone(vector.Vector(x=self.width/2, y=self.height-10))
        newDots[0].setBestDot(True)

        for index in range(1, len(newDots)):
            parent = self.selectParent()
            newDots[index] = parent.clone(vector.Vector(x=self.width/2, y=self.height-10))

        self.generation+=1
        self.dots = newDots.copy()

    def mutateGeneration(self):
        for dot in self.dots:
            if not dot.isBestDot():
                dot.mutate()
