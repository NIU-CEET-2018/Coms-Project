#!/usr/bin/python3

"""TODO: Docs"""


class ThinkingSequence():
    """This class that represents an updating data structure.

The class described here in is a is of a data-object that is meant to
sometimes update in value when another data-source updates (and then
cause ripple down effects from that update). This class is
intentionally designed to be chain-able with its self so that complex
sequences can be described in simple steps, similar to the Unix
pipe."""

    def __init__(self):
        """Initialize the hooks and values."""
        def dataCopy(x):
            x.outData = x.inData
        self.onUpdateHook = dataCopy
        self.afterUpdateHook = lambda x: 0
        self.inData = []
        self.outData = []
        self.changed = False

    def recive(self, d):
        """Change the data."""
        if self.inData != d:
            self.inData = d
            d = self.outData
            self.onUpdateHook(self)
            if self.outData != d:
                self.changed = True
                self.afterUpdateHook(self)

    def hasUpdated(self):
        if self.changed:
            self.changed = False
            return True
        return False

    def getData(self):
        return self.outData
