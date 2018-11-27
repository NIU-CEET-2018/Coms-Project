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
    z = np.delete(y, -1, 1)
    numrows = len(z)
    if numrows <= 50:
        shape = (50, 37)
        result = np.zeros(shape)
        result[:z.shape[0], :z.shape[1]] = z
    else:
        while numrows > 50:
            z = np.delete(z, -1, 0)
            numrows = len(z)
        result = z
    return result

#definition
data_list1 = []
DATA_DIR1 = './Normalize/'
listing1 = os.listdir(DATA_DIR1)
num_samples1 = len(listing1)

letter_encode=[]
for filename in os.listdir(DATA_DIR1):
    m = re.search(r'[a-zA-Z]',filename)
    letter_encode.append(m.group(0))
letter_encode=list(set(letter_encode))
letter_encode.sort()

#creates 3D array
label1 = np.ones((num_samples1, 13), dtype=int)
for filename in os.listdir(DATA_DIR1):
    #print(filename)
    x = np.genfromtxt(DATA_DIR1 + filename, delimiter=',')
    normalized = reshape(x)
    reshaped = normalized.reshape(1, 50, 37)
    data_list1.append(reshaped)
    m = re.search(r'[a-zA-Z]',filename)
    p = letter_encode.index(m.group(0))
    #print(p,m.group(0))
    label1[len(data_list1)-1] = [0]*p+[1]+[0]*(len(letter_encode)-p-1)
data_array1 = np.vstack(data_list1)

#exit(0)

#indexs the arrays with the label
train_data1 = [data_array1, label1]
X, Y = train_data1[0], train_data1[1]

#randomizes data set and splits into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=4)

#creates model
np.random.seed(7)
model = Sequential()
model.add(Dense(200, input_shape=(50, 37), activation='tanh'))
model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(13, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#checkpoint
filepath='weights.best.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

print(model.summary())

#iterates model over data set
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=200, batch_size=32, callbacks=callbacks_list, verbose=0)


# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=2)
print("Accuracy: %.2f%%" % (scores[1]*100))


#saves model to file
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
print("Saved model to disk")


