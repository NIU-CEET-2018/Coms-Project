#!/usr/bin/python3

"""The test file for SpeechSynth."""
import unittest
import SpeechSynth


class SpeechSynthUnitTests(unittest.TestCase):
    """The unit test suite for SpeechSynth."""
    def setUp(self):
        """Noting to setup here."""
        pass

    def test_can_say_words(self):
        """A simple test that things work."""
        SpeechSynth.sayText("This is a test.")

    def tearDown(self):
        """Noting to tearDown."""
        pass
