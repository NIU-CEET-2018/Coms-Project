import numpy as np
import os

def norm(data):
    #normalization functions
    def positionxz(x):
        y = (x + 500)/(1000)
        return y
    def positiony(x):
        y = x/500
        return y
    def unitvector(x):
        y = (x+1)/(2)
        return y
    def velocity(x):
        y = (x+1000)/(2000)
        return y

    #uses specified normalization function on correct rows
    for x in range(len(data[:,0])):
        y = data[x,0]
        y = positionxz(y)
        data[x, 0] = y

    for x in range(len(data[:,1])):
        y = data[x,1]
        y = positiony(y)
        data[x, 1] = y

    for x in range(len(data[:,2])):
        y = data[x,2]
        y = positionxz(y)
        data[x, 2] = y
        
    for column in range(3,9):
        for x in range(len(data[:,column])):
            y = data[x,column]
            y = unitvector(y)
            data[x, column] = y

    for column in range(9,12):
        for x in range(len(data[:,column])):
            y = data[x,column]
            y = velocity(y)
            data[x, column] = y
    return data

