# %%
import turtle
import tkinter as tk
import time
import numpy as np
from random import randint
# from tkinter import *

# %%
from maze import Maze
from bots import *

# %%
def calc_coord(pos,edge_len,dim):
    x = int(-edge_len*dim[0]/2 + pos[0]*edge_len + edge_len/2)
    y = int(-edge_len*dim[1]/2 + pos[1]*edge_len + edge_len/2)
    return x,y

def draw_path(maze, bots, edge_len):
    path=[]
    max_path_len=0
    for b_ in bots:
        b_.turtle.clear()
        b_.turtle.penup()
        p_=b_.get_path()
        b_.turtle.goto(calc_coord(p_[0][0], edge_len, (maze.xDim,maze.yDim)))
        b_.turtle.showturtle()
        b_.turtle.pendown()
        path.append(p_[1:])
        max_path_len = max(b_.path_len,max_path_len)

    i=0
    while i<=max_path_len:
        for j in range(len(bots)):
            try:
                dir=path[j][i][1]
            except IndexError:
                continue
            bots[j].turtle.setheading(dir*90)
            bots[j].turtle.forward(edge_len)
        time.sleep(0.05)
        i+=1
    # for (_, dir) in path[1:]:
    #     t.setheading(dir*90)
    #     t.forward(edge_len)
    # print("all done")

def calc_tk_coord(pos,edge_len, dim, border=0):
    x_=pos[0]
    y_=dim[1]-pos[1]

    x = int(-dim[0]/2*edge_len + x_*edge_len + edge_len/2)
    y = int(-dim[1]/2*edge_len + y_*edge_len - edge_len/2)
    return x,y

def draw_tk_box(w, x, y, len=10, cor="black"):
    cx=int(x-len/2)
    cx_=int(x+len/2)
    cy=int(y-len/2)
    cy_=int(y+len/2)
    w.create_rectangle(cx, cy, cx_, cy_, fill=cor)

def draw_tk_maze(w, maze, edge_len, border):
    width=edge_len*maze.xDim+2*border
    height=edge_len*maze.yDim+2*border
    dim=(maze.xDim,maze.yDim)
    xmax=int(width/2)
    xmin=-xmax
    ymax=int(height/2)
    ymin=-ymax
    w.create_line(xmin, int(ymin+border/2), xmax, \
        int(ymin+border/2), fill="#7F7F7F", width=border)
    w.create_line(xmin, int(ymax-border/2), xmax, \
        int(ymax-border/2), fill="#7F7F7F", width=border)
    w.create_line(int(xmin+border/2), ymin, \
        int(xmin+border/2), ymax, fill="#7F7F7F", width=border)
    w.create_line(int(xmax-border/2), ymin, \
        int(xmax-border/2), ymax, fill="#7F7F7F", width=border)

    for cord in maze.obsticals:
        (x,y) = calc_tk_coord(cord, edge_len, dim, border)
        draw_tk_box(w, x, y,len=edge_len)
    (x,y) = calc_tk_coord(maze.target, edge_len, dim, border)
    draw_tk_box(w, x, y,len=edge_len, cor='red')
    (x,y) = calc_tk_coord(maze.start, edge_len, dim, border)
    draw_tk_box(w, x, y,len=edge_len, cor='yellow')

dim=(30,20)
edge_len = 16
border = 10
seed=42

population=20 # number of bots per generation
mut_rate = 0.1 # mutation rate

maze = None 
bot = [RefferenceBot()]
while not bot[0].target_found:
    maze = Maze(dimentions=dim)
    bot[0].find_path(maze)
maze.set_min_path_lenght(bot[0].path_len)
print("The reference path length is %d" % bot[0].path_len)

m=np.full(dim, 0)
m[1][int(dim[1]/2)]=3
m[int(dim[0]-1)][int(dim[1]/2)]=2
m[int(dim[0]/2)][int(dim[1]/2)]=1
maze = Maze(matrix=m)
bot[0].find_path(maze)


width=edge_len*maze.xDim+2*border
height=edge_len*maze.yDim+2*border
master = tk.Tk()
canvas = tk.Canvas(master, width=width, height=height)
canvas.pack()

turt = turtle.RawTurtle(canvas)
turt.hideturtle()
turt.penup()

draw_tk_maze(canvas, maze, edge_len, border)
time.sleep(1)

bot[0].add_turtle(turt.clone(), color="blue")

target_count=0
target_bots=[]

np.random.seed(seed)

cor=[1.0,0.3,0.1]
for i in range( 1, population+1):
    bot.append(DNNBot())
    bot[i].add_turtle(turt.clone(),tuple(cor))
    cor[1]+=0.03
    cor[0]-=0.03

dna = [None]*(population+1)
generation=0
while True:
    generation+=1
    survivor = []
    finisher = []
    weights={}
    for i in range( 1, population+1):
        bot[i].find_path(maze)
        if bot[i].cost in weights.keys():
            weights[bot[i].cost].append(bot[i])
        else:
            weights[bot[i].cost]=[bot[i]]
        if bot[i].target_found:
            # target_bots.append(bt[i])
            # target_count+=1
            survivor.append(i)
            finisher.append(i)
            # print("Bot %d costs %f, made %d steps and found the goal!" % (i,bot[i].cost,bot[i].path_len-1))
        elif bot[i].crashed:
            pass 
            # print("Bot %d costs %f, made %d steps and crshed!" % (i,bot[i].cost,bot[i].path_len-1))
        else:
            survivor.append(i)
            # print("Bot %d costs %f, made %d steps and dit not find the goal!" % (i,bot[i].cost,bot[i].path_len-1))
        dna[i] = bot[i].get_dna()

    print("in generation %i %i bots survived and %i bots finished!" % (generation, len(survivor), len(finisher)))
    # print([*weights])
    if not generation%10:
        draw_path(maze, bot, edge_len)

    crossover = finisher + survivor + finisher
    # print(survivor, finisher, crossover)
    for i in range( 1, population+1):
        x = randint(0,len(crossover)-1)
        y = randint(0,len(crossover)-1)
        z = randint(0,bot[i].dna_size-1)
        d = np.concatenate((dna[crossover[x]][:z],dna[crossover[y]][z:]))
        for j in range(int(bot[i].dna_size*mut_rate)):
            d[j]+=d[j]*mut_rate*randint(-1,1)
        bot[i].set_dna(d)

# random runner:
# bot=Bot()
# runner=turt.clone()



# count = 0
# scount = 0
# while not bot.target_found:
#     count+=1
#     bot.find_path(maze)
#     scount+=bot.path_len
#     if not count%1000 or bot.path_len>rbot.path_len*8:
#         # print("try number %d, length %d" % (count, bot.path_len))
#         draw_path(runner, bot, edge_len, dim, speed='fast')

# draw_path(runner, bot, edge_len, dim)

# print("The DNN path length is %d" % bot.path_len)


master.mainloop()


# %%
