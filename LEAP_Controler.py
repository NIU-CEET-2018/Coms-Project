#!/usr/bin/python3

"""Interface with the LEAP Motion to detect hand positions.
"""

import os

def raw_event_source(handler):
    """Spawn a python 2 interpreter for interfacing with the LEAP and pass
the events it generates to the handler."""
    sub = os.popen('python2', 'LEAP_Reader.py')
    l = sub.readline()
    while l:
        handler(l)
        l = sub.readline()

def event_loop(t_seq_in):
    """Call t_seq_in for each Leap event."""
    def event_handler(event):
        """Wrap the provided function with the needed parser for the Leap's data."""
        # TODO: should probably sanitize that
        data = eval(event)
        t_seq_in(data)
    raw_event_source(event_handler)
