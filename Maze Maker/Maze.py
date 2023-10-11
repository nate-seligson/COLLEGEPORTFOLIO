from graphics import *
import math
import random
import sys
from time import sleep
sys.setrecursionlimit(5000)
win = GraphWin("THE GRAPH", 1440,800, False)
bottom = 100
right = 180
win.setCoords(0,bottom,right,0)
w = 5
# sqr object
class Sqr:
    def __init__(self, obj):
        self.walls = []
        self.uncovered = []
        self.obj = obj

#generate columns
columns = [[Sqr(Rectangle(Point(w * x, w * y), Point((w*x)+w, (w*y) + w))) for x in range(math.floor(right/w))] for y in reversed(range(math.floor(bottom/w)))]
for c in columns:
    for r in c:
        r.obj.draw(win)
#randomly set start and end
start = columns[random.randint(0,len(columns))][random.randint(0,len(columns[0]))]
end = columns[random.randint(0,len(columns))][random.randint(0,len(columns[0]))]
uncovered = []

#CREATE MAZE

#find all paths to go through
def findNeighbors(s):
    for c in columns:
        try:
            rowIndex = c.index(s)
            columnIndex = columns.index(c)
        except:
            continue
    neighbors = []
    for i in range(3):
        #go one to the left and one under, then ignore yourself, then one to the right and one up as possibilites
        currCol = columnIndex-1 + i
        currRow = rowIndex-1 + i
        if not (i == 1) and currRow >=0 and currCol >= 0:
            try:
                neighbors.append(columns[currCol][rowIndex])
                neighbors.append(columns[columnIndex][currRow])
            except:
                continue
    random.shuffle(neighbors)
    return neighbors
#determine walls
def buildWalls(prev, curr):
    # get previous square and current square, to build walls based on its relative position
    global w
    prms = [prev,curr]
    xs = [int(prev.obj.p1.x),int(curr.obj.p1.x)]
    ys = [int(prev.obj.p1.y),int(curr.obj.p1.y)]
    ps = [xs,ys]
    walls = []
    #start by building all walls and adding them to list
    for i in range(2):
        if prms[i].walls == []:
            l1 = Line(Point(xs[i], ys[i]), Point(xs[i], ys[i] + w))
            l2 = Line(Point(xs[i]+w, ys[i]), Point(xs[i]+w, ys[i]+w))
            l3 = Line(Point(xs[i], ys[i]), Point(xs[i]+w, ys[i]))
            l4 = Line(Point(xs[i], ys[i]+w), Point(xs[i]+w, ys[i] + w))
            li = [l1,l3,l2,l4]
            prms[i].walls = li
            for l in li:
                l.draw(win)
        else:
            li = prms[i].walls
        walls.append(li)
    #based on position, remove specific walls
    if xs[0] > xs[1]:
        s =[0,2]
    elif xs[0] < xs[1]:
        s = [2,0]
    elif ys[0] > ys[1]:
        s =[1,3]
    elif ys[0] < ys[1]:
        s = [3,1]
    walls[0][s[0]].undraw()
    walls[1][s[1]].undraw()
    #add to list for finding paths
    prev.uncovered.append(curr)
    curr.uncovered.append(prev)

#Generate maze recursively
def MakeMaze(s, checked = [], prev = None):
    global uncovered
    #stop if you are at a repeat square
    if s in checked:
        return
    checked.append(s)
    if prev is not None:
        buildWalls(prev, s)
        update()
    s.obj.setFill("white")
    s.obj.setOutline("white")
    #recurse for all neighbors
    for l in findNeighbors(s):
        if l not in checked:
            MakeMaze(l, checked, s)
    return checked

#MAZE SOLVER
    
#find all paths with no walls
def getPaths():
    covered = []
    paths = []
    paths.append([start])
    while True:
        for p in paths:
            #reset the grid to show purple square "moving"
            for s in p:
                if s != start and s != end:
                    s.obj.setFill("white")
            s = p[-1]
            #stop if at the end
            if s == end:
                s.obj.setFill("green")
                return p
            covered.append(s)
            p.append(s.uncovered[0])
            #duplicate if multiple paths
            if len(s.uncovered) > 1:
                for ss in s.uncovered[1:]:
                    if ss not in covered:
                        ss.obj.setFill("purple")
                        newp = p.copy()
                        newp.append(ss)
                        paths.append(newp)
                else:
                    paths.remove(p)
            update()
#Find all paths
def FindSolution(start):
    solution = getPaths()
##    for c in columns:
##        for r in c:
##            if r != start and r != end:
##                s.obj.setFill("white")
    for s in solution:
        s.obj.setFill("green")
        s.obj.setOutline("green")
        update()

#infinitely repeat for style points
while True:
    while True:
        try:
            start = columns[random.randint(0,len(columns))][random.randint(0,len(columns[0]))]
            end = columns[random.randint(0,len(columns))][random.randint(0,len(columns[0]))]
            break
        except:
            continue
    MakeMaze(start)
    start.obj.setFill("green")
    end.obj.setFill("red")
    win.postscript(file = "maze_unsolved.ps")
    update()
    FindSolution(start)
    win.postscript(file = "maze_solved.ps")


    #reset params and stuff
    win.close()
    win = GraphWin("THE GRAPH", 1440,800, False)
    bottom = 100
    right = 180
    win.setCoords(0,bottom,right,0)
    columns = [[Sqr(Rectangle(Point(w * x, w * y), Point((w*x)+w, (w*y) + w))) for x in range(math.floor(right/w))] for y in reversed(range(math.floor(bottom/w)))]
    for c in columns:
        for r in c:
            r.obj.draw(win)
    uncovered = []
