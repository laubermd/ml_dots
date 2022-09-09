# import tkinter
# from tkinter import *
from difficulty import Difficulty
import level
import population

# root = tkinter.Tk()
width,height = 500,500
dotCount,mutationRate = 30,.01
showCheckpoints = False
# myCanvas = tkinter.Canvas(root, bg="white", height=height, width=width)
myLevel = level.Level(Difficulty.EASY, dotCount, width, height, mutationRate, showCheckpoints)

# easyButton = Button(myCanvas, text="Easy", command=lambda:myLevel.setDifficulty(Difficulty.EASY))
# mediumButton = Button(myCanvas, text="Medium", command=lambda:myLevel.setDifficulty(Difficulty.MEDIUM))
# hardButton = Button(myCanvas, text="Hard", command=lambda:myLevel.setDifficulty(Difficulty.HARD))
# mazeButton = Button(myCanvas, text="Maze", command=lambda:myLevel.setDifficulty(Difficulty.MAZE))
# ezamButton = Button(myCanvas, text="ezaM", command=lambda:myLevel.setDifficulty(Difficulty.EZAM))
# resetButton = Button(myCanvas, text="Reset", command=lambda:myLevel.resetBrains())

# easyButton.place(x=5, y=5)
# mediumButton.place(x=5, y=35)
# hardButton.place(x=5, y=65)
# mazeButton.place(x=5, y=95)
# ezamButton.place(x=5, y=125)
# resetButton.place(x=460, y=5)

# def do_one_frame():
#     myLevel.movePopulation()
#     root.after(50, do_one_frame)

# do_one_frame()
# root.mainloop()
