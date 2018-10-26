import numpy as np
import pandas as pd
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

from keras.models import model_from_json
from sklearn.model_selection import train_test_split


data_list2=[]
#same reshape as model program
def reshape(y):
    y = np.delete(y, 0 ,0)
    z = np.delete(y,-1,1)
    numrows = len(z)
    if numrows <=50:
        shape=(50,37)
        result = np.zeros(shape)
        result[:z.shape[0],:z.shape[1]] = z
    else:
        while numrows > 50:
            z = np.delete(z,-1,0)
            numrows = len(z)
        result = z
    return result

#definitions
DATA_DIR2 = './Test_Data/'
listing2 = os.listdir(DATA_DIR2)
num_samples2=len(listing2)

#creating 3D array
for filename in os.listdir(DATA_DIR2):
    x1 = np.genfromtxt(DATA_DIR2 + filename,delimiter=',')    
    normalized1 = reshape(x1)
    reshaped1 = normalized1.reshape(1, 50, 37)
    data_list2.append(reshaped1)
data_array2 = np.vstack(data_list2)

#onehot encoding
label2=np.ones((num_samples2,13),dtype = int)
label2[0:20] = [1,0,0,0,0,0,0,0,0,0,0,0,0]
label2[20:40] = [0,1,0,0,0,0,0,0,0,0,0,0,0]
label2[40:60] = [0,0,1,0,0,0,0,0,0,0,0,0,0]
label2[60:80] = [0,0,0,1,0,0,0,0,0,0,0,0,0]
label2[80:100] = [0,0,0,0,1,0,0,0,0,0,0,0,0]
label2[100:120] = [0,0,0,0,0,1,0,0,0,0,0,0,0]
label2[120:140] = [0,0,0,0,0,0,1,0,0,0,0,0,0]
label2[140:160] = [0,0,0,0,0,0,0,1,0,0,0,0,0]
label2[160:180] = [0,0,0,0,0,0,0,0,1,0,0,0,0]
label2[180:200] = [0,0,0,0,0,0,0,0,0,1,0,0,0]
label2[200:220] = [0,0,0,0,0,0,0,0,0,0,1,0,0]
label2[220:240] = [0,0,0,0,0,0,0,0,0,0,0,1,0]
label2[240:] = [0,0,0,0,0,0,0,0,0,0,0,0,1]

#labels data
train_data2=[data_array2,label2]
(X_test,Y_test) = (train_data2[0],train_data2[1])


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("weights.best.hdf5")
print("Loaded model from disk")

#feeds new data to model and tests
loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X_test, Y_test, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))

#feeds single file to model for testing
#NOTE: change the file directory in genfromtxt to test any file in the test folder
z_predict = np.genfromtxt(DATA_DIR2 + 'm14.csv', delimiter= ',')
z_predict = reshape(z_predict)
z_final = np.reshape(z_predict, (1,50,37))
y_predict = loaded_model.predict(z_final, verbose=0)

#convert output from float to rounded integers
predict = np.round(y_predict)
predict =predict.astype(int)
predict = np.reshape(predict, (13,))

#dictionary to translate back to letter
dictionary = {'a': np.array([1,0,0,0,0,0,0,0,0,0,0,0,0]),
             'b': np.array([0,1,0,0,0,0,0,0,0,0,0,0,0]),
             'c': np.array([0,0,1,0,0,0,0,0,0,0,0,0,0]),
             'd': np.array([0,0,0,1,0,0,0,0,0,0,0,0,0]),
             'e': np.array([0,0,0,0,1,0,0,0,0,0,0,0,0]),
             'f': np.array([0,0,0,0,0,1,0,0,0,0,0,0,0]),
             'g': np.array([0,0,0,0,0,0,1,0,0,0,0,0,0]),
             'h': np.array([0,0,0,0,0,0,0,1,0,0,0,0,0]),
             'i': np.array([0,0,0,0,0,0,0,0,1,0,0,0,0]),
             'j': np.array([0,0,0,0,0,0,0,0,0,1,0,0,0]),
             'k': np.array([0,0,0,0,0,0,0,0,0,0,1,0,0]),
             'l': np.array([0,0,0,0,0,0,0,0,0,0,0,1,0]),
             'm': np.array([0,0,0,0,0,0,0,0,0,0,0,0,1])}

#iterates over dictionary to find corresponding letter
for key, value in dictionary.items():
    if np.array_equal(predict, value):
        print(key)