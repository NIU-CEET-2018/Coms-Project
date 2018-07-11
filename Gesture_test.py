#!/usr/bin/python3

"""The test file for Gesture."""
import unittest
import Gesture


class GesgureUnitTests(unittest.TestCase):
    """The unit test suite for Gesture."""
    def setUp(self):
        """Disable Learning while using the test data."""
        # Gesture.LEARNING = False
        pass

    def test_Bone_to_Gestlet_GofAI(self):
        """A basic Sanity test."""
        # load up some known hands
        # pass them though the model
        # check it's right
        pass

    def test_Bone_to_Gestlet_AI(self):
        """A basic Sanity test."""
        # pass in the same hands as above
        # check the output is the right shape
        pass

    def test_GestletPS_to_GesturePS_GofAI(self):
        """A basic Sanity test."""
        # load up some pre-known gestlets
        # check that it's the right gesture
        pass

    def test_GestletPS_to_GesturePS_AI(self):
        """A basic Sanity test."""
        # load up the same gestlets
        # check that it gives the right format
        pass

    def test_GesturePS_to_GestureMS_GofAI(self):
        """A basic Sanity test."""
        pass

    def test_GesturePS_to_GestureMS_AI(self):
        """A basic Sanity test."""
        pass

    def test_GestureS_to_Next_Gesture_GofAI(self):
        """A basic Sanity test."""
        pass

    def test_GestureS_to_Next_Gesture_AI(self):
        """A basic Sanity test."""
        pass

    def test_GestletsSeqToGesture_GofAI(self):
        """A basic Sanity test."""
        # pass in some known sequences
        # check it outputs correctly
        pass

    def tearDown(self):
        """Nothing to tearDown."""
        pass
