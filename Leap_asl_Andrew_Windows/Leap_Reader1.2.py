#!/usr/bin/python2
import Leap
import csv, ctypes, os, sys, thread, time, math
import numpy as np

data_dir ='./Data_Folder/'
letter = ''
csv_path =''

debug_leap_prints = True

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bones = ['Metacarpal', 'Proximal', 'Medial', 'Distal' ]
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        if debub_mode:
            print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
                  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

             # Get the hand's normal vector, direction, and position
            normal = [hand.palm_normal.x, hand.palm_normal.y, hand.palm_normal.z]
            direction = [hand.direction.x, hand.direction.y, hand.direction.z]
            hand_center = [hand.palm_position.x, hand.palm_position.x, hand.palm_position.z]
            velocity = [hand.palm_velocity.x, hand.palm_velocity.y, hand.palm_velocity.z]

            if debug_leap_prints:
                print "  %s, id %d, hand position: %s, hand direction: %s, hand normal: %s, hand velocity: %s" % (
                      handType, hand.id, hand_center, direction, normal, velocity)

            #create data list
            data =[]
        
            #open csv file to write to
            with open(csv_path, 'a') as csv_file:
                # TODO: perf check opeing the file on each frame
                writer = csv.writer(csv_file, delimiter = ',', lineterminator = '\n')

                #add new vectors to data list
                data.append(hand_center[0])
                data.append(hand_center[1])
                data.append(hand_center[2])
                data.append(direction[0])
                data.append(direction[1])
                data.append(direction[2])
                data.append(normal[0])
                data.append(normal[1])
                data.append(normal[2])
                data.append(velocity[0])
                data.append(velocity[1])
                data.append(velocity[2])

                print data

                # Get fingers
                for finger in hand.fingers:
                    if debug_leap_prints:
                        print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                              self.finger_names[finger.type],
                              finger.id,
                              finger.length,
                              finger.width)

                    # Get bones
                    bone1 = [finger.bone(1).direction.x, finger.bone(1).direction.y, finger.bone(1).direction.z]
                    bone2 = [finger.bone(2).direction.x, finger.bone(2).direction.y, finger.bone(2).direction.z]
                    bone3 = [finger.bone(3).direction.x, finger.bone(3).direction.y, finger.bone(3).direction.z]

                    if debug_leap_prints:
                        print "Bone1: %s Bone2: %s Bones3: %s" % (bone1, bone2, bone3)

                    #angle of deviation of each bone from straight
                    deviation1 = math.cos(np.dot(bone1, direction))/(np.linalg.norm(bone1) * np.linalg.norm(direction))
                    deviation2 = math.cos(np.dot(bone2, direction))/(np.linalg.norm(bone1) * np.linalg.norm(direction))
                    deviation3 = math.cos(np.dot(bone3, direction))/(np.linalg.norm(bone1) * np.linalg.norm(direction))

                    # between each bone
                    joint_angle1 = math.cos(np.dot(bone1, bone2))/(np.linalg.norm(bone1) * np.linalg.norm(bone2))
                    joint_angle2 = math.cos(np.dot(bone2, bone3))/(np.linalg.norm(bone2) * np.linalg.norm(bone3))

                    # TODO: Put the above data in the desired canonical form.
                    # The 3 angles between the bones in the direction of normal
                    # The 3 angle beteen the bones and the plane of (normal X prior bone)

                    if debug_leap_prints:
                        print "deviation1: %s, deviation2: %s, deviation3: %s, jointangle1: %s, jointangle2: %s" % (
                              deviation1, deviation2, deviation3, joint_angle1, joint_angle2)
                    data.append(deviation1)
                    data.append(deviation2)
                    data.append(deviation3)
                    data.append(joint_angle1)
                    data.append(joint_angle2)


                writer.writerow(data)
    

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    
def start():
    # Takes in starting inputs
    global letter
    letter = str(raw_input("Input letter: "))
    create_file()
    raw_input("Press enter to record.")

def create_file():
    global csv_path

    # If the folder doesn't exist warn and create it.
    if not os.path.exists(data_dir):
        print "Couldn't find data directory, createing."
        os.makedirs(data_dir)

    j = 0
    while os.path.exists(data_dir+letter + str(j)+".csv"):
        j += 1

    csv_path = data_dir+letter + str(j)+".csv"
    with open(csv_path, 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',', lineterminator = '\n')
        header = [
            'Palm Normal x'       , 'Palm Normal y'       , 'Palm Normal z'       ,
            'Palm Direction x'    , 'Palm Direction y'    , 'Palm Direction z'    ,
            'Palm Center x'       , 'Palm Center y'       , 'Palm Center z'       ,
            'Palm Velocity x'     , 'Palm Velocity y'     , 'Palm Velocity z'     ,
            'Thumb Deviation 1'   , 'Thumb Deviation 2'   , 'Thumb Deviation 3'   ,
            'Thumb Joint Angle1'  , 'Thumb Joint Angle2'  ,
            'Index Deviation 1'   , 'Index Deviation 2'   , 'Index Deviation 3'   ,
            'Index Joint Angle 1' , 'Index Joint Angle 2' ,
            'Middle Deviation 1'  , 'Middle Deviation 2'  , 'Middle Deviation 3'  ,
            'Middle Joint Angle 1', 'Middle Joint Angle 2',
            'Ring Deviation 1'    , 'Ring Deviation 2'    , 'Ring Deviation 3'    ,
            'Ring Joint Angle 1'  , 'Ring Joint Angle 2'  ,
            'Pinky Deviation 1'   , 'Pinky Deviation 2'   , 'Pinky Deviation 3'   ,
            'Pinky Joint Angle 1' , 'Pinky Joint Angle 2' ,
        ]
        writer.writerow(header)

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    start()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
