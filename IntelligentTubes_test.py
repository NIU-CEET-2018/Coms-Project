#!/usr/bin/python3

"""The test file for Intelligent Tubes."""
import unittest
from IntelligentTubes import ThinkingSequence, LearningSequence, AIShepard


class ThinkingSequenceUnitTests(unittest.TestCase):
    """The unit test suite for ThinkingSequence."""
    def setUp(self):
        """Nothing to setup here."""
        pass

    def test_existance(self):
        """Test that the class can hold data."""
        thinkSeq = ThinkingSequence()
        if thinkSeq.hasUpdated() is not False:
            self.fail("An update was detected before one was made.")
        thinkSeq.recive(["the", "cat", "in", "the", "hat"])
        if thinkSeq.hasUpdated() is not True:
            self.fail("No update Detected.")
        if thinkSeq.getData() != ["the", "cat", "in", "the", "hat"]:
            self.fail("The structure contained the wrong data.")

    def test_basic_hook(self):
        """Test a basic hook."""
        def double(t_sequence):
            """Double the inData for a ThinkingSequence."""
            t_sequence.outData = []
            for v in t_sequence.inData:
                t_sequence.outData.append(v*2)
        thinkSeq = ThinkingSequence()
        thinkSeq.onUpdateHook = double
        thinkSeq.recive([1, 2, 3, 4])
        if thinkSeq.getData() != [2, 4, 6, 8]:
            self.fail("Wrong data found:"+str(thinkSeq.getData()))

    def test_chain(self):
        """Test that it is chain-able."""
        thinkSeq1 = ThinkingSequence()
        thinkSeq2 = ThinkingSequence()

        thinkSeq1.hook_as_next(thinkSeq2)

        thinkSeq1.recive(["Test", "Text"])
        if thinkSeq2.getData() != ["Test", "Text"]:
            self.fail("Wrong data found:"+str(thinkSeq2.getData()))

    def tearDown(self):
        """Nothing to tearDown."""
        pass

class LearningSequenceUnitTests(unittest.TestCase):
    """The unit test suite for LearningSequence."""
    def setUp(self):
        """Load a default module and don't let it learn."""
        self.model = LearningSequence("./testModel")
        self.model.LEARNING = False

    def tearDown(self):
        """Nothing to tearDown."""
        pass

class AIShepardUnitTests(unittest.TestCase):
    """The unit test suite for AIShepard."""
    def setUp(self):
        """Nothing to setup here."""
        model1 = LearningSequence("./testAIS1")
        model2 = LearningSequence("./testAIS2")
        self.model = AIShepard([model1, model2], "./testAISConfig")
        self.model.LEARNING = False

    def tearDown(self):
        """Nothing to tearDown."""
        pass
