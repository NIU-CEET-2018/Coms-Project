#!/usr/bin/python3
"""Converts text to speach."""

import pyttsx3
engine = pyttsx3.init()


def sayText(t):
    engine.say(t)
    engine.runAndWait()
