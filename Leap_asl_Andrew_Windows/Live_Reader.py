import numpy as np
from LEAP_Controler import raw_event_source 
from keras.models import load_model
from keras.models import model_from_json
from string import ascii_lowercase


def loadmodel():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("weights.best.hdf5")
    print("Loaded model from disk")
    return loaded_model

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

def predict_data(predict):
    global model
    global old
    predict = model.predict(predict, verbose=0)

    #convert output from float to rounded integers
    predict = predict > 0.98
    
    predict = predict.astype(int)
    predict = np.reshape(predict, (26,))

    #dictionary to translate back to letter
    dictionary = {}
    x = 0
    for c in ascii_lowercase:
        dictionary[c] = np.array([0]*x +[1] + [0]*(25-x))
        x+=1

    global times
    #iterates over dictionary to find corresponding letter
    for key, value in dictionary.items():
        if np.array_equal(predict, value):
            times+=1
            if key!=old:
                times=0
                old=key
            if times==10:
                print(key)
                #return key

#def document(key):
    #with open("Document.txt", "w") as text_file:
        #text_file.write(key)


times=0
model = loadmodel()
predict=np.zeros((50,41))
old=None
def all_the_Things(data):
    global predict
    if data[0]!='[':
        print(data)
        return
    data=eval(data) # TODO: make that a parser
    data = np.array([data])
    data=norm(data)
    predict = np.vstack((predict,data))
    predict = np.delete(predict, 0, 0)
    predict1 = np.reshape(predict,(1,50,41))
    predict_data(predict1)
    #document(key)



if __name__ == "__main__":
    raw_event_source(all_the_Things)
    