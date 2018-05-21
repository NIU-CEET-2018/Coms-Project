#!/usr/bin/python3
import unittest
import SpeechSynth


class SpeechSynthTests(unittest.TestCase):
        def setUp(self):
                pass

        def test_can_say_words(self):
                SpeechSynth.sayText("This is a test.")

        def tearDown(self):
                pass
