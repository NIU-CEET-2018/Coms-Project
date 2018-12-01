#!/usr/bin/python2
import os
import sys
import math
import numpy as np
import threading
from datetime import datetime
import sys
import LEAP.Leap as Leap
from LEAP.Leap import Bone
# , thread, time

DEBUG_LEAP_PRINTS = False

class Listener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            def get_xyz(obj):
                """Returns a tuple of the x, y, and z components of an object."""
                return (obj.x, obj.y, obj.z)

            data = []

            # Get palm metrics
            for metric in [hand.palm_position,
                        hand.direction,
                        hand.palm_normal,
                        hand.palm_velocity]:
                for direction in get_xyz(metric):
                    data.append(direction)

            prev_bone = None
            # Get fingers
            for finger in hand.fingers:
                def bone(num, fin=finger):
                    """Returns the xyz of a particular bone."""
                    return get_xyz(fin.bone(num).direction)

                def deviation(bone, han=hand):
                    """Angle of deviation of a bone from straight."""
                    return math.cos(np.dot(bone, get_xyz(han.direction))) \
                        / (np.linalg.norm(bone) * np.linalg.norm(get_xyz(han.direction)))

                def bend_angle(bone1, bone2):
                    """Angle of deviation between two bones."""
                    return math.cos(np.dot(bone1, bone2)) \
                        / (np.linalg.norm(bone1) * np.linalg.norm(bone2))

                def finger_to_finger(bone1, bone2):
                    if bone2 is None:
                        pass
                    else:
                        data.append(bend_angle(bone1, bone2))

                data.append(deviation(bone(1)))
                data.append(deviation(bone(2)))
                data.append(deviation(bone(3)))
                data.append(bend_angle(bone(1), bone(2)))
                data.append(bend_angle(bone(2), bone(3)))

                finger_to_finger(bone(1), prev_bone)
                prev_bone = bone(1)
        
            print str(data)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

        return "STATE_UNKNOWN"


def main():
    listener = Listener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
