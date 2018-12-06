from pynput.keyboard import Key, Controller
from LEAP_Controler import raw_event_source
from Full_Live_Reader import splitter

keyboard=Controller()

def pressKey(key):
    keyboard.press(str(key))
    keyboard.release(str(key))

def handel_gesture(g):
    if len(g)==1:
        pressKey(g)
    else:
        if g == "right":
            pressKey(" ")
        elif g == "left":
            pass
        elif g == "down":
            pressKey(".")
        elif g == "nope":
            pass

if __name__ == "__main__":
    raw_event_source(lambda row: handel_gesture(splitter(row)))
    