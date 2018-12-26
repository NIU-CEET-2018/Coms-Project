from pynput.keyboard import Key, Controller
from LEAP_Controler import raw_event_source
from Full_Live_Reader import splitter
import time


keyboard=Controller()

def pressKey(key):
    keyboard.press(key)
    keyboard.release(key)

def handel_gesture(g):
    if g == None:
        pass
    elif len(g)==1:
        pressKey(g)
    else:
        if g == "close":
            pressKey(" ")
        elif g == "left":
            pressKey(Key.backspace)
        elif g == "down":
            pressKey(".")
        elif g == "nope":
            pass

if __name__ == "__main__":
    time.sleep(2)
    raw_event_source(lambda row: handel_gesture(splitter(row)))
    