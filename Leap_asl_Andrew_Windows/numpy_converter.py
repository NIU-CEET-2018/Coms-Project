import numpy
import numpy as np
test = np.array([[1,2,3,4,5],[2,2,3,4,5],[3,3,4,5,2],[4,2,3,4,5],[5,2,3,4,5],[6,2,3,4,5],[7,2,3,4,5]])

print (test[3])
def reshape(y):
    x = 0
    numrows = len(y)
    print(numrows)
    if numrows <=4:
        shape=(4,5)
        result = np.zeros(shape)
        result[:y.shape[0],:y.shape[1]] = y
    else:
        while numrows > 4:
            y = np.delete(y,-1,0)
            numrows = len(y)
        result = y

    return result


x = reshape(test)

print(x)