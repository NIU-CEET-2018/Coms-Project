import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import csv
import cPickle as pickle

letter = ''

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bones = {'Metacarpal'  : Bone.TYPE_METACARPAL,
             'Proximal'    : Bone.TYPE_PROXIMAL,
             'Intermediate': Bone.TYPE_INTERMEDIATE,
             'Distal'      : Bone.TYPE_DISTAL}
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
        LetterDict = pickle.load( open ( "letterdict.p", "rb"))

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, positionx: %s, positiony: %s, positionz: %s" % (
                handType, hand.id, hand.palm_position.x, hand.palm_position.y, hand.palm_position.z)

            # Get the hand's normal vector, direction, and position
            normal = hand.palm_normal
            direction = hand.direction
            hand_center = hand.palm_position

            #create data list
            data =[]
        
            #open csv file to write to
            with open('data.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',', lineterminator = '\n')

                # Get fingers
                for finger in hand.fingers:
                    print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                        self.finger_names[finger.type],
                        finger.id,
                        finger.length,
                        finger.width)

                    # Get bones
                    for b in self.bones:
                        bone = self.bones[b]
                        #subtract bone vector from palm vector
                        vectorx = bone.next_joint.x - hand_center.x
                        vectory = bone.next_joint.y - hand_center.y
                        vectorz = bone.next_joint.z - hand_center.z

                        #printing for our use
                        print "      Bone: %s, vectorx: %s, vectory: %s, vectorz: %s" % (
                            b,
                            vectorx,
                            vectory,
                            vectorz)

                        #add new vectors to data list
                        data.append(vectorx)
                        data.append(vectory)
                        data.append(vectorz)

                #adds the letter list to the end of the data list
                print "letter equals: %s" % (letter)
                data.extend(LetterDict[letter])
                
                print "     Data: %s" % (data)   
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
    letter = str(raw_input("Input letter:"))
    valid_input()
    raw_input("Press enter to record.")

def valid_input():
    LetterDict = pickle.load( open( "letterdict.p", "rb"))
    i = [0]*100
    if letter in LetterDict.keys():
        pass
    else:
        x = raw_input("This character is undefined. Would you like to define it? y/n: ")
        if x == 'y':
            l = len(LetterDict.keys())
            i[l] = 1
            LetterDict[letter] = i
            pickle.dump(LetterDict, open("letterdict.p", "wb"))
        else:
            main()

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
