from difficulty import Difficulty
import level
import population

width,height = 500,500
dotCount,mutationRate = 50,.01
showCheckpoints = True
myLevel = level.Level(Difficulty.MAZE, dotCount, width, height, mutationRate, showCheckpoints)
