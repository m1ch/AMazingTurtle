# %%
#from array import *
import numpy as np
from random import randint
import numpy.matlib

# %%
class Maze():
    '''
    Add class description here
    '''

    obsticalVal = 1  # Black
    targetVal   = 2  # Red
    startVal    = 3  # Yellow

    def find_location(self, m, marker):
        result = np.where(m==marker)
        listOfCoordinates = list(zip(result[0], result[1]))
        return listOfCoordinates

    def check_maze(self):
        1

    def import_from_matrix(self, matrix):
        if matrix.min() < 0 or \
           matrix.max() > max(self.startVal, \
                              self.targetVal, \
                              self.obsticalVal):
            raise ValueError('The input matrix must only contain int from 0 to 3!')
        
        self.xDim=len(matrix)
        self.yDim=len(matrix[0])
        for r in matrix:
            if len(r) != self.yDim:
                raise IndexError('All rows must be the same size!')

        x=self.find_location(matrix, self.startVal)
        if len(x)==1:  
            self.start=x[0]
        else:
            raise ValueError('Exact one start is allowed')
        x=self.find_location(matrix, self.targetVal)
        if len(x)==1:
            self.target=x[0]
        else:
            raise ValueError('Exact one start is allowed')
        self.obsticals=self.find_location(matrix, self.obsticalVal)

    def import_from_file(self, file):
        self.xDim=0
        self.yDim=0
        # Todo: 
        1

    def create_with_dimention(self, dimentions):
        self.xDim=dimentions[0]
        self.yDim=dimentions[1]
        self.__maze=np.full(dimentions, 0)

        self.start=(randint(0,self.xDim-1),
                    randint(0,self.yDim-1))
        while True:
            o=(randint(0,self.xDim-1),
               randint(0,self.yDim-1))
            if o != self.start:
                self.target = o
                break
        
        obs_cnt=randint(2,int(self.xDim*self.yDim/2))
        obs=[]
        i = 0
        while i<obs_cnt:
            o=(randint(0,self.xDim-1),
               randint(0,self.yDim-1))
            if o != self.start and o != self.target and \
               o not in obs:
                obs.append(o)
                i+=1
        self.obsticals=obs

    def __init__(self, matrix=None, dimentions=None, file=None ):
        if matrix is not None:
            self.import_from_matrix(matrix)
        elif dimentions is not None:
            self.create_with_dimention(dimentions)
        elif file is not None:
            self.import_from_file(file)
        else:
            # Trough exeption!
            1
        self.maxLength = self.xDim*self.yDim-len(self.obsticals)
        self.minLength = int(self.xDim*self.yDim/2)
    
    def maze(self):
        m=np.full((self.xDim,self.yDim), 0)
        m[self.start[0]][self.start[1]]=self.startVal
        m[self.target[0]][self.target[1]]=self.targetVal
        for o in self.obsticals:
            m[o[0]][o[1]]=self.obsticalVal
        return m
    
    def get_start(self):
        return self.start
    def get_target(self):
        return self.target

    def get_field(self, coord):
        coord = tuple(coord)
        if coord == self.target:
            return self.targetVal
        if coord[0] < 0 or coord[1] < 0 or \
                coord[0] > self.xDim-1 or coord[1] > self.yDim-1 or \
                coord in self.obsticals:
            return self.obsticalVal
        return 0

    def set_min_path_lenght(self, len):
        self.minLength = int(len)

    def get_min_path_lenght(self):
        return self.minLength

    def get_max_path_lenght(self):
        return self.maxLength
        
if __name__ == "__main__":
    test_maze=Maze(dimentions=(7,7))
    x=test_maze.maze()
    print(x)
    test_maze=Maze(matrix=x)
    print(test_maze.obsticals)
    o = test_maze.obsticals[randint(0,len(test_maze.obsticals)-1)]
    print("Start: ", test_maze.get_start(),test_maze.get_field(test_maze.get_start()))
    print("Obst: ", o, test_maze.get_field(list(o)))
    y=test_maze.obsticals
    c=(randint(0,7),randint(0,7))
    print("Random: ", c, test_maze.get_field(c))
    print("Target: ", test_maze.get_target(),test_maze.get_field(test_maze.get_target()))



# %%


# %%
