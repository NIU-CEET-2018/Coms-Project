#!/usr/bin/python3

"""Interprets bone structures into Gestures and Gesture Sequences."""
from ThinkingSequence import ThinkingSequence


class AI_Multi_Path(ThinkingSequence):
    """An AI multiplexer.

A trainable generator that is constructed on two generators, the first
of which is the simplistic but functional generator and the second of
which is the trainable but notes necessary good. The system will
assume that he second starts off as not very good but as it trained
will eventually swap out the old version for better/trained second
version. This will occur over many runs of the program as data is
collected and the system trained.

"""
    def __init__(self):
        ThinkingSequence.__init__(self)


class Bone_to_Gestlet_GofAI(ThinkingSequence):
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
        ThinkingSequence.__init__(self)


class Bone_to_Gestlet_AI(ThinkingSequence):
    """Converts bone structure information into probable Gestlets.
(A gestlet is a particular hand position in a gesticulation.)

A small RANN written in tensor-flow."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GestletPS_to_GesturePS_GofAI(ThinkingSequence):
    """Converts a Sequence of Gestlets into Gesture Probabilities."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GestletPS_to_GesturePS_AI(ThinkingSequence):
    """Converts a sequence of Gestlets into Gesture Probabilities."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GesturePS_to_GestureMS_GofAI(ThinkingSequence):
    """Converts a sequence of Gesture Probabilities into likely Gestures.

Probably some markovian maths here."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GesturePS_to_GestureMS_AI(ThinkingSequence):
    """Converts a sequence of Gesture Probabilities into likely Gestures.

Probably some markovian maths here."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GestureS_to_Next_Gesture_GofAI(ThinkingSequence):
    """Converts a Gesture Sequence into the probable next word.

Or, if the current word is partly typed, the completion of current
word."""
    def __init__(self):
        ThinkingSequence.__init__(self)


class GestureS_to_Next_Gesture_AI(ThinkingSequence):
    """Converts a Gesture Sequence into the probable next word.

Or, if the current word is partly typed, the completion of current
word."""
    def __init__(self):
        ThinkingSequence.__init__(self)


# Make Gesture
"""Construct a new internal gesture from a given hand gesture."""

# Train Gesture
"""Improve the accuracy of a given gesture via repetition."""
