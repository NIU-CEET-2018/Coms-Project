#!/usr/bin/python3

"""Some code for interfacing with the LEAP Motion

Examples from here
https://github.com/ssaamm/sign-language-tutor/blob/master/hand_data.py
and here
https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
"""

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
controller = Leap.Controller()

def get_hand_position(blocking=False):
    # TODO: convert to a timeout
    frame = controller.frame()
    if not blocking and len(frame.fingers) == 0:
        return None

    while len(frame.fingers) == 0:
        frame = controller.frame()

    # TODO: two hands will usualy be present
    fingers = controller.frame().fingers
    finger_bones = []
    for finger in fingers:
        finger_bones.append(finger.bone(Bone.TYPE_METACARPAL).next_joint)
        finger_bones.append(finger.bone(Bone.TYPE_PROXIMAL).next_joint)
        finger_bones.append(finger.bone(Bone.TYPE_INTERMEDIATE).next_joint)
        finger_bones.append(finger.bone(Bone.TYPE_DISTAL).next_joint)

    # possible issue when more than one hand
    hands = controller.frame().hands
    hand_center = 0
    for hand in hands:
        hand_center = hand.palm_position

        calibrated_finger_bones = collections.OrderedDict()
        for i in range(len(finger_bones)):
            normalized_joint = (finger_bones[i] - hand_center).to_tuple()
            for j in range(3):
                calibrated_finger_bones["feat" + str(i*3+j)] = normalized_joint[j]

    # TODO: here goes the physics filter

    return calibrated_finger_bones

if __name__ == "__main__":
    while True:
        get_hand_position()
        time.sleep(1)
