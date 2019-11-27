# %%
import numpy as np
import csv
# import predict as util

# %%


w1 = np.matrix([
        [0.01, 0.05, 0.07],
        [0.2, 0.041, 0.11],
        [0.04, 0.56, 0.13],
        [0.1, 0.1, 0.1]
    ])
w2 = np.matrix([
        [0.04, 0.78],
        [0.4, 0.45],
        [0.65, 0.23],
        [0.1, 0.1]
    ])
w3 = np.matrix([
        [0.04],
        [0.41],
        [0.1]
    ])


x_size=4
z1_size=6
z2_size=6
z3_size=4

w1=np.random.normal(-1,1,(x_size,z1_size))
w2=np.random.normal(-1,1,(z1_size+1,z2_size))
w3=np.random.normal(-1,1,(z2_size+1,z3_size))

# x=[0.1, -0.1, -0.22, 0.3]
# x=np.random.randint(7, size=(10,4))/3.5-1
x=np.random.normal(-1,1,(2,x_size))

z2 = np.dot(x, w1)
a2 = np.tanh(z2)
ba2 = np.ones((x.shape[0], 1))
a2 = np.concatenate((a2, ba2), axis=1)

z3 = np.dot(a2, w2)
a3 = np.tanh(z3)
# we add the the 1 unit (bias) at the output of the second layer
ba3 = np.ones((a3.shape[0], 1))
a3 = np.concatenate((a3, ba3), axis=1)

# output layer, prediction of our network
z4 = np.dot(a3, w3)
a4 = np.tanh(z4)

r = []
for a_ in a4:
    r.append(np.where(a_ == np.amax(a_))[0][0])
print(a4)
print(r)

y=np.random.normal(-1,1,(10,x_size))
result = np.where(y == np.amax(y))  

# %%

# a = np.arange(9) - 4
# print(a)
# b = a.reshape((3, 3))
# print(b)
# print(np.linalg.norm(a))
# print(np.linalg.norm(b, 'fro'))
# print(np.linalg.norm(b, axis=0))
# print(np.linalg.norm(b, axis=1))
