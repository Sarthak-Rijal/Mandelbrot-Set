# Visualization of Mandelbrot equation iterations in the complex plane.

# This program plots the iterations of the function f(z) = z*z + c.

# Note: (The x-axis is flipped but I haven't gotten around to fixing
# it yet.)

import math as ma
import matplotlib.pyplot as plt
import numpy as np
import pygame as pg

# Adjust window size.
wScreen = 1200
hScreen = 900

# Color values
white = (255, 255, 255)
gray = (100, 100, 100)

# Adjust dimensions of x and y axis. (Must be int)
# You can play around with this. I find 2 and 2 or 1 and 1 works best.
xDim = 1
yDim = 1

# Radius of data point circles.
radius = 5

# Adjusts the c value of the equation.
# Play around with different constants to see if you
# can make different patterns.
# constant = complex(-0.7, 0.09) gives 
# constant = complex (-0.4,0.4) is cool too.
constant = complex(-0.2,0.3)



# Allocating iterations list for faster run.
numIter = 800
iterations = np.arange(numIter)


# Ignore. (Stuff for matplotlib)
#x = np.arange(-xDim,xDim)
#y = np.arange(-yDim, yDim)
#XX,YY = np.meshgrid(x,y)

        
win = pg.display.set_mode((wScreen, hScreen))

# Class defining attributes of f(z).
class zed(object):

    def __init__(self, rCoord, jCoord, radius, color):
        self.rCoord = rCoord
        self.jCoord = jCoord
        self.radius = radius
        self.color = color

    def drawZed(self, win):
        self.x = int(wScreen/2 - ((wScreen/2)/xDim)*self.rCoord)
        self.y = int(hScreen/2 - ((hScreen/2)/yDim)*self.jCoord)
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def iterateZed(self, z, co):
        self.z = complex(self.rCoord,self.jCoord)
        self.fz = z**2 + co
        self.z = self.fz
        iterations.append(self.z)
        if (len(iterations) < numIter and ma.hypot(self.z.real,self.z.imag) < 1000000):
            self.iterateZed(self.z, co)

# Draws points and lines to iterations of initial z value.
def drawIter(win, iterations, zed):
    coord = getCoord(zed.rCoord,zed.jCoord)
    for i in range(numIter):
        try:
            lastCoord = coord
            real = iterations[i].real
            imag = iterations[i].imag
            coord = getCoord(real, imag)
            pg.draw.circle(win, white, coord, radius)
            pg.draw.line(win, white, lastCoord, coord)
        except:
            break

# Draw unit grid.
def drawGrid(win):
    pg.draw.line(win, gray, getCoord(0,-yDim), getCoord(0,yDim), 3)
    pg.draw.line(win, gray, getCoord(-xDim,0), getCoord(xDim,0), 3)

    for i in range(xDim):
        pg.draw.line(win, gray, getCoord(i,-yDim), getCoord(i, yDim))
        pg.draw.line(win, gray, getCoord(-i,-yDim), getCoord(-i, yDim))
    for i in range(yDim):
        pg.draw.line(win, gray, getCoord(-xDim,i), getCoord(xDim, i))
        pg.draw.line(win, gray, getCoord(-xDim,-i), getCoord(xDim, -i))

# Translates traditional (x,y) coordinates to screen coordinates for pygame.
def getCoord(xCoord,yCoord):
    x = ((wScreen/2) - ((wScreen/2)/xDim)*xCoord)
    y = (hScreen/2) - ((hScreen/2)/yDim)*yCoord
    #x = ma.floor(x)
    #y = ma.floor(y)
    x = int(x)
    y = int (y)
    coord = (x, y)
    return coord



    
# Creating zed object.
ZZ = zed(0,0,radius, white)

# Run loop.
run = True
while run:
    iterations = []
    mousePos = pg.mouse.get_pos()
    #ZZ.rCoord = xDim*(1-(2*mousePos[0])/wScreen)
    #ZZ.jCoord = yDim*(1-(2*mousePos[1])/hScreen)
    x = xDim*(1-(2*mousePos[0])/wScreen)
    y = yDim*(1-(2*mousePos[1])/hScreen)
    ZZ.iterateZed(complex(ZZ.rCoord, ZZ.jCoord), complex(x,y))
    win.fill((0,0,50))
    drawGrid(win)
    ZZ.drawZed(win)
    drawIter(win,iterations, ZZ)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

pg.quit()
