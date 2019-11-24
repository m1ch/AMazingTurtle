import tkinter as tk
import turtle
import time
from bots import *
from maze import Maze

class Gui():
    def __init__(self, dim, border=20):
        self.dim = dim
        # self.edgeLen = edgeLen
        self.border = border
        self.width = dim[0] # edgeLen*maze.xDim+2*border
        self.height= dim[1] # edgeLen*maze.yDim+2*border
        self.master = tk.Tk()
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.turtle = turtle.RawTurtle(self.canvas)
        self.turtle.hideturtle()
        self.turtle.penup()
        self.xmax=int(self.width/2-self.border)
        self.xmin=-self.xmax
        self.ymax=int(self.height/2-self.border)
        self.ymin=-self.ymax

    def draw_maze(self, maze):
        self.maze = maze
        self.xDim = maze.xDim
        self.yDim = maze.yDim
        self.edgeLen = (
            (self.xmax-self.xmin)/self.xDim, \
            (self.ymax-self.ymin)/self.yDim
        )

        self.canvas.create_line(self.xmin, self.ymin-self.border/2, \
                                self.xmax, self.ymin-self.border/2, \
                                fill="#7F7F7F", width=self.border)
        self.canvas.create_line(self.xmin, self.ymax+self.border/2, \
                                self.xmax, self.ymax+self.border/2, \
                                fill="#7F7F7F", width=self.border)
        self.canvas.create_line(self.xmin-self.border/2, self.ymin, \
                                self.xmin-self.border/2, self.ymax, \
                                fill="#7F7F7F", width=self.border)
        self.canvas.create_line(self.xmax+self.border/2, self.ymin, \
                                self.xmax+self.border/2, self.ymax, \
                                fill="#7F7F7F", width=self.border)
        self.canvas.create_rectangle(self.xmin, self.ymin, \
                                     self.xmin+self.edgeLen[0]*self.xDim, \
                                     self.ymin+self.edgeLen[1]*self.yDim, fill="#003333")

        for coord in maze.obsticals:
            self.draw_box(coord)
        self.draw_box(maze.target, cor='red')
        self.draw_box(maze.start, cor='yellow')

    def calc_coord(self, pos):
        x_=pos[0]
        y_=pos[1]
        x = self.xmin + x_*self.edgeLen[0] + self.edgeLen[0]/2
        y = self.ymin + y_*self.edgeLen[1] + self.edgeLen[1]/2
        return x,y

    def draw_box(self, coord, cor="black"):
        (x,y) = self.calc_coord(coord)
        cx=int(x-self.edgeLen[0]/2)
        cx_=int(x+self.edgeLen[0]/2)
        cy=int(-y-self.edgeLen[1]/2)
        cy_=int(-y+self.edgeLen[1]/2)
        self.canvas.create_rectangle(cx, cy, cx_, cy_, fill=cor)

    def draw_path(self, bots):
        path=[]
        max_path_len=0
        for b_ in bots:
            b_.turtle.penup()
            p_=b_.get_path()
            b_.turtle.goto(self.calc_coord(p_[0][0]))
            b_.turtle.showturtle()
            b_.turtle.pendown()
            path.append(p_[1:])
            max_path_len = max(b_.path_len,max_path_len)

        i=0
        while i<=max_path_len:
            for j in range(len(bots)):
                try:
                    dir=path[j][i][1]
                    coord=path[j][i][0]
                except IndexError:
                    continue
                bots[j].turtle.setheading(dir*90)
                bots[j].turtle.goto(self.calc_coord(coord))
                # bots[j].turtle.forward(self.edgeLen)
            time.sleep(0.05)
            i+=1
        # for (_, dir) in path[1:]:
        #     t.setheading(dir*90)
        #     t.forward(edge_len)
        # print("all done")

    def clean_path(self, bots):
        for b_ in bots:
            b_.turtle.clear()
            b_.turtle.hideturtle()


if __name__ == "__main__":
    pass
