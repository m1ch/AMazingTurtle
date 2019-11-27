# %%
import turtle

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
    for _ in range(4):
        t.forward(len)           
        t.left(90)
    t.end_fill()

def draw_maze(t, maze, edge_len, dim):
    t.clear()
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
    y = int(-edge_len*dim[0]/2 + pos[1]*edge_len + edge_len/2)
    return x,y

def draw_path(t, bot, edge_len, dim, col="green", speed='normal'):
    t.clear()
    t.speed('fastest')
    t.color(col)
    t.pensize(3)
    t.shape('turtle')
    # t.resizemode("user")
    t.shapesize(2)
    t.showturtle()

    t.penup()

    path = bot.get_path()
    t.goto(calc_coord(path[0][0], edge_len, dim))
    t.pendown()
    t.speed(speed)

    for (pos, dir) in path[1:]:
        t.setheading(dir*90)
        t.forward(edge_len)

# %%
dim=(100,100)
edge_len = 5
border = 10

try:
    type(turt)
except NameError:
    turt = turtle.Turtle()

turt.reset()
turt.screen.bgcolor("aqua")
turt.screen.title("A Mazing Turtle")
turt.screen.setup(width=edge_len*dim[0]+2*border, height=edge_len*dim[1]+2*border,
             startx=0, starty=0)
turt.hideturtle()
turt.penup()

try:
    type(backgr)
except NameError:
    backgr=turt.clone()

maze = None 
rbot = RefferenceBot()
while not rbot.target_found:
    maze = Maze(dimentions=dim)
    rbot.find_path(maze)
print("The reference path length is %d" % rbot.path_len)

draw_maze(backgr, maze, edge_len, dim)

try:
    type(refer)
except NameError:
    refer=turt.clone()


draw_path(refer, rbot, edge_len, dim, col="yellow")

bot=Bot()

try:
    type(runner)
except NameError:
    runner=turt.clone()

count = 0
scount = 0
while not bot.target_found:
    count+=1
    bot.find_path(maze)
    scount+=bot.path_len
    if not count%1000 or bot.path_len>rbot.path_len*3:
        print("try number %d, length %d" % (count, bot.path_len))
        draw_path(runner, bot, edge_len, dim, speed='fast')

draw_path(runner, bot, edge_len, dim)

print("The random path length is %d" % bot.path_len)
print("It took %d random tries and the average pathleng is %.2f" % \
    (count, scount/count ))

# %%
turtle.done()


# %%
