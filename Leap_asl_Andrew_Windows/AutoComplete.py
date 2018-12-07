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

def give(probl_let_arry):
    """Recive an aray of probably letters."""
    curr += probl_let_arry

# private
def modes(pos_lets_array):
    if len(pos_lets_array)=0:
        return ['']
    ms = list(modes(pos_lets_array[1:]))
    return list(l+m
                for l in pos_lets_array[0]
                for m in ms)
    
def known():
    """Give known words back."""
    # TODO: get new knowns
    def actual_thing():
        """check for known words."""
        ln=len(curr)
        for l in range(curr):
            p=list(*ac.predict(mode)
                   for mode in modes(curr[:l]))
            if len(p)==1:
                curr_done.append(p[0][0])
                curr=curr[l:]
                break
            if len(p)=0:
                p=list(*ac.predict(mode)
                       for mode in modes(curr[:l-1]))
                curr_done.append(p[0][0])
                break
        if len(curr)!=ln:
            actual_thing()
    # return the set of knowns
    ret=curr_done
    sent += curr_done
    curr_done=[]
    sent = sent.split('.')[-1]
    return ret

def predict():
    """Predict the next or current word given a sentience."""
    if curr == '':
        if len(curr_done)>0:
            return ac.predict(curr_done[-1],'')
        return ac.predict(sent.split(' ')[-1],'')
    else:
        pos_strs = modes(curr)
        if len(curr_done)>0:
            return set(*ac.predict(curr_done[-1],word)
                       for word in pos_strs)
        return set(*ac.predict(sent.split(' ')[-1],word)
                   for word in pos_strs)


# TODO: Have a function to save new data and lern the client's cantor
# of speech.
