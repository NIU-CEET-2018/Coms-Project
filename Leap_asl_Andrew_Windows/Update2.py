import os
import re
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from keras.models import model_from_json
from Normalize import norm

def loadmodel():
    # load json and create model
    json_file = open('right_hand.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("right_hand.hdf5")
    print("Loaded model from disk")
    return loaded_model

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

data_list1 = []
DATA_DIR1 = './Update_Right/'
listing1 = os.listdir(DATA_DIR1)
num_samples1 = len(listing1)

letter_encode = []
for filename in os.listdir(DATA_DIR1):
    m = filename[0]
    letter_encode.append(m)
letter_encode=list(set(letter_encode))
letter_encode.sort()

#creates 3D array
label1 = np.ones((num_samples1, 14), dtype=int)
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
    label1[len(data_list1)-1] = [0]*p+[1]+[0]*(14-p-1)
    #print (label1[len(data_list1)-1])
data_array1 = np.vstack(data_list1)

#exit(0)

#indexs the arrays with the label
train_data1 = [data_array1, label1]
X, Y = train_data1[0], train_data1[1]

#randomizes data set and splits into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)

model = loadmodel()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#checkpoint
filepath='right_hand.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

print(model.summary())

#iterates model over data set
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=100, batch_size=32, callbacks=callbacks_list, verbose=0)