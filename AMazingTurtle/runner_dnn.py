# %%
import turtle
import tkinter as tk
# from tkinter import *

# %%
from maze import Maze
from bots import *
# %%

def draw_box(t, x, y, len=10, cor="black"):
    t.speed("fastest")
    t.hideturtle()
    t.penup()
    t.fillcolor(cor)
    t.goto(x,y)
    t.begin_fill()
    for i in range(4):
        t.forward(len)           
        t.left(90)
    t.end_fill()

def draw_maze(w, maze, edge_len, dim):
    w.clear()
    for cord in maze.obsticals:
        x = int(-edge_len*dim[0]/2 + cord[0]*edge_len)
        y = int(-edge_len*dim[1]/2 + cord[1]*edge_len)
        draw_box(t, x, y,len=edge_len)

    x = int(-edge_len*dim[0]/2 + maze.target[0]*edge_len)
    y = int(-edge_len*dim[1]/2 + maze.target[1]*edge_len)
    draw_box(t, x, y,len=edge_len, cor='red')

    x = int(-edge_len*dim[0]/2 + maze.start[0]*edge_len)
    y = int(-edge_len*dim[1]/2 + maze.start[1]*edge_len)
    draw_box(t, x, y,len=edge_len, cor='yellow')
# %%
def calc_coord(pos,edge_len,dim):
    x = int(-edge_len*dim[0]/2 + pos[0]*edge_len + edge_len/2)
    y = int(-edge_len*dim[1]/2 + pos[1]*edge_len + edge_len/2)
    return x,y

def draw_path(t, bot, edge_len, dim, col="green", speed='normal'):
    t.clear()
    t.speed('fastest')
    t.color(col)
    t.pensize(3)
    t.shape('turtle')
    # t.resizemode("user")
    t.shapesize(1)
    t.penup()

    path = bot.get_path()
    t.goto(calc_coord(path[0][0], edge_len, dim))
    t.showturtle()
    t.pendown()
    t.speed(speed)

    for (_, dir) in path[1:]:
        t.setheading(dir*90)
        t.forward(edge_len)

def calc_tk_coord(pos,edge_len,dim, border=0):
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

def draw_tk_maze(w, maze, edge_len, dim, border):
    width=edge_len*dim[0]+2*border
    height=edge_len*dim[1]+2*border
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

dim=(20,20)
edge_len = 30
border = 10

np.random.seed(0)

width=edge_len*dim[0]+2*border
height=edge_len*dim[1]+2*border
master = tk.Tk()
canvas = tk.Canvas(master, width=width, height=height)
canvas.pack()

maze = None 
rbot = RefferenceBot()
while not rbot.target_found:
    maze = Maze(dimentions=dim)
    rbot.find_path(maze)
print("The reference path length is %d" % rbot.path_len)

turt = turtle.RawTurtle(canvas)
turt.hideturtle()
turt.penup()

draw_tk_maze(canvas, maze, edge_len, dim, border)


refer=turt.clone()

draw_path(refer, rbot, edge_len, dim, col="blue")

while True:
    bot=DNNBot()
    runner=turt.clone()
    bot.find_path(maze)
    draw_path(runner, bot, edge_len, dim, speed='fast')
    if bot.target_found:
        break



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

print("The DNN path length is %d" % bot.path_len)


master.mainloop()
