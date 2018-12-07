import os
import re
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

#formats data to all the same size and removes timestamp
def reshape(y):
    y = np.delete(y, 0  ,0)
    z = np.delete(y, -1, 1)
    numrows = len(z)
    if numrows <= 50:
        shape = (50, 41)
        result = np.zeros(shape)
        result[:z.shape[0], :z.shape[1]] = z
    else:
        while numrows > 50:
            z = np.delete(z, -1, 0)
            numrows = len(z)
        result = z
    return result

def norm(data):
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

#definition
data_list1 = []
DATA_DIR1 = './Right_Hand_Train/'
listing1 = os.listdir(DATA_DIR1)
num_samples1 = len(listing1)

letter_encode = []
for filename in os.listdir(DATA_DIR1):
    m = filename[0]
    letter_encode.append(m)
letter_encode=list(set(letter_encode))
letter_encode.sort()


#creates 3D array
label1 = np.ones((num_samples1, 15), dtype=int)
for filename in os.listdir(DATA_DIR1):
    #print(filename)
    x = np.genfromtxt(DATA_DIR1 + filename, delimiter=',')
    normalized = reshape(x)
    normalized = norm(normalized)
    reshaped = normalized.reshape(1, 50, 41)
    data_list1.append(reshaped)
    m = filename[0]
    p = letter_encode.index(m)
    #print(p,m)
    label1[len(data_list1)-1] = [0]*p+[1]+[0]*(15-p-1)
    #print (filename, label2[len(data_list2)-1])
data_array1 = np.vstack(data_list1)


#indexs the arrays with the label
train_data1 = [data_array1, label1]
X, Y = train_data1[0], train_data1[1]
#randomizes data set and splits into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)

#creates model
np.random.seed(7)
model = Sequential()
model.add(Dense(200, input_shape=(50, 41), activation='tanh'))
model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(15, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#checkpoint
filepath='right_hand.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

print(model.summary())

#iterates model over data set
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=150, batch_size=32, callbacks=callbacks_list, verbose=0)


#saves model to file
# serialize model to JSON
model_json = model.to_json()
with open("right_hand.json", "w") as json_file:
    json_file.write(model_json)
print("Saved model to disk")


