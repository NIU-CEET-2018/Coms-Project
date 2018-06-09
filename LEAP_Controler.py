#!/usr/bin/python3

"""Interface with the LEAP Motion to detect hand positions.
"""

import collections
import Leap
from Leap import Bone
import Physics_Filter

CONTROLLER = Leap.Controller()


def handle_frame():
    """Capture and convert a frame from the LEAP into hand vectors."""
    frame = CONTROLLER.frame()

    handVectors = collections.OrderedDict()
    # TODO: Make this an array of "OrderedDict"s

    h = -1
    for hand in frame.hands:
        h += 1
        hand_center = hand.palm_position
        finger_bones = []
        for finger in hand.fingers:
            for b in [Bone.TYPE_METACARPAL,
                      Bone.TYPE_PROXIMAL,
                      Bone.TYPE_INTERMEDIATE,
                      Bone.TYPE_DISTAL]:
                finger_bones.append(finger.bone(b)
                                    .next_joint)

        for i in range(len(finger_bones)):
            relJoint = (finger_bones[i] - hand_center).to_tuple()
            if hand.is_left():
                # TODO: negate the LR axis to make a right hand
                pass
            for j in range(3):
                handVectors[h]["feat" + str(i*3+j)] = relJoint[j]
        for j in range(3):
            handVectors[h]["featHand"+str(j)] = hand_center[j]

    return handVectors


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
    pass
