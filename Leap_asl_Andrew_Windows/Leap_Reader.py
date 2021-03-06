#!/usr/bin/python2

""" File documentation/desription goes here.

TODO: This @amurph.
"""

import csv
import os
import sys
import math
import numpy as np
import Leap
import threading
from datetime import datetime


DEBUG_LEAP_PRINTS = False
DATA_DIR = './Data_Folder/'
CSV_WRITER = None
count = 0
def safe_frame_serial(frame):
    """Save a leap frame using the built in seiralization."""
    raise Exception("TODO!")

def save_frame_canonical(frame):
    """Save a leap frame in the conolical form."""
    if DEBUG_LEAP_PRINTS:
        print "Frame "        + str(frame.id)              + "\n" + \
              "- timestamp: " + str(frame.timestamp)       + "\n" + \
              "- hands:     " + str(len(frame.hands))      + "\n" + \
              "- fingers:   " + str(len(frame.fingers))    + "\n" + \
              "- tools:     " + str(len(frame.tools))      + "\n" + \
              "- gestures:  " + str(len(frame.gestures()))
    global are_there_hands
    global are_there_no_hands
    if len(frame.hands)>0:
        if not are_there_hands.is_set():
            # print "Hand Found"
            are_there_hands.set()
            are_there_no_hands.clear()
    else:
        if not are_there_no_hands.is_set():
            # print "Hand Lost"
            are_there_hands.clear()
            are_there_no_hands.set()

    # Get hands
    for hand in frame.hands:
        handType = "Left hand" if hand.is_left else "Right hand"

        def get_xyz(obj):
            """Returns a tuple of the x, y, and z components of an object."""
            return (obj.x, obj.y, obj.z)

        if DEBUG_LEAP_PRINTS:
            print str(handType) + " - " + str(hand.id) + "\n" + \
                  " - center:    " + str(get_xyz(hand.palm_position)) + "\n" + \
                  " - direction: " + str(get_xyz(hand.direction))     + "\n" + \
                  " - normal:    " + str(get_xyz(hand.palm_normal))   + "\n" + \
                  " - velocity:  " + str(get_xyz(hand.palm_velocity))

        data = []

        # Get palm metrics
        for metric in [hand.palm_position,
                       hand.direction,
                       hand.palm_normal,
                       hand.palm_velocity]:
            for direction in get_xyz(metric):
                data.append(direction)

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

            data.append(deviation(bone(1)))
            data.append(deviation(bone(2)))
            data.append(deviation(bone(3)))
            data.append(bend_angle(bone(1), bone(2)))
            data.append(bend_angle(bone(2), bone(3)))

            # TODO: Put the above data in the desired canonical form.
            # The angle between the bones in the direction of normal
            # The angle between the bones and the plane of (normal & prior bone)

        data.append(frame.timestamp)
        CSV_WRITER.writerow(data)

class LeapSerrializingListner(Leap.Listener):
    """TODO: @amurph"""
    bones = ['Metacarpal', 'Proximal', 'Medial', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, _):
        print "Initialized"

    def on_connect(self, _):
        print "Motion Sensor Connected"

    def on_disconnect(self, _):
        # Note: not dispatched when running in a debugger.
        print "Motion Sensor Disconnected"

    def on_exit(self, _):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        #save_frame_serial(controller.frame())
        save_frame_canonical(controller.frame())

    def state_string(self, state):
        """Convert the state enum to a string."""
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"
        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"
        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"
        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
        return "STATE_NULL"

def create_file(letter):
    """If the folder doesn't exist warn the user and create it."""
    if not os.path.exists(DATA_DIR):
        print "Couldn't find data directory, createing."
        os.makedirs(DATA_DIR)

    j = 0
    while os.path.exists(DATA_DIR+letter + str(j)+".csv"):
        j += 1

    return DATA_DIR+letter + str(j)+".csv"

def add_header():
    """Add the column headers to the CSV file."""
    header = []
    for vec in ['Normal', 'Direction', 'Center', 'Velocity']:
        for comp in ['x', 'y', 'z']:
            header.append("Palm "+vec+" "+comp)
    for flang in ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']:
        for n in [1, 2, 3]:
            header.append(flang+" Deviation "+str(n))
        for n in [1, 2]:
            header.append(flang+" Joint Angle "+str(n))
    header.append('Time Stamp')
    CSV_WRITER.writerow(header)

def record_single_char(l=""):
    """"Record a single gesgure sample to a file."""

    global are_there_hands
    global are_there_no_hands
    are_there_hands = threading.Event()
    are_there_no_hands = threading.Event()

    # Create a sample listener and controller
    listener = LeapSerrializingListner()
    controller = Leap.Controller()

    letter=""
    if l == "":
        print "Please enter a letter or word"
        print "(Blank to close)"
        letter = str(raw_input(": "))
        if letter == '':
            return ''
    else:
        letter = l
    csv_path = create_file(letter)
    with open(csv_path, 'a+') as csv_file:
        global CSV_WRITER
        CSV_WRITER = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        add_header()

        # Have the sample listener receive events from the controller
        controller.add_listener(listener)

        # Keep this process running until Enter is pressed
        try:
            timeout_reached = False
            timeout = 10
            timeout_counter = datetime.utcnow()
            print "Waiting for Hands..."
            while not are_there_hands.wait(.1):
                if (datetime.utcnow() - timeout_counter).total_seconds() > timeout:
                    #raise ValueError("No hands found.")
                    print "No hands Found."
                    return
            print "Recording..."
            timeout_counter = None
            timeout = 3
            while not timeout_reached:
                while are_there_hands.wait(.1):
                    timeout_counter = None
                if are_there_no_hands.is_set():
                    if timeout_counter == None:
                        timeout_counter = datetime.utcnow()
                    elif (datetime.utcnow() - timeout_counter).total_seconds() > timeout:
                        timeout_reached = True
            print "Finished"
        except KeyboardInterrupt:
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)
    return letter

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
       record_single_char(sys.argv[1])
    else:
       l = None
       while l != "":
           l=record_single_char()
