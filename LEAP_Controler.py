#!/usr/bin/python3

"""Some code for interfacing with the LEAP Motion

Examples from here
https://github.com/ssaamm/sign-language-tutor/blob/master/hand_data.py
and here
https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
"""

import time
import collections
import Leap
from Leap import Bone
controller = Leap.Controller()


def valid_hands(h):
    if len(h) == 1:
        return True
    if len(h) == 2:
        if h[0].is_right():
            return h[1].is_left()
        return h[1].is_right()
    return False


def get_hand_position(blocking=False):
    # TODO: convert to a timeout
    frame = controller.frame()
    if not blocking and not valid_hands(frame.hands):
        return None

    while not valid_hands(frame.hands):
        frame = controller.frame()

    dataVector = collections.OrderedDict()

    for hand in frame.hands:
        hand_center = hand.palm_position
        finger_bones = []
        for finger in hand.fingers:
            for b in [Bone.TYPE_METACARPAL,
                      Bone.TYPE_PROXIMAL,
                      Bone.TYPE_INTERMEDIATE,
                      Bone.TYPE_DISTAL,
                      ]:
                finger_bones.append(finger.bone(b).
                                    next_joint)

        # always 20 = 5 fingers * 4 joionts
        for i in range(len(finger_bones)):
            relJoint = (finger_bones[i] - hand_center).to_tuple()
            for j in range(3):
                # if only left or right hand some features will be missing
                # TODO: set them to 0
                dataVector["feat" + str(hand.is_right()*(20*3+3) +
                                        i*3+j+3)] = relJoint[j]
        for j in range(3):
            dataVector["feat"+str(hand.is_right()*(20*3+3)+j)] = hand_center[j]

    # TODO: here goes the physics filter

    return dataVector
