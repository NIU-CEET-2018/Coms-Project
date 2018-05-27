#!/usr/bin/python3

"""Interpreats bone structures into Gestures and Gesture Sequences.
"""

# Bone to Gestlet
"""Converts bone structure information into probable Gestlets.
(A gestlet is a particular hand position in a gesticulation.)"""

# Gestlet Seq to P(Gesture)
"""Converts a small sequence of Gestlets into a probable Gesture.
OR
Converts an updating sequence of Gestlets into an updating sequence of Gesture Probabilities."""

# P(Gesture) Seq to Gesture Seq
"""Converts a Sequence of Gesture Probabilities into a most likely (Markovian?) sequence of Gestures.
OR
Converts an updating sequence of Gesture Probabilities into an updating sequence of most likely Gestures."""

# Current Gesture Seq to Next Gesture Prediction
"""Takes in a Gesture Sequence and outputs the probable (next word) or (completion of current word)."""

# AI Multi-Path
"""A trainable generator that is constructed on two generators, the first of which is the simplistic but functional generator and the second of which is the trainable but notes necessary good. The system will assume that he second starts off as not very good but as it trained will eventually swap out the old version for better/trained second version. This will occur over many runs of the program as data is collected and the system trained."""

# Make Gesture
"""Construct a new internal gesture from a given hand gesture."""
# Train Gesture
"""Improve the accuracy of a given gesture's recognition via manual repetition."""
