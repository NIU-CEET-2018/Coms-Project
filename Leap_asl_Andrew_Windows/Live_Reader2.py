import numpy as np
from LEAP_Controler import raw_event_source 
from keras.models import load_model
from keras.models import model_from_json
from string import ascii_lowercase
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


def predict_data(predict):
    global model
    global old
    predict = model.predict(predict, verbose=0)
    #convert output from float to rounded integers
    predict = predict > 0.98
    
    predict = predict.astype(int)
    predict = np.reshape(predict, (14,))
    #print(predict)
    #dictionary to translate back to letter
    dictionary = {}
    x = 0
    for c in range(1,10):
        dictionary[str(c)] = np.array([0]*x +[1] + [0]*(13-x))
        x+=1
    dictionary['close'] = np.array([0,0,0,0,0,0,0,0,0,1,0,0,0,0])
    dictionary['down'] = np.array([0,0,0,0,0,0,0,0,0,0,1,0,0,0])
    dictionary['left'] = np.array([0,0,0,0,0,0,0,0,0,0,0,1,0,0])
    dictionary['right'] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,1,0])
    dictionary['up'] = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1])

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
    