#!/usr/bin/python3

"""Offer completions for words and sentences.

Based on examples or prior text (though training) offer possible
completions to bo individual words and sentences.
"""

# TODO: This module will probably be completely replaced by one that
# converts the set of probable hand gestures into words and sentences.
# This is because in sign-languages (as in speech) words are not
# delineated, and so regular completion libs will not suffice.

import autocomplete as ac

ac.load()

# TODO: globals for remebering state
#predicting letter buffer
curr = []
#done letter buffer
curr_done = []
#current Senctince
sent = []

DEBUG = False #True

def give(probl_let_arry):
    """Recive an aray of probably letters."""
    global curr
    curr.append(probl_let_arry)

# private
def modes(pos_lets_array):
    if len(pos_lets_array)==0:
        return ['']
    ms = list(modes(pos_lets_array[1:]))
    return list(l+m
                for l in pos_lets_array[0]
                for m in ms)
    
def known():
    """Give known words back."""
    global curr
    global curr_done
    global sent
    global DEBUG
    if DEBUG:
        print("curr",curr)
        print("done",curr_done)
        print("sent",sent)
    def actual_thing():
        """check for known words."""
        global curr
        while curr[0]==[' ']:
            curr.pop(0)
            curr_done.append([' '])
        ln=len(curr)
        print("smart part",ln,curr)
        for l in range(ln):
            p=list(p
                   for mode in modes(curr[:l])
                   for p in ac.predict_currword(mode))
            #print(p)
            if len(p)==1:
                print("found",p[0][0])
                curr_done.append(p[0][0])
                curr=curr[l:]
                break
            if len(p)==0:
                p=list(p[0]
                   for mode in modes(curr[:l-1])
                   for p in ac.predict_currword(mode))
                print(p)
                if curr[:l-1] in p:
                    p=[curr[:l-1]]
                print("guessed",p[0])
                curr=curr[l-1:]
                curr_done.append(p[0])
                break
        if len(curr)!=ln:
            actual_thing()
    actual_thing()
    # return the set of knowns
    ret=curr_done
    sent += curr_done
    curr_done=[]
    sent = ' '.join(sent).split('.')[-1].split(' ')
    return ret

def predict():
    """Predict the next or current word given a sentience."""
    global curr
    global curr_done
    global sent
    if curr == '':
        if len(curr_done)>0:
            return ac.predict(curr_done[-1],'')
        elif len(sent)>0:
            return ac.predict(sent[-1],'')
        else:
            return []
    else:
        pos_strs = modes(curr)
        if len(curr_done)>0:
            return set(p
                       for word in pos_strs
                       for p in ac.predict(curr_done[-1],word))
        elif len(sent)>0:
            return set(p
                       for word in pos_strs
                       for p in ac.predict(sent[-1],word))
        else:
            return []

# TODO: Have a function to save new data and lern the client's cantor
# of speech.