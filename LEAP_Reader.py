#!/usr/bin/python2

import sys
import LEAP.Leap as Leap
from LEAP.Leap import Bone
# , thread, time


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
            p = []
            p.append(frame.id)
            p.append(frame.timestamp)
            p.append(hand.is_left())
            for j in range(3):
                p.append(hand.palm_position[j])
            for finger in hand.fingers:
                for b in [Bone.TYPE_METACARPAL,
                          Bone.TYPE_PROXIMAL,
                          Bone.TYPE_INTERMEDIATE,
                          Bone.TYPE_DISTAL]:
                    for j in range(3):
                        p.append((finger.bone(b).next_joint
                                  - hand.palm_position)[j])
            print(p)

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
