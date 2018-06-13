#!/usr/bin/python3

"""Interface with the LEAP Motion to detect hand positions.
"""

import collections
import Physics_Filter


newHands = []

# TODO: Make a thread that
#       - consumes a frame
#       - checks the physics (and removes extra hands)
#       - checks it's non-empty
#       - adds it to a list of un-consumed hand(-pair)s


def Get_Hand():
    """Return the next unconsumed hand position. Blocking."""
    while not newHands:
        # wait
        pass
    # get the front hand
    # remove it from the array
    # return it
