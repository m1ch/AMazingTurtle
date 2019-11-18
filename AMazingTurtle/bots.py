# %%
# from array import *
import numpy as np
from random import randint
import numpy.matlib
from maze import Maze

# %%
class Bot:
    def __init__(self):
        self.target_found = False

    def angle_to_vector(self, ang):
        if ang == 0:
            return [1,0]
        elif ang == 90:
            return [0,1]
        elif ang == 180:
            return [-1,0]
        elif ang == 270:
            return [0,-1]

    def get_move(self):
        x = randint(0,2)
        if x == 0:
            val = -90
        elif x == 1:
            val = 0
        else:
            val = 90
        return(val)

    def get_new_pos(self):
        # mov = get_move()
        mov = randint(0,3) 
        dir = (self.pos[1]+mov)%4
        
        self.pos = ([x + y for x, y in zip(self.pos[0], \
                    ([1,0],[0,1],[-1,0],[0,-1])[dir])], \
                    dir)

    def find_path(self, maze=None):
        if maze is not None:
            self. maze = maze
        else:
            try:
                maze = self.maze
            except NameError:
                print("No maze given")

        # pos is a duplet from coordinates and the direction
        self.pos  = (maze.get_start(),0)

        self.path = [self.pos]
        self.target_found = False
        while True:
            self.get_new_pos()
            self.path.append(self.pos)

            f = maze.get_field(self.pos[0])
            if f == maze.obsticalVal:
                break

            if f == maze.targetVal:
                self.target_found = True
                break
        
        self.path_len=len(self.path)

    def get_path(self):
        return self.path
    
    def print_path(self):
        m = self.maze.maze()

        if self.path is None:
            return

        for f in self.path:
            c = f[0]
            x = self.maze.get_field(c)
            try:
                m[c[0]][c[1]] = 5
            except IndexError:
                1
        
        c = self.path[0][0]
        m[c[0]][c[1]] = 6
        c = self.path[-1][0]
        if self.target_found:
            try:
                m[c[0]][c[1]] = 7
            except IndexError:
                1
        else:
            try:
                m[c[0]][c[1]] = 8
            except IndexError:
                1

        for x in range(0,len(m)):
            s=""
            for y in range(0,len(m[0])):
                if m[x][y] == 0:
                    s+=" "
                elif m[x][y] == self.maze.obsticalVal:
                    s+="#"
                elif m[x][y] == self.maze.targetVal:
                    s+="T"
                elif m[x][y] == 5:
                    s+="."
                elif m[x][y] == 6:
                    s+="S"
                elif m[x][y] == 7:
                    s+="T"
                elif m[x][y] == 8:
                    s+="X"
            print(s)

class RefferenceBot(Bot):
    def __init__(self):
        super().__init__()


    def find_path(self, maze=None):
        if maze is not None:
            self.maze = maze
        else:
            try:
                maze = self.maze
            except NameError:
                print("No maze given")

        # pos is a duplet from coordinates and the direction
        self.pos  = (maze.get_start(),0)

        trace = [{'cord':self.pos[0],'dir':self.pos[1],'pred':None}]
        localBoard = maze.maze()
        self.target_found = False
        i = 0
        while i<len(trace):
            for x in (0,1,2,3):   
                c = np.array(trace[i]['cord']) + \
                        np.array(([1,0],[0,1],[-1,0],[0,-1])[x])
                if min(c)<0 or c[0]>maze.xDim-1 or c[1]>maze.yDim-1:
                    continue
                e = localBoard[c[0]][c[1]]
                if e == maze.obsticalVal:
                    continue
                localBoard[c[0]][c[1]] = maze.obsticalVal
                trace.append({'cord':list(c),'dir':x,'pred':i})
                if e == maze.targetVal:
                    self.target_found = True 
                    break
            if self.target_found:
                break
            i+=1
        
        if not self.target_found:
            self.path = None
            self.path_len=0
            return

        self.path = []
        i = len(trace)-1
        j=0
        while i != None:
            self.path.insert(0,(trace[i]['cord'], trace[i]['dir']))
            i = trace[i]['pred']
            j+=1

        self.path_len=len(self.path)

class DNNBot(Bot):
    def __init__(self):
        super().__init__()
        # define nn structure:
        self.x_size=3   # input neurons
        self.z1_size=6  # h1
        self.z2_size=6  # h2
        self.z3_size=4  # output
        # initialize random waights:
        self.w1=np.random.normal(-1,1,(self.x_size,self.z1_size))
        self.w2=np.random.normal(-1,1,(self.z1_size+1,self.z2_size))
        self.w3=np.random.normal(-1,1,(self.z2_size+1,self.z3_size))

    front_sight = 3
    side_sight = 3

    '''
    Sight: 
    ---V---
       |
       |
       |
    '''

    def get_sight(self):
        # returns the distance values to the next obsticle in front and 
        # on the sides. 
        # the distance is a value between -1 and 1 and is calculated like this
        # -1: an obsticle is one field away  >#
        # -1/max_sight*(max_sight-dist)...for obsticle     
        # ie. with a sight of 4:             0.75=>-#; 0.5=>--# 0.25=>---#
        # 0: nothing in sight                >----
        # 1: the target is one field away    >T
        # +1/max_sight*(max_sight-dist)...for target

        
        c = np.array(self.pos[0])
        d = self.pos[1]
        #front view
        d_ = np.array(([1,0],[0,1],[-1,0],[0,-1])[d])
        c_=c.copy()
        front=0
        for dist in range(0,self.front_sight):
            c_+=d_
            f = self.maze.get_field(tuple(c_))
            if not f:
                continue
            if f == self.maze.targetVal:
                front=1/self.front_sight*(self.front_sight-dist)
                break
            if f == self.maze.obsticalVal:
                front=-1/self.front_sight*(self.front_sight-dist)
                break
        #left:
        d_ = np.array(([0,1],[-1,0],[0,-1],[1,0])[d])
        c_=c.copy()
        left=0
        for dist in range(0,self.side_sight):
            c_+=d_
            f = self.maze.get_field(tuple(c_))
            if not f:
                continue
            if f == self.maze.targetVal:
                left=1/self.side_sight*(self.side_sight-dist)
                break
            if f == self.maze.obsticalVal:
                left=-1/self.side_sight*(self.side_sight-dist)
                break
        #right:
        d_ = np.array(([0,-1],[1,0],[0,1],[-1,0])[d])
        c_=c.copy()
        right=0
        for dist in range(0,self.side_sight):
            c_+=d_
            f = self.maze.get_field(tuple(c_))
            if not f:
                continue
            if f == self.maze.targetVal:
                right=1/self.side_sight*(self.side_sight-dist)
                break
            if f == self.maze.obsticalVal:
                right=-1/self.side_sight*(self.side_sight-dist)
                break
        self.sight = np.array([[front,left,right]])

    def calc_move(self,x):
        z2 = np.dot(x, self.w1)
        a2 = np.tanh(z2)
        ba2 = np.ones((x.shape[0], 1))
        a2 = np.concatenate((a2, ba2), axis=1)

        z3 = np.dot(a2, self.w2)
        a3 = np.tanh(z3)
        # we add the the 1 unit (bias) at the output of the second layer
        ba3 = np.ones((a3.shape[0], 1))
        a3 = np.concatenate((a3, ba3), axis=1)

        # output layer, prediction of our network
        z4 = np.dot(a3, self.w3)
        a4 = np.tanh(z4)

        r = []
        for a_ in a4:
            r.append(np.where(a_ == np.amax(a_))[0][0])
        return np.where(a_ == np.amax(a_))[0][0]

    def get_new_pos(self):
        # mov = get_move()
        self.get_sight()
        mov = self.calc_move(self.sight)
        dir = (self.pos[1]+mov)%4
        
        self.pos = ([x + y for x, y in zip(self.pos[0], \
                    ([1,0],[0,1],[-1,0],[0,-1])[dir])], \
                    dir)

    def find_path(self, maze=None):
        if maze is not None:
            self.maze = maze
        else:
            try:
                maze = self.maze
            except NameError:
                print("No maze given")
            except AttributeError:
                print("No maze given")

        # pos is a duplet from coordinates and the direction
        self.pos  = (maze.get_start(),0)

        self.path = [self.pos]
        self.target_found = False
        max_steps = maze.xDim*maze.yDim 
        while True:
            self.get_new_pos()
            self.path.append(self.pos)

            f = maze.get_field(self.pos[0])
            if f == maze.obsticalVal:
                break

            if f == maze.targetVal:
                self.target_found = True
                break
            max_steps-=1
            if not max_steps:
                break
        
        self.path_len=len(self.path)


if __name__ == "__main__":
    # test_maze=np.full((10,10), 0)
    # test_maze[5][5] = obstical
    # test_maze[9][9] = target
    # test_maze[0][0] = start

    test_maze=Maze(dimentions=(10,10))

    bot=Bot()
    bot=RefferenceBot()
    bot.find_path(test_maze)
    print(test_maze.maze())
    bot.print_path()
    
    bot2=DNNBot()
    bot2.find_path(test_maze)
    print(test_maze.maze())
    bot2.get_sight()
    print(bot2.sight)




# %%
