#!/usr/bin/python3

# @package Speach_Synth
#
#

import pyttsx3
engine = pyttsx3.init()


def sayText(t):
    engine.say(t)
    engine.runAndWait()
