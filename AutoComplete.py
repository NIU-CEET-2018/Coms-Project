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

def predict(s):
    if(len(s.split()))>1:
        return ac.predict_currword_given_lastword(s.split(" ")[-1],"")
    else:
        return ac.predict_currword(s)

def compleate(s):
    return ac.split_predict(s)

#TODO: Have a function to save new data and lern the client's cantor
# of speech.
