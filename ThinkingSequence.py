#!/usr/bin/python3

"""TODO: Docs"""


class ThinkingSequence():
    """A class that represents an updating vector.

The class described here in is similar to a const vector reference in
that the items within is could be manipulated still by the providing
thread, but the receiving thread is unable to change the values if
finds (only read them). This class will also have the ability to
inform others when changes have occurred and possibility the ability
to hook functions into it from the client side so that they can be
automatically called upon an update occurring (possibly
non-threaded)."""

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
