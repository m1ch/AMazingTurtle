# %%
from turtle import Turtle, Screen
from array import *
import numpy as np
from random import randint
import numpy.matlib

from AMazingTurtle.bots import *

dim=(50,50)
obstical = 1  # Black
target   = 2    # Red
start    = 3     # Yellow
edge_len = 10


# %%
def draw_box(x,y,len=10, cor="black"):
    t = Turtle()
    t.speed(10000)
    t.hideturtle()
    t.penup()
    t.fillcolor(cor)
    t.goto(x,y)
    t.begin_fill()
    t.goto(x+len,y)
    t.goto(x+len,y+len)
    t.goto(x,y+len)
    t.goto(x,y)
    t.end_fill()
# %%
if __name__ == "__main__":
    screen = Screen()
    screen.clear()
    screen.setup(width=300, height=300, startx=0, starty=0)
    draw_box(0,0)
    draw_box(20,0,30)
    draw_box(0,30,cor='red')

# %% calculate the next move

def get_move():
    x = randint(0,2)
    if x == 0:
        val = -90
    elif x == 1:
        val = 0
    else:
        val = 90
    return(val)

# %%
def angle_to_vector(ang):
    if ang == 0:
        return [1,0]
    elif ang == 90:
        return [0,1]
    elif ang == 180:
        return [-1,0]
    elif ang == 270:
        return [0,-1]

# %%
def get_new_pos(pos, dir):
    mov = get_move()
    dir = (dir+mov)%360
    pos = [x + y for x, y in zip(pos, angle_to_vector(dir))]

    return pos, dir


# %% 
def calc_coord(pos):
    x = -edge_len*dim[0]/2 + pos[0]*edge_len + edge_len/2
    y = -edge_len*dim[0]/2 + pos[1]*edge_len + edge_len/2
    return x,y


# %%


board=np.full(dim, 0)
board[1][3] = obstical
board[5][3] = obstical
board[6][3] = obstical
board[7][3] = obstical
board[8][3] = obstical
board[9][3] = obstical
board[18][18] = obstical
board[19][18] = obstical
board[20][18] = obstical
board[18][19] = obstical
board[18][20] = obstical
for i in range(0,34):
    board[15][i] = obstical

for i in range(25,45):
    board[i][25] = obstical
    board[i][35] = obstical



board[30][30] = target
board[0][0] = start

screen = Screen()
screen.clear()
screen.setup(width=edge_len*dim[0]+20, height=edge_len*dim[1]+20,
             startx=0, starty=0)

# draw obsticals
result = np.where(board==obstical)
listOfCoordinates= list(zip(result[0], result[1]))

for cord in listOfCoordinates:
    x = -edge_len*dim[0]/2 + cord[0]*edge_len
    y = -edge_len*dim[1]/2 + cord[1]*edge_len
    draw_box(x, y,len=edge_len)

# draw start and target
result = np.where(board==target)
listOfCoordinates= list(zip(result[0], result[1]))
if len(listOfCoordinates) == 1:
    x = -edge_len*dim[0]/2 + listOfCoordinates[0][0]*edge_len
    y = -edge_len*dim[1]/2 + listOfCoordinates[0][1]*edge_len
    draw_box(x, y,len=edge_len, cor='red')

result = np.where(board==start)
listOfCoordinates= list(zip(result[0], result[1]))
if len(listOfCoordinates) == 1:
    x = -edge_len*dim[0]/2 + listOfCoordinates[0][0]*edge_len
    y = -edge_len*dim[1]/2 + listOfCoordinates[0][1]*edge_len
    draw_box(x, y,len=edge_len, cor='yellow')

# %%
# draw obsticals

from AMazingTurtle.maze import Maze
# %%
dim=(10,10)
edge_len = 30
try:
    type(screen)
except NameError:
    screen = Screen()
screen.clear()
screen.setup(width=edge_len*dim[0]+20, height=edge_len*dim[1]+20,
             startx=0, starty=0)

maze = Maze(dimentions=dim)


result = np.where(board==obstical)
listOfCoordinates= list(zip(result[0], result[1]))

for cord in maze.obsticals:
    x = -edge_len*dim[0]/2 + cord[0]*edge_len
    y = -edge_len*dim[1]/2 + cord[1]*edge_len
    draw_box(x, y,len=edge_len)

x = -edge_len*dim[0]/2 + maze.target[0]*edge_len
y = -edge_len*dim[1]/2 + maze.target[1]*edge_len
draw_box(x, y,len=edge_len, cor='red')

x = -edge_len*dim[0]/2 + maze.start[0]*edge_len
y = -edge_len*dim[1]/2 + maze.start[1]*edge_len
draw_box(x, y,len=edge_len, cor='yellow')

# %%
from AMazingTurtle.bots import Bot
# %% 
bot=Bot()
bot.find_path(maze)

showPath = True
# %%
if showPath:
    # init the bot
    try:
        type(turt)
        
    except NameError:
        turt = Turtle()
    try:
        turt.reset()
    except TclError:
        1
    turt.speed(10000)
    turt.color('green')
    turt.pensize(3)
    turt.shape('classic')
    turt.penup()

    path = bot.get_path()
    turt.goto(calc_coord(path[0][0]))
    turt.pendown()
    turt.speed(10)

    for (pos, dir) in path[1:]:
        print(pos, dir)
        turt.setheading(dir*90)
        turt.forward(edge_len)

# %%
def find_random_path(board):
    i = 0
    botDir=0
    result = np.where(board==start)
    listOfCoordinates = list(zip(result[0], result[1]))
    botPos = listOfCoordinates[0]
    path = [(botPos, botDir)]
    victory = False
    while True:
        i+=1

        (botPos, botDir) = get_new_pos(botPos, botDir)
        path.append((botPos, botDir))

        if botPos[0] < 0 or botPos[1] < 0 or \
                botPos[0] > dim[0]-1 or botPos[1] > dim[1]-1:
            # print(botPos, botDir)
            ## print("Bot left the board after %d moves!!" % i)
            break

        curField = board[botPos[0]][botPos[1]]
        if  curField == target:
            print("Bot reached the goal in %d moves" % i)
            victory = True
            break

        elif curField == obstical:
            # print(botPos, botDir)
            ## print("Bot hit an obstical after %d moves!!" % i)
            break
    
    steps=i
    return steps, path, victory

# %%
def find_shortest_path(board):
    botDir=0
    
    result = np.where(board==start)
    listOfCoordinates = list(zip(result[0], result[1]))
    botPos = listOfCoordinates[0]

    maxX = board.shape[0]-1
    maxY = board.shape[1]-1

    trace = [{'cord':botPos,'dir':botDir,'pred':None}]

    localBoard=board.copy()
    victory = False
    i = 0
    while i<len(trace):
        #for x in ([1,0],[0,1],[-1,0],[0,-1]):
        for x in (0,90,180,270):   
            c = np.array(trace[i]['cord']) + np.array(angle_to_vector(x))
            if min(c)<0 or c[0]>maxX or c[1]>maxY:
                continue
            e = localBoard[c[0]][c[1]]
            if e == obstical:
                continue
            localBoard[c[0]][c[1]] = obstical
            trace.append({'cord':list(c),'dir':x,'pred':i})
            if e == target:
                victory=True 
                break
        if victory:
            break
        i+=1

    if not victory:
        return 0, [], False

    path = []
    i = len(trace)-1
    j=0
    while i != None:
        path.insert(0,(trace[i]['cord'], trace[i]['dir']))
        i = trace[i]['pred']
        j+=1

    return j, path, True

# %%
#single run:
showPath = True

from AMazingTurtle.bots import *


bot1=Bot()

# %%

# (steps, path, victory) = find_random_path(board)
(steps, path, victory) = find_shortest_path(board)

if showPath:
    # init the bot
    try:
        type(bot)
    except NameError:
        bot = Turtle()
    bot.reset()
    bot.speed(10000)
    bot.color('green')
    bot.pensize(3)
    bot.shape('classic')
    bot.penup()

    bot.goto(calc_coord(path[0][0]))
    bot.pendown()
    bot.speed(100)

    for (pos, dir) in path[1:]:
        print(pos, dir)
        bot.setheading(dir)
        bot.forward(edge_len)

# %%
victory = False
vcount = 0
scount = 0
showPath = True

while True:
    vcount+=1

    (steps, path, victory) = find_random_path(board)

    if showPath or victory:
        # init the bot
        try:
            type(bot)
        except NameError:
            bot = Turtle()
        bot.reset()
        bot.speed(10000)
        bot.color('green')
        bot.pensize(3)
        bot.shape('classic')
        bot.penup()

        bot.goto(calc_coord(path[0][0]))
        bot.pendown()
        bot.speed(100)

        for (pos, dir) in path[1:]:
            bot.setheading(dir)
            bot.forward(edge_len)

    if vcount%1000:
        showPath = False
    else:
        #print(vcount)
        showPath = True

    if victory:
        print("Victorious after %d tries" % vcount)
        astep=scount/vcount
        print("Average steps done: %f" % astep)
        break



# %%

one = np.array((1,0))

tilt = np.array((0,1))
one*tilt

# %%
dir = (0 + 1j)


# %%

bot = turtle.Turtle(-100,100)
bot.goto(-100, -100)
bot.color('red')
bot.pensize(3)
bot.shape('classic')

bot.forward(200)
bot.left(20)
bot.forward(200)


# %%



# %%
turtle.bye() 


# %%
from turtle import *

pensize(25)
speed(200)

colormode(255)
for i in range(36):
    if i > 30:
        color("lightgrey")
    elif i > 25:
        color("pink")
    elif i > 20:
        color("violet")
    elif i > 15:
        color("purple")
    elif i > 10:
        color("blue")
    elif i > 5:
        color("turquoise")
    else:
        color("lightblue")
    fd(150)
    bk(150)
    lt(10)
bye()

