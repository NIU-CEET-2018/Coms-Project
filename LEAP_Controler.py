#!/usr/bin/python3

"""Some code for interfacing with the LEAP Motion

Examples from here
https://github.com/ssaamm/sign-language-tutor/blob/master/hand_data.py
and here
https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
"""

import os, sys, inspect, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
# arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
controller = Leap.Controller()

def valid_hands(h):
    if len(h)==1:
        return True
    if len(h)==2:
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

    calibrated_finger_bones = collections.OrderedDict()

    for hand in frame.hands:
        hand_center = hand.palm_position
        finger_bones = []
        for finger in hand.fingers:
            finger_bones.append(finger.bone(Bone.TYPE_METACARPAL).next_joint)
            finger_bones.append(finger.bone(Bone.TYPE_PROXIMAL).next_joint)
            finger_bones.append(finger.bone(Bone.TYPE_INTERMEDIATE).next_joint)
            finger_bones.append(finger.bone(Bone.TYPE_DISTAL).next_joint)

        # always 20 = 5 fingers * 4 joionts
        for i in range(len(finger_bones)):
            normalized_joint = (finger_bones[i] - hand_center).to_tuple()
            for j in range(3):
                # if only left or right hand some features will be missing
                # TODO: set them to 0
                calibrated_finger_bones["feat" + str(hand.is_right()*(5*4*3+3) +
                                                     i*3+j+3)] = normalized_joint[j]
        for j in range(3):
            calibrated_finger_bones["feat"+str(hand.is_right()*(5*4*3+3)+j)] = hand_center[j]

    # TODO: here goes the physics filter

    return calibrated_finger_bones


if __name__ == "__main__":
    while True:
        get_hand_position()
        time.sleep(1)
