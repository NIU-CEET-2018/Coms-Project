#!/usr/bin/python3

"""Interface with the LEAP Motion to detect hand positions.
"""

import Leap
from Leap import Bone
controller = Leap.Controller()
import collections


import Physics_Filter


def handle_frame():
    frame = controller.frame()

    handVectors = collections.OrderedDict()
    # TODO: Make this an array of "OrderedDict"s

    h=-1
    for hand in frame.hands:
        h+=1
        hand_center = hand.palm_position
        finger_bones = []
        for finger in hand.fingers:
            for b in [Bone.TYPE_METACARPAL,
                      Bone.TYPE_PROXIMAL,
                      Bone.TYPE_INTERMEDIATE,
                      Bone.TYPE_DISTAL,
                      ]:
                finger_bones.append(finger.bone(b)
                                    .next_joint)

        for i in range(len(finger_bones)):
            relJoint = (finger_bones[i] - hand_center).to_tuple()
            if hand.is_left():
                # TODO: negate the LR axis to make a right hand
                pass
            for j in range(3):
                dataVector[h]["feat" + str(i*3+j)] = relJoint[j]
        for j in range(3):
            dataVector[h]["featHand"+str(j)] = hand_center[j]

    return dataVector

newHands=[]

# TODO: Make a thread that
#       - consumes a frame
#       - checks the physics (and removes extra hands)
#       - checks it's non-empty
#       - adds it to a list of un-consumed hand(-pair)s

def Get_Hand(blocking=True):
    while blocking and len(newHands):
        # wait
        pass
    if len(newHands):
        # get the front hand
        # remove it from the array
        # return it
        pass
