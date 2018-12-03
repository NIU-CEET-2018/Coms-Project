import numpy as np
import pandas as pd
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from Normalize import norm
import re
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
from string import ascii_lowercase



#same reshape as model program
def reshape(y):
    y = np.delete(y, 0 ,0)
    z = np.delete(y,-1,1)
    numrows = len(z)
    if numrows <=50:
        shape=(50,41)
        result = np.zeros(shape)
        result[:z.shape[0],:z.shape[1]] = z
    else:
        while numrows > 50:
            z = np.delete(z,-1,0)
            numrows = len(z)
        result = z
    return result

#definitions
data_list2 = []
DATA_DIR2 = './right_test/'
listing2 = os.listdir(DATA_DIR2)
num_samples2=len(listing2)

letter_encode = []
for filename in os.listdir(DATA_DIR2):
    m = filename[0]
    letter_encode.append(m)
letter_encode=list(set(letter_encode))
letter_encode.sort()


#creates 3D array
label2 = np.ones((num_samples2, 14), dtype=int)
for filename in os.listdir(DATA_DIR2):
    #print(filename)
    x = np.genfromtxt(DATA_DIR2 + filename, delimiter=',')
    normalized = reshape(x)
    normalized = norm(normalized)
    reshaped = normalized.reshape(1, 50, 41)
    data_list2.append(reshaped)
    m = filename[0]
    p = letter_encode.index(m)
    #print(p,m)
    label2[len(data_list2)-1] = [0]*p+[1]+[0]*(14-p-1)
    #print (filename, label2[len(data_list2)-1])
data_array2 = np.vstack(data_list2)
#exit(0)

#labels data
train_data2=[data_array2,label2]
(X_test,Y_test) = (train_data2[0],train_data2[1])
print(train_data2[1].shape)
print(train_data2[0].shape)


# load json and create model
json_file = open('right_hand.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("right_hand.hdf5")
print("Loaded model from disk")

#feeds new data to model and tests
loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
def print_nines(x):
    if x==1:
        print("all the nines!")
        return
    from math import log
    print("that's",round(-log(1-x,10),1),"nines")
print_nines(score[1])

#feeds single file to model for testing
#NOTE: change the file directory in genfromtxt to test any file in the test folder
for filename in os.listdir(DATA_DIR2):
    z_predict = np.genfromtxt(DATA_DIR2 + filename, delimiter= ',')
    z_predict = reshape(z_predict)
    z_predict = norm(z_predict)
    z_final = np.reshape(z_predict, (1,50,41))
    y_predict = loaded_model.predict(z_final, verbose=0)

    #convert output from float to rounded integers
    predict = np.round(y_predict)
    predict =predict.astype(int)
    predict = np.reshape(predict, (14,))
    dictionary = {}
    x = 0
    for c in range(1,10):
        dictionary[str(c)] = np.array([0]*x +[1] + [0]*(13-x))
        x+=1
    dictionary['close'] = [0,0,0,0,0,0,0,0,0,1,0,0,0]
    dictionary['down'] = [0,0,0,0,0,0,0,0,0,0,1,0,0,0]
    dictionary['left'] = [0,0,0,0,0,0,0,0,0,0,0,1,0,0]
    dictionary['right'] = [0,0,0,0,0,0,0,0,0,0,0,0,1,0]
    dictionary['up'] = [0,0,0,0,0,0,0,0,0,0,0,0,0,1]

    #iterates over dictionary to find corresponding letter
    for key, value in dictionary.items():
        if np.array_equal(predict, value):
            l = filename[0]
            if key != l:
                print("Guessed '"+str(key)+"' but was '"+str(l)+"'")
