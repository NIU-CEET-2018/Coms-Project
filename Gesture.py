#!/usr/bin/python3

"""Interprets bone structures into Gestures and Gesture Sequences."""
from IntelligentTubes import LearningSequence


class Bone_to_Gestlet_GofAI(LearningSequence):
    """Converts bone structure information into probable Gestlets.
(A gestlet is a particular hand position in a gesticulation.)

The system keeps a set of pre-approved Gestlet snapshots and compares
the distance between them and the current gestlet, returning the
normalized reciprocal of their values.

#+BEGIN_SRC \\latex{APL}
p\\rightarrow\\{1 \\div w\\}/dist
p\\rightarrow 1-\\umlaut{\\tilde} 2\\times p\\div max(p)
p\\rightarrow p\\div+/p
#+END_SRC
"""
    def __init__(self):
        LearningSequence.__init__(self)


class Bone_to_Gestlet_AI(LearningSequence):
    """Converts bone structure information into probable Gestlets.
(A gestlet is a particular hand position in a gesticulation.)

A small RANN written in tensor-flow."""
    def __init__(self):
        LearningSequence.__init__(self)


class GestletPS_to_GesturePS_GofAI(LearningSequence):
    """Converts a Sequence of Gestlets into Gesture Probabilities."""
    def __init__(self):
        LearningSequence.__init__(self)


class GestletPS_to_GesturePS_AI(LearningSequence):
    """Converts a sequence of Gestlets into Gesture Probabilities."""
    def __init__(self):
        LearningSequence.__init__(self)


class GesturePS_to_GestureMS_GofAI(LearningSequence):
    """Converts a sequence of Gesture Probabilities into likely Gestures.

Probably some markovian maths here."""
    def __init__(self):
        LearningSequence.__init__(self)


class GesturePS_to_GestureMS_AI(LearningSequence):
    """Converts a sequence of Gesture Probabilities into likely Gestures.

Probably some markovian maths here."""
    def __init__(self):
        LearningSequence.__init__(self)


class GestureS_to_Next_Gesture_GofAI(LearningSequence):
    """Converts a Gesture Sequence into the probable next word.

Or, if the current word is partly typed, the completion of current
word."""
    def __init__(self):
        LearningSequence.__init__(self)


class GestureS_to_Next_Gesture_AI(LearningSequence):
    """Converts a Gesture Sequence into the probable next word.

Or, if the current word is partly typed, the completion of current
word."""
    def __init__(self):
        LearningSequence.__init__(self)


def MakeGesture():
    """Construct a new internal gesture from a given hand gesture."""
    pass


def TrainGesture():
    """Improve the accuracy of a given gesture via repetition."""
    pass
