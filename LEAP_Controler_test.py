#!/usr/bin/python3
import unittest
import LEAP_Controler


class LeapControllerTests(unittest.TestCase):
        def setUp(self):
                pass

        def basic_test(self):
                LEAP_Controler.get_hand_position(True)

        def tearDown(self):
                pass
