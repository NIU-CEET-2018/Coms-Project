#!/usr/bin/python3
import unittest
import AutoComplete


class AutoCompleteTests(unittest.TestCase):
        def setUp(self):
                pass

        def test_example(self):
                if len(AutoComplete.predict("")) == 0:
                        self.fail("shouldn't happen")

        def tearDown(self):
                pass
