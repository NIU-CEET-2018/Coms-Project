#!/usr/bin/python3
import unittest
import Gesture


class GesgureTests(unittest.TestCase):
        def setUp(self):
                pass

        def test_Bone_to_Gestlet_GofAI(self):
                # load up some known hands
                # pass them though the model
                # check it's right
                pass

        def test_Bone_to_Gestlet_AI(self):
                # pass in the same hands as above
                # check the output is the right shape
                pass

        def test_GestletPS_to_GesturePS_GofAI(self):
                # load up some pre-known gestlets
                # check that it's the right gesture
                pass

        def test_GestletPS_to_GesturePS_AI(self):
                # load up the same gestlets
                # check that it gives the right format
                pass

        def test_GesturePS_to_GestureMS_GofAI(self):
                pass

        def test_GesturePS_to_GestureMS_AI(self):
                pass
        
        def test_GestureS_to_Next_Gesture_GofAI(self):
                pass

        def test_GestureS_to_Next_Gesture_AI(self):
                pass

        def test_GestletsSeqToGesture_GofAI(self):
                # pass in some known sequences
                # check it outputs correctly
                pass

        def tearDown(self):
                pass
