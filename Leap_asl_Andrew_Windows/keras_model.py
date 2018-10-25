import numpy as np
import pandas as pd
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

from sklearn.model_selection import train_test_split



#formats data to all the same size and removes timestamp
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

#definition
data_list1=[]
DATA_DIR1 = './Train_Data/'
listing1 = os.listdir(DATA_DIR1)
num_samples1=len(listing1)

#creates 3D array
for filename in os.listdir(DATA_DIR1):
    x = np.genfromtxt(DATA_DIR1 + filename,delimiter=',')    
    normalized = reshape(x)
    reshaped = normalized.reshape(1, 50, 37)
    data_list1.append(reshaped)
data_array1 = np.vstack(data_list1)


#one hot encodes the data set
#TODO create a more efficient method for this
label1=np.ones((num_samples1,13),dtype = int)
label1[0:200] = [1,0,0,0,0,0,0,0,0,0,0,0,0]
label1[200:400] = [0,1,0,0,0,0,0,0,0,0,0,0,0]
label1[400:600] = [0,0,1,0,0,0,0,0,0,0,0,0,0]
label1[600:800] = [0,0,0,1,0,0,0,0,0,0,0,0,0]
label1[800:1000] = [0,0,0,0,1,0,0,0,0,0,0,0,0]
label1[1000:1200] = [0,0,0,0,0,1,0,0,0,0,0,0,0]
label1[1200:1400] = [0,0,0,0,0,0,1,0,0,0,0,0,0]
label1[1400:1600] = [0,0,0,0,0,0,0,1,0,0,0,0,0]
label1[1600:1800] = [0,0,0,0,0,0,0,0,1,0,0,0,0]
label1[1800:2000] = [0,0,0,0,0,0,0,0,0,1,0,0,0]
label1[2000:2200] = [0,0,0,0,0,0,0,0,0,0,1,0,0]
label1[2200:2400] = [0,0,0,0,0,0,0,0,0,0,0,1,0]
label1[2400:] = [0,0,0,0,0,0,0,0,0,0,0,0,1]
"""label[488:522] = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
label[522:557] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
label[557:596] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
label[596:632] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
label[632:669] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
label[669:702] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
label[702:741] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
label[741:789] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
label[789:831] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
label[831:870] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
label[870:909] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
label[909:959] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
label[959:] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]"""


#indexs the arrays with the label
train_data1=[data_array1,label1]
(X,Y) = (train_data1[0],train_data1[1])

#randomizes data set and splits into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=4)

#creates model
np.random.seed(7)
model = Sequential()
model.add(Dense(200, input_shape=(50,37), activation='tanh'))
model.add(LSTM(200, dropout=0.2,recurrent_dropout=0.2))
model.add(Dense(13, activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
print(model.summary())

#iterates model over data set
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=200, batch_size=32)

# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=2)
print("Accuracy: %.2f%%" % (scores[1]*100))


#saves model to file
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


