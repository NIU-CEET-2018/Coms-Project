#!/usr/bin/python3

"""Intelligent Tubes

The classes described within this file describe a set of data pipes
that can perform specific actions on their content. The originating
purpose of this library is two fold: the first is for parallel AI
training; and, the second is to be able to set up a chain of simple
data processing calls that happen every-time there is an event.

For further information please read the docs of ThinkingSequence and
AIShepard. """
# TODO: Tensorflow here?


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
        def dataCopy(think_seq):
            """A simple placeholder function to copy the data."""
            think_seq.outData = think_seq.inData
        self.onUpdateHook = dataCopy
        self.afterUpdateHook = lambda x: 0
        self.inData = []
        self.outData = []
        self.changed = False

    def recive(self, data):
        """Change the data."""
        if self.inData != data:
            self.inData = data
            old_out_data = self.outData
            self.onUpdateHook(self)
            if self.outData != old_out_data:
                self.changed = True
                self.afterUpdateHook(self)

    def hasUpdated(self):
        """Check if the output has changed since last checked."""
        if self.changed:
            self.changed = False
            return True
        return False

    def getData(self):
        """Return the newest out-data and mark the system as read."""
        self.changed = False
        return self.outData


class LearningSequence(ThinkingSequence):
    """TODO: Docs"""

    def __init__(self, model):
        """Initialize with an AI."""
        ThinkingSequence.__init__(self)
        self.LEARNING = True
        self.BACKPROPOGATIN = True
        self.backPropHook = lambda x, y: 0
        self.correctedInData = []
        self.backConfidince = .9
        # use the model
        if isinstance(model, str):
            # if it's a valid file path, load it
            #     if it doesn't exist
            #         load a default and create the file
            pass
        else:  # if it's an AI
            # use it for the hooks
            self.model = model

    def correct(self, data, confidence=1):
        """Train against a correct output."""
        if self.LEARNING:
            # TODO: call self.model.correct(data)
            self.outData = data
        # TODO: update self.correctedInData
        if self.BACKPROPOGATIN:
            self.backPropHook(self.correctedInData,
                              confidence * self.backConfidince)

    def back_propogation_hook(self, func):
        """Set the function to be called in the case of back propagation."""
        self.backPropHook = func

    def __del__(self):
        """Save the model."""
        # TODO: save the model


class AIShepard(LearningSequence):
    """An AI Shepard for an AI Heard.

This class is designed to house and shepard several different AI
models within one containers such that each can be used when it is
most accurate, for the initial version there will be no attempt at
guessing which is best other than a time weighted sum (in contrast to
a system that attempts to analyses the input type). The intended
benefit of such a system is in that many different types of AI System
take different amounts of data to train and have different degrees of
accuracy once trained (and while training) by running several in
parallel and selecting between them one can hopefully take the "best
of each" and use them without the others' downsides. This is to be
used instead of pre-training the "best" of the systems because access
to the data is limited due to it being undesirable to try to collect
the data without the system being in place. (the data server no
propose other than to improve this system, but without this system
attempts to gather the data will require the creation of most of this
system and so the existence of early semi-accurate modeling will
provide great advantage over a "dead" device that simply collects data
until it is ready (and, this will also increase the speed of the
data's collection).) This system is being developed with the intent of
one of the (two) AI systems it owns to be a GofAI system so that it
can (with the knowledge of the programmer) kick-start the system's
accuracy rather than having to wait for the system to train.

In order to not destroy the typically fast execution time of each AI
system that is one of their benefits, each system will only be trained
with data on low priority threads that are forked off after the
"correct" system is chosen to use in the hot execution path. In order
to expedited the training time, the system can train the other
(non-used) AI on every uncorrected (assumed correct) output of the
current primary AI system. This is enabled by default as the initial
use of this system is for a slow learning AI system that will receive
a (probably) small amount of negative (active) feedback."""

    def __init__(self):
        LearningSequence.__init__(self)
