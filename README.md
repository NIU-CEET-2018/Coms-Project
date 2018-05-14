CP Communication System
=======================

To anybody who is familiar with python, I apologize. This repository will be structured much more like C and C++.

Testing
=======

All python modules have a testing function when called ``./name.py test``.
Each module has either unit tests or integration tests depending on if it includes any other modules.

Modules
=======

Gesture
-------
- Setup
  Takes a DB to store gestures in
- Make/Refine Gesture
  Takes a ``hand`` and a gesture name
  no return
  incorporates that gesture into the database
- ReadGesgure
  Takes a ``hand``.
  returns a tuple of ``(position, direction, gesture)``, where ``gesture`` is a vector of certainty for each known gesture

AutoComplete
------------
- Setup
  Takes a dictionary of words with usage frequency
- predict
  Takes a vector of letter distributions
  returns a vector of word probabilities
  
SpeechSynth
-----------
- Setup
  Takes a DB of phonemes
  Checks for a program for reading text.
- Say
  Takes a phrase or set of letters
  outputs an utterance to the speakers

LEAP Controller
--------------
- Setup
  connects to the LEAP

USB Keyboard Slave
------------------
The pretends to be a USB keyboard for simple interfacing with a host computer.

Gesture Interface
-----------------
The Gesture Interface is stateful and controls the user's actual experience
- Handel Frame
  Takes a vector of ``(position, direction, gesture)`` for each hand visible
The outputs of this module are almost exclusively through the attached screen.

TODO
====
- Add LEAP motion libs to make file
  ``https://forums.leapmotion.com/t/leap-motion-sdk-with-python-3-5-in-linux-tutorial/5249``
- Add tensorflow or tensorflow-gpu to pip requirements
  ``https://www.tensorflow.org/install/install_linux``

