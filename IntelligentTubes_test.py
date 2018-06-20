#!/usr/bin/python3

"""The test file for Intelligent Tubes."""
import unittest
from IntelligentTubes import ThinkingSequence


class ThinkingSequenceUnitTests(unittest.TestCase):
    """The unit test suite for ThinkingSequence."""
    def setUp(self):
        """Nothing to setup here."""
        pass

    def test_existance(self):
        """Test that the class can hold data."""
        t = ThinkingSequence()
        if t.hasUpdated() is not False:
            self.fail("An update was detected before one was made.")
        t.recive(["the", "cat", "in", "the", "hat"])
        if t.getData() != ["the", "cat", "in", "the", "hat"]:
            self.fail("The structure contained the wrong data.")
        if t.hasUpdated() is not True:
            self.fail("No update Detected.")

    def test_basic_hook(self):
        """Test a basic hook."""
        def double(x):
            x.outData = []
            for v in x.inData:
                x.outData.append(v*2)
        t = ThinkingSequence()
        t.onUpdateHook = double
        t.recive([1, 2, 3, 4])
        if t.getData() != [2, 4, 6, 8]:
            self.fail("Wrong data found:"+str(t.getData()))

    def test_chain(self):
        """Test that it is chain-able."""
        t1 = ThinkingSequence()
        t2 = ThinkingSequence()

        def passData(x):
            x.hasUpdated()
            t2.recive(x.getData())

        t1.afterUpdateHook = passData

        t1.recive(["Test", "Text"])
        if t2.getData() != ["Test", "Text"]:
            self.fail("Wrong data found:"+str(t2.getData()))

    def tearDown(self):
        """Nothing to tearDown."""
        pass
