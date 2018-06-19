#!/usr/bin/python3

"""Converts text to speech."""

from google_speech import Speech
import pyttsx3
pyttEngine = pyttsx3.init()

# TODO: Make the voice more suted to the client.
#       pyttsx3: https://pyttsx3.readthedocs.io/en/latest/engine.html
#       google_speech: http://sox.sourceforge.net/sox.html#EFFECTS


def sayText(Text):
    """Speak some text.

Will attempt to produce a high quality voice with google speech, but
will roll over to eSpeak if it can't reach the server."""

    def sayWithGoogle():
        """Speak some text with google, throw if can't."""
        Speech(Text, "en").play(("Speed", "1.2"))

    def sayWithESpeak():
        """Speak some text with eSpeak."""
        pyttEngine.say(Text)
        pyttEngine.runAndWait()

    try:
        sayWithGoogle()
    except Exception as e:
        # TODO: make this a ConnectionError
        print(e)
        sayWithESpeak()
