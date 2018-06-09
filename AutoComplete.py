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


def predict(sent):
    """Predict the current word given a sentience."""
    if(len(sent.split())) > 1:
        return ac.predict_currword_given_lastword(sent.split(" ")[-1], "")
    return ac.predict_currword(sent)


def compleate(sent):
    """Predict the next word given a sentience."""
    return ac.split_predict(sent)

# TODO: Have a function to save new data and lern the client's cantor
# of speech.
