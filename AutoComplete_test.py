#!/usr/bin/python3

"""The test file for AutoComplete"""
import unittest
import AutoComplete


class AutoCompleteUnitTests(unittest.TestCase):
    """The unit test suite for auto-completion."""
    def setUp(self):
        """Nothing to setup here."""
        pass

    def test_autoCompleateLoads(self):
        """Check that autocomplete even loads"""
        if not AutoComplete.predict(""):
            self.fail("shouldn't happen")

    def tearDown(self):
        """Nothing to tearDown either."""
        pass
