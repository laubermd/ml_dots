import tkinter
import dot
import vector

# init tk
root = tkinter.Tk()

width = 500
height = 500
startingPoint = vector.Vector(x=width/2, y=height)

# create canvas
myCanvas = tkinter.Canvas(root, bg="white", height=500, width=500)

# TODO make lots of dots
# TODO check if all dots alive
    # draw dot
    # TODO redraw dot and move
myDot = dot.Dot(startingPoint)
coord = myDot.getCoord()
arc = myCanvas.create_arc(coord, start=0, extent=359.9, fill="black")

def do_one_frame():
    # do whatever you need to draw one frame
    myDot.move()
    vel = myDot.getVelocity()
    print("move by: %f,%f" % (vel.getX(), vel.getY()))
    myCanvas.move(arc, vel.getX(), vel.getY())
    # coord = myDot.getCoord()
    # arc = myCanvas.create_arc(coord, start=0, extent=359.9, fill="black")
    # myDot.move()
    # if (self.myDot.isAlive()):
    root.after(100, do_one_frame)

# add to window and show
myCanvas.pack()

do_one_frame()
root.mainloop()

