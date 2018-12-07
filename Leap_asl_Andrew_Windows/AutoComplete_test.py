#!/usr/bin/python3

"""The test file for AutoComplete"""
import unittest
import AutoComplete as ac


class AutoCompleteUnitTests(unittest.TestCase):
    """The unit test suite for auto-completion."""
    def setUp(self):
        """Nothing to setup here."""
        pass

    def test_autoCompleateLoads(self):
        """Check that autocomplete even loads"""
        if ac.predict()!=[]:
            self.fail("shouldn't happen")

    def test_cat_in_the_hat(self):
        """test a simple input output set."""
        # give it each letter unambigiously
        # check the output
    def test_uncirtenty(self):
        """Test the system's ability to predict with unciretn inputs."""
        # give "the cat in the hat" with parts overlayed
        def give(s):
            for l in s:
                ac.give([l])
        tstring = "the cat in the hat"
        give(tstring)
        if tstring != ac.known():
            self.fail('Failed to predic when given literaly all the things!\n' + \
                      'was "'+str(ac.known())+'"\n' + \
                      'should be "'+str(tstring)+'"')
    def test_by_parts(self):
        """ask for words while giving parts to get thing out incrementaly."""
        def give(s):
            for l in s:
                ac.give([l])
        out=''
        give('the ca')
        # check the output
        out += ' '.join(ac.known())
        # give more data
        give('t in t')
        # check output
        out += ' '.join(ac.known())
        # one more
        give('he hat')
        # this time with feeling
        out += ' '.join(ac.known())
        if out != 'the cat in the hat':
            self.fail('Failed to re-assemble the string\n'+
                      'out was "'+str(out)+'"')
        pass
    def test_uncirtenty_by_parts(self):
        """give partial dataas and check tha tthe output comes only when it is sure of the inputs."""
        pass
    def test_nospaces(self):
        """test that the system works when space chars aren't provided."""
        # make model
        # make the test string
        tstring = "the cat in the hat"
        # give the things
        def give(s):
            for l in s:
                ac.give(l)
        give(tstring.replace(' ',''))
        # check the output
        if ac.predict()!=tstring:
            self.fail('Failed to understand string with no spaces.')
        pass
    def tearDown(self):
        """Nothing to tearDown either."""
        pass
