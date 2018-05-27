#!/usr/bin/python3
"""Converts text to speach."""

from google_speech import Speech
import pyttsx3
engine = pyttsx3.init()

# TODO: Make the voice more suted to the client.
#       pyttsx3: https://pyttsx3.readthedocs.io/en/latest/engine.html
#       google_speech: http://sox.sourceforge.net/sox.html#EFFECTS


def sayText(t):
    def sayWithGoogle():
        Speech(t, "en").play(("Speed", "1.2"))

    def sayWithESpeak():
        engine.say(t)
        engine.runAndWait()

    try:
        sayWithGoogle()
    except:
        sayWithESpeak()
