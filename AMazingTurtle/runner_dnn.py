# %%
import turtle
import tkinter as tk
import time
import numpy as np
from random import randint
import os
# from tkinter import *

# %%
from maze import Maze
from bots import *
from gui import Gui

# %%
# def calc_coord(pos,edge_len,dim):
#     x = int(-edge_len*dim[0]/2 + pos[0]*edge_len + edge_len/2)
#     y = int(-edge_len*dim[1]/2 + pos[1]*edge_len + edge_len/2)
#     return x,y

# def draw_path(maze, bots, edge_len):
#     path=[]
#     max_path_len=0
#     for b_ in bots:
#         b_.turtle.penup()
#         p_=b_.get_path()
#         b_.turtle.goto(calc_coord(p_[0][0], edge_len, (maze.xDim,maze.yDim)))
#         b_.turtle.showturtle()
#         b_.turtle.pendown()
#         path.append(p_[1:])
#         max_path_len = max(b_.path_len,max_path_len)

#     i=0
#     while i<=max_path_len:
#         for j in range(len(bots)):
#             try:
#                 dir=path[j][i][1]
#             except IndexError:
#                 continue
#             bots[j].turtle.setheading(dir*90)
#             bots[j].turtle.forward(edge_len)
#         time.sleep(0.05)
#         i+=1
#     # for (_, dir) in path[1:]:
#     #     t.setheading(dir*90)
#     #     t.forward(edge_len)
#     # print("all done")

# def clean_path(bots):
#     for b_ in bots:
#         b_.turtle.clear()
#         b_.turtle.hideturtle()

# def calc_tk_coord(pos,edge_len, dim, border=0):
#     x_=pos[0]
#     y_=dim[1]-pos[1]

#     x = int(-dim[0]/2*edge_len + x_*edge_len + edge_len/2)
#     y = int(-dim[1]/2*edge_len + y_*edge_len - edge_len/2)
#     return x,y

# def draw_tk_box(w, x, y, len=10, cor="black"):
#     cx=int(x-len/2)
#     cx_=int(x+len/2)
#     cy=int(y-len/2)
#     cy_=int(y+len/2)
#     w.create_rectangle(cx, cy, cx_, cy_, fill=cor)

# def draw_tk_maze(w, maze, edge_len, border):
#     width=edge_len*maze.xDim+2*border
#     height=edge_len*maze.yDim+2*border
#     dim=(maze.xDim,maze.yDim)
#     xmax=int(width/2)
#     xmin=-xmax
#     ymax=int(height/2)
#     ymin=-ymax
#     w.create_line(xmin, int(ymin+border/2), xmax, \
#         int(ymin+border/2), fill="#7F7F7F", width=border)
#     w.create_line(xmin, int(ymax-border/2), xmax, \
#         int(ymax-border/2), fill="#7F7F7F", width=border)
#     w.create_line(int(xmin+border/2), ymin, \
#         int(xmin+border/2), ymax, fill="#7F7F7F", width=border)
#     w.create_line(int(xmax-border/2), ymin, \
#         int(xmax-border/2), ymax, fill="#7F7F7F", width=border)

#     for cord in maze.obsticals:
#         (x,y) = calc_tk_coord(cord, edge_len, dim, border)
#         draw_tk_box(w, x, y,len=edge_len)
#     (x,y) = calc_tk_coord(maze.target, edge_len, dim, border)
#     draw_tk_box(w, x, y,len=edge_len, cor='red')
#     (x,y) = calc_tk_coord(maze.start, edge_len, dim, border)
#     draw_tk_box(w, x, y,len=edge_len, cor='yellow')

def crossover(bot, cros=None, mutation=0.1):
    if cros is None:
        cros = [ 
            9, # cross first with next
            3, # cross second with
            1, # cross 
            1, # cross
            1  # add x new random bots
        ]  # The remaining will be random crossed
    
    finisher = {}
    survivor = {}
    died = {}
    for i in range( len(bot)):
        # if bot[i].cost in weights.keys():
        #     weights[bot[i].cost].append(bot[i])
        # else:
        #     weights[bot[i].cost]=[bot[i]]
        if bot[i].target_found:
            if bot[i].path_len in finisher.keys():
                finisher[bot[i].path_len].append(bot[i].get_dna())
            else:
                finisher[bot[i].path_len] = [bot[i].get_dna()]
        elif bot[i].crashed:
            if bot[i].path_len in died.keys():
                died[bot[i].path_len].append(bot[i].get_dna())
            else:
                died[bot[i].path_len] = [bot[i].get_dna()]
        else:
            if bot[i].path_len in survivor.keys():
                survivor[bot[i].path_len].append(bot[i].get_dna())
            else:
                survivor[bot[i].path_len] = [bot[i].get_dna()]
    dna = []

    # finisher with the shortes path
    for i in sorted(finisher):
        dna += finisher[i]

    # survivor with the longest path
    for i in list(reversed(sorted(survivor))):
        dna += survivor[i]

    # died after the longest path
    for i in list(reversed(sorted(died))):
        dna += died[i]

    setBot = 0
    for i in range(len(cros)-1):
        for j in range(i+1,cros[i]+i+1):
            # print("cross %i with %i" % (i,j))
            d0 = i
            d1 = j
            crosPoint = randint(0,bot[i].dna_size-1)
            if j%1:
                d = np.concatenate((dna[d0][:crosPoint],\
                                    dna[d1][crosPoint:]))
            else:
                d = np.concatenate((dna[d1][:crosPoint],\
                                    dna[d0][crosPoint:]))
            bot[setBot].set_dna(d)
            setBot+=1

    while setBot < len(bot)-cros[-1]:
        d0 = randint(0,len(dna)-1)
        d1 = randint(0,len(dna)-1)
        # print("cross %i with %i" % (d0,d1))
        crosPoint = randint(0,bot[i].dna_size-1)
        d = np.concatenate((dna[d0][:crosPoint],\
                            dna[d1][crosPoint:]))
        bot[setBot].set_dna(d)
        setBot += 1
    
    for i in range(len(bot)-cros[-1],len(bot)):
        bot[i].random_dna()
        # print("random %i" % (i))

    # mutation:
    for i in range( 0, len(bot)):
        d = bot[i].get_dna()
        for _ in range(int(bot[i].dna_size*mut_rate)):
            k = randint(0,bot[i].dna_size-1)
            d[k]+=d[k] * mut_rate * randint(-1,1)
        bot[i].set_dna(d)

dim=(30,30)
edge_len = 16
border = 10
seed=23

population=20 # number of bots per generation
mut_rate = 0.1 # mutation rate

if not "DISPLAY" in os.environ:
    enablePlot = False
else:
    enablePlot = True
    
plotN=100000

maze = None 
bot = [RefferenceBot()]
while not bot[0].target_found:
    maze = Maze(dimentions=dim)
    bot[0].find_path(maze)
maze.set_min_path_lenght(bot[0].path_len)
print("The reference path length is %d" % bot[0].path_len)

m=np.full(dim, 0)
# m[1][int(dim[1]/2)]=3
m[2][2]=3
m[int(dim[0]-3)][int(dim[1]/2)]=2
m[int(dim[0]/2)][int(dim[1]/2)]=1
maze = Maze(matrix=m)
bot[0].find_path(maze)

if enablePlot:
    gui = Gui((640,640))
    gui.draw_maze(maze)

try:
    bot[0].add_turtle(gui.turtle.clone(), color="blue")
except NameError:
    pass

target_count=0
target_bots=[]

np.random.seed(seed)

cor=[1.0,0.3,0.1]
for i in range( 1, population+1):
    bot.append(DNNBot())
    try:
        bot[i].add_turtle(gui.turtle.clone(),tuple(cor))
    except NameError:
        pass
    
    cor[1]+=0.03
    cor[0]-=0.03

dna = [None]*(population+1)
generation = 1
last_gen = 0
maze_tries = 0
maze_nr = 0
while True:
    survivor = []
    finisher = []
    uniquePath = []
    uniquePathBots = []
    weights={}
    time_start = time.process_time()
    time_cros = 0
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
        if not uniquePath.count(bot[i].get_path()):
            uniquePath.append(bot[i].get_path())
            uniquePathBots.append(bot[i])

    newMaze = False
    newPlot = False
    if len(finisher) > population/2:
        maze_tries = 0
        if generation > last_gen:
            newPlot = enablePlot
            last_gen = generation
        else:
            newPlot = False
        if maze_nr < dim[1]/2-3:
            maze.add_obstical((int(dim[0]/4),maze_nr))
            maze.add_obstical((int(dim[0]/4),dim[1]-1-maze_nr))
        elif maze_nr < 2*dim[1]/2 - (3+3):
            mn = maze_nr-(dim[1]/2-3)
            maze.add_obstical((int(dim[0]/2),mn))
            maze.add_obstical((int(dim[0]/2),dim[1]-1-mn))
        elif maze_nr < 3*dim[1]/2 - (3+3+2):
            mn = maze_nr-(2*dim[1]/2 - (3+3))
            maze.add_obstical((int(dim[0]*3/4),dim[1]/2+mn))
            maze.add_obstical((int(dim[0]*3/4),dim[1]/2-mn))
        elif maze_nr < 4*dim[1]/2 - (3+3+2+4):
            mn = maze_nr-(3*dim[1]/2 - (3+3+2))
            maze.add_obstical((int(dim[0]/2)+mn,dim[1]/2))
            maze.add_obstical((int(dim[0]/2)-mn,dim[1]/2))

        newMaze = enablePlot
        maze_nr += 1
    else:
        time_pre = time.process_time()
        crossover(bot[1:], cros=[9,3,1,1,1], mutation=0.3)
        time_cros = time.process_time() - time_pre
        generation+=1
        maze_tries += 1

    print("Maze %i/ Generation %i: %i bots survived and %i bots finished! " % \
        (maze_nr, generation, len(survivor), len(finisher)), \
        "(%i uniqu path found;" % (len(uniquePath)), 
        "Time round: %f, Time crossover: %f)" % (time.process_time()-time_start, time_cros))


    # if not maze_tries%plotN or newPlot:
    if newPlot:
        try:
            gui.clean_path(bot)
            gui.draw_path(uniquePathBots)
        except NameError:
            pass

    if newMaze:
        try:
            gui.draw_maze(maze)
        except NameError:
            pass




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


gui.master.mainloop()


# %%
