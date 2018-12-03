import numpy as np
import pandas as pd
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from sklearn.model_selection import train_test_split
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation

dataframe1 = pd.read_csv('E:/Github/Coms-Project/Leap_asl_Andrew_Windows/standar_class/a0.csv', header=None)
dataframe2 = pd.read_csv('E:/Github/Coms-Project/Leap_asl_Andrew_Windows/standar_class/b1.csv', header=None)
dataset1 = dataframe1.values
dataset2 = dataframe2.values
X_train = dataset1[:,0:37].astype(float)
Y_train = dataset1[:,37]
X_test = dataset2[:,0:37].astype(float)
Y_test = dataset2[:,37]

model = Sequential()
model.add(Dense(37, input_dim=37, activation='tanh'))

model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, Y_train, epochs=20, batch_size=10)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

predictx = np.array([-0.64793992,176.9178314,10.05590057,0.308497488,0.235490337,-0.921614647,
0.031486955,-0.970868349,-0.23753579,2.8560431,-21.7956295,-12.18798351,0.658587866,0.606588783,	
0.813041276,	0.723884172,	0.680979226,	0.999176798,	0.5613816,	0.710258405,	0.968649736,	0.805780325,	0.998519311,	
0.548788784,	0.781188077,	0.985765746,	0.832286535,	0.999575864,	0.562006087,	0.756794214,	0.991037015,	0.795011433,	
0.997204393,	0.603242934,	0.719559501,	0.991417767,	0.781813749
])
print(predictx.shape)
prediction = model.predict(predictx, verbose=0)
print(prediction)

