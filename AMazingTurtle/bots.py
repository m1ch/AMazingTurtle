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
        
        self.path_len=len(self.path)-1

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
    
    def add_turtle(self, turtle, color='green'):
        self.turtle=turtle
        self.turtle.speed('fastest')
        self.turtle.color(color)
        self.turtle.pensize(3)
        self.turtle.shape('turtle')
        # t.resizemode("user")
        self.turtle.shapesize(1)

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

        self.path_len=len(self.path)-1

class DNNBot(Bot):
    def random_dna(self):
        self.w=[
                np.random.normal(-1,1,(self.a_size[0],self.a_size[1]-1)),
                np.random.normal(-1,1,(self.a_size[1],self.a_size[2]-1)),
                np.random.normal(-1,1,(self.a_size[2],self.a_size[3]))
            ]

    def __init__(self, dna=None):
        super().__init__()
        # define nn structure:
        self.a_size=[4,7,7,4]
        self.dna_size=0
        for i in range(1,len(self.a_size)):
            if i < len(self.a_size)-1:
                self.dna_size+=self.a_size[i-1]*(self.a_size[i]-1)
            else:
                self.dna_size+=self.a_size[i-1]*self.a_size[i]

        if dna is None:
            # initialize random waights:
            self.random_dna()
        else:
            self.w = [None]*(len(self.a_size)-1)
            self.set_dna(dna)
        self.a=[None]*len(self.a_size)

    front_sight = 3
    side_sight = 3

    '''
    Sight: 
    ---V---
       |
       |
       |
    '''

    def get_dna(self):
        dna = []
        for w_ in self.w:
            dna+=list(w_.flatten())
        return np.array(dna)

    def set_dna(self, dna):
        if len(dna)!=self.dna_size:
            raise ValueError('The input vector is not the same size as the dna')
        
        offset=0
        a_s = self.a_size.copy()
        a_s[-1]+=1
        for i in range(1, len(a_s)):
            size=a_s[i-1]*(a_s[i]-1)
            self.w[i-1] = (dna[offset:offset+size]).reshape((a_s[i-1],a_s[i]-1))
            offset+=size
        
    def get_sight(self,direction,dist):
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
        d = self.pos[1]+direction
        d = np.array(([1,0],[0,1],[-1,0],[0,-1])[d%4])
        sight=0
        for di_ in range(0,dist):
            c+=d
            f = self.maze.get_field(tuple(c))
            if not f:
                continue
            if f == self.maze.targetVal:
                sight=1/dist*(dist-di_)
                break
            if f == self.maze.obsticalVal:
                sight=-1/dist*(dist-di_)
                break
        return sight

    def gen_input(self):
        self.a[0] = np.array([[
            self.get_sight(0, self.front_sight),
            self.get_sight(+1, self.side_sight),
            self.get_sight(-1, self.side_sight),
            -1+self.pos[1]*2/3]]) # use compass

    def calc_move(self):
        '''
        Return the relative direction of the next move.
        * 0...front
        * 1...left
        * 2...back
        * 3...right
        '''
        # DNN calculation:
        i = 1
        while True:
            # for i in range(1,len(self.a_size)):
            z = np.dot(self.a[i-1], self.w[i-1])
            # sigma function:
            self.a[i] = np.tanh(z)
            if i==len(self.a_size)-1:
                break
            # add the the 1 unit (bias) at the output
            ba = np.ones((self.a[i-1].shape[0], 1))
            self.a[i] = np.concatenate((self.a[i], ba), axis=1)
            i+=1

        # get highest output value
        r = []
        for a_ in self.a[-1]:
            r.append(np.where(a_ == np.amax(a_))[0][0])
        return np.where(a_ == np.amax(a_))[0][0]

    def get_new_pos(self):
        # mov = get_move()
        self.gen_input()
        mov = self.calc_move()
        dir = (self.pos[1]+mov)%4 # new absolute direction
        
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
        max_steps = maze.get_max_path_lenght()
        self.cost = 0.0
        visit=np.zeros((maze.xDim,maze.yDim),dtype=int)
        self.crashed=False
        while True:
            self.get_new_pos()
            self.path.append(self.pos)

            if self.path.count(self.pos)>1:
                # already did this step before. No escape possible
                break

            f = maze.get_field(self.pos[0])
            if f == maze.obsticalVal:
                self.crashed = True
                self.cost+=2
                break

            self.cost+=(visit[tuple(self.pos[0])]-1) / max_steps
            visit[tuple(self.pos[0])]+=1

            if f == maze.targetVal:
                self.target_found = True
                self.cost-=1
                break
            if self.cost>1:
                break
        
        self.path_len=len(self.path)-1

class Dna():
    def __init__(self, dna=None):
        pass

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
    print("dna", bot2.get_dna())
    bot2.find_path(test_maze)
    bot.print_path()
    bot2.print_path()
    dna = bot2.get_dna()
    bot2.set_dna(np.zeros_like(dna))
    bot2.find_path(test_maze)
    bot2.print_path()



    # print(test_maze.maze())
    # print(bot2.sight)




# %%
