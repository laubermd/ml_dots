import tkinter
from difficulty import Difficulty
import level
import population

root = tkinter.Tk()
width,height = 500,500
dotCount,mutationRate = 1000,.01
showCheckpoints = False
myCanvas = tkinter.Canvas(root, bg="white", height=height, width=width)
myLevel = level.Level(Difficulty.MAZE, dotCount, width, height, mutationRate, showCheckpoints, myCanvas)

def do_one_frame():
    myLevel.movePopulation()
    root.after(50, do_one_frame)

do_one_frame()
root.mainloop()