import numpy as np
x = np.array([[1,2,3,4,5],[5,4,3,2,1]])
print(x.item(-1))
x = np.reshape(x,(1,2,5))
print(x.item(-1))