#!/usr/bin/python3

"""The test file for LEAP_Controler."""
import unittest
import LEAP_Controler


class LeapControllerUnitTests(unittest.TestCase):
    """The unit test suite for LEAP_Controler."""
    def setUp(self):
        """Noting to setup here."""
        pass

    def basic_test(self):
        """"Check that the functions don't crash."""
        LEAP_Controler.Get_Hand()

    def tearDown(self):
        pass
