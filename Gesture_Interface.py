#!/usr/bin/python3

"""The way the user interacts between modes and what their interactions do."""

from IntelligentTubes import ThinkingSequence, AIShepard
import LEAP_Controler
import Physics_Filter
import Gesture
# TODO: import something ascii graphics?

def startLeapPipeline(pipeline):
    """Start the LEAP event Handler."""
    LEAP_Controler.event_loop(pipeline.recive)

def AIPipeline():
    """Assemble the Gesture understanding pipe."""
    # TODO: create instances of Gesture functions and Physics_Filter
    # and glue them together with AIShepards
    return ThinkingSequence()

def startInterface():
    """Run the onscreen interface."""
    screen = ThinkingSequence()
    # TODO: load hooks needed for screen update functions
    AIPipe = AIPipeline()
    # TODO: hook screen to the end of AIPipe
    startLeapPipeline(AIPipe)
