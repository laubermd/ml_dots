import tkinter
import dot
from difficulty import Difficulty
import level
import population
import vector

# init tk
root = tkinter.Tk()

width = 500
height = 500
dotCount = 1000
reachedGoal = False
goalX = width/2
goalY = 10
goalCoord = goalX-3, goalY+3, goalX+3, goalY-3
# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=500, width=500)
population = population.Population(dotCount, width, height, myCanvas)
coord = population.getStartCoord()
myLevel = level.Level(Difficulty.MAZE, myCanvas)

# TODO move to a level object?
def calculateFitness(dot):
    fitness = 0
    if (dot.getReachedGoal()):
        # fitness better with fewer steps
        fitness = 10000/(dot.getStepCount()**2)
    else:
        pos = dot.getPosition()
        xDistance = goalX - pos.getX()
        yDistance = goalY - pos.getY()
        distanceSq = xDistance**2 + yDistance**2
        fitness = dot.getBonus()/distanceSq
    dot.setFitness(fitness)

def resetCanvas():
    myCanvas.delete('all')
    population.resetCanvas()
    myLevel.resetCanvas()
    goal = myCanvas.create_arc(goalCoord, start=0, extent=359.9, fill="red")

def do_one_frame():
    if population.areAllDotsDead():
        population.naturalSelection()
        population.setAllDotsDead(False)
        population.mutateGeneration()
        resetCanvas()
    else:
        allDotsDead = True # trust, but verify
        allDots = population.getDots()
        for dotIndex in range(0, len(allDots)):
            if allDots[dotIndex].isAlive():
                allDotsDead = False
                population.move(dotIndex)
                pos = allDots[dotIndex].getPosition()
                xPos = pos.getX()
                yPos = pos.getY()

                # TODO handle collisions in level class
                if (xPos<2 or yPos<2 or xPos>width-2 or yPos>height -2):
                    # dot hits the edge
                    allDots[dotIndex].unalive()
                    calculateFitness(allDots[dotIndex])
                elif (abs(goalX-xPos) < 5 and abs(goalY-yPos) < 5):
                    # dot reaches the goal
                    reachedGoal = True
                    allDots[dotIndex].setReachedGoal(True)
                    allDots[dotIndex].unalive()
                    calculateFitness(allDots[dotIndex])
                elif (myLevel.checkCollision(allDots[dotIndex])):
                    # kill the dot, but award points
                    allDots[dotIndex].unalive()
                    calculateFitness(allDots[dotIndex])
        if (allDotsDead):
            population.setAllDotsDead(True)
    root.after(50, do_one_frame)

# add to window and show
resetCanvas()
myCanvas.pack()
do_one_frame()
root.mainloop()