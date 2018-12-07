import numpy as np
from LEAP_Controler import raw_event_source 
from keras.models import load_model
from keras.models import model_from_json
from string import ascii_lowercase
from Normalize import norm
from collections import defaultdict


def loadmodel1():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("weights.best.hdf5")
    print("Loaded model1 from disk")
    return loaded_model

def loadmodel2():
    # load json and create model
    json_file = open('right_hand.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("right_hand.hdf5")
    print("Loaded model2 from disk")
    return loaded_model


def predict_data1(data):
    global predict1
    global model1

    predict1 = np.vstack((predict1,data))
    predict1 = np.delete(predict1, 0, 0)
    predict = np.reshape(predict1,(1,50,41))

    predict = model1.predict(predict, verbose=0)

    #convert output from float to rounded integers
    m = max(*list(predict)) # get the max probability
    predict = predict > m * .8 # check for at least 80% of max found
    if sum(*predict)*m < .8: # check that the total chance of a letter is at least 80%
        return 'nope' # if not leave

    predict = np.reshape(predict, (27,))
    #print(predict)
    #dictionary to translate back to letter
    dictionary = {}
    
    for c in range(0,18):
        dictionary[ascii_lowercase[c]] = np.array([0]*c +[1] + [0]*(26-c))

    for c in range(19,27):
        dictionary[ascii_lowercase[c-1]] = np.array([0]*c +[1] + [0]*(26-c))
    if np.all(predict == np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0])):
        return "nope"
    else:
        return output(predict, dictionary)

#def document(key):
    #with open("Document.txt", "w") as text_file:
        #text_file.write(key)

def predict_data2(data):
    global predict2
    global model2
    predict2 = np.vstack((predict2,data))
    predict2 = np.delete(predict2, 0, 0)
    predict = np.reshape(predict2,(1,50,41))

    predict = model2.predict(predict, verbose=0)

    #convert output from float to rounded integers
    m = max(*list(predict)) # get the max probability
    predict = predict > m * .8 # check for at least 80% of max found
    if sum(*predict)*m < .8: # check that the total chance of a letter is at least 80%
        return 'nope' # if not leave

    predict = np.reshape(predict, (15,))

    #translates
    dictionary = {}
    for c in range(1,5):
        dictionary[str(c)] = np.array([0]*(c) +[1] + [0]*(14-(c)))
    for c in range(6,10):
        dictionary[str(c)] = np.array([0]*(c) +[1] + [0]*(14-(c)))
    
    dictionary['5'] = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    dictionary['close'] = np.array([0,0,0,0,0,0,0,0,0,0,1,0,0,0,0])
    dictionary['down'] = np.array([0,0,0,0,0,0,0,0,0,0,0,1,0,0,0])
    dictionary['left'] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0])
    dictionary['right'] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,0])
    dictionary['up'] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    
    if np.all(predict == np.array([0,0,0,0,1,0,0,0,0,0,0,0,0,0])):
        return "nope"
    else:
        return output1(predict, dictionary)

def output(prediction, dictionary):
    global times
    global old
    #iterates over dictionary to find corresponding letter
    for key, value in dictionary.items():
        if np.array_equal(prediction, value):
            times+=1
            if key!=old:
                times=0
                old=key
            if times==20:
                return key

def output1(prediction, dictionary):
    global times
    global old
    #iterates over dictionary to find corresponding letter
    for key, value in dictionary.items():
        if np.array_equal(prediction, value):
            times+=1
            if key!=old:
                times=0
                old=key
            if times==20:
                return key

times = 0#defaultdict(lambda: 0)
predict1=np.zeros((50,41))
predict2=np.zeros((50,41))
old=None
model1 = loadmodel1()
model2 = loadmodel2()

def splitter(data):
    if data[0]!='[':
        print(data)
        return "nope"
    data=eval(data) # TODO: make that a parser
    data = np.array([data])
    data=norm(data)
    #print(data)
    x = data.item(-1)
    data=np.delete(data, -1, 1)
    #print(data)
    if x == 1:
        return predict_data1(data)
    else:
        return predict_data2(data)

    #document(key)



if __name__ == "__main__":
    def prnt(x):
        if x != None and x != 'nope':
            print(x)
    raw_event_source(lambda x:prnt(splitter(x)))
    




