Sign Language Communication System
==================================

This repository describes a device for assisting individuals to communicate using sign language with others and computers.
This devices is (initially) aimed towards an individual with Cerebral Palsy who nigher learn standard ASL nor has the dexterity to perform such.

Setup
-----

Running ``make reqs`` will (on Debian) install the required packages through apt and pip3.

Testing
-------

All modules have an associated unittest script in ``./name_test.py``, ``make test`` will run all of these tests.


Hardware
========

- UDOO Ultra
- LEAP Motion Camera
- 3D Printed Case

Software Modules
================

LEAP Controller
---------------
- Setup
  connects to the LEAP
- Inputs
  A generator object that Streams out hand vectors.

Physics Filter
--------------
- Filter
  A generator object that is constructed on a stream of timestamped continuous physics measurements and filters out the suspicious measurements.

Gesture
-------
- Setup
  Loads up the necessary models for the internal AI and GofAI to function.
- Gesture_Input
  A generator object that returns a stream of tuple(Current Gesture Sequence, Next Gesture Prediction)
  Each of the sub modules have an AI and a GofAI version
  - Bone to Gestlet
    Converts bone structure information into probable Gestlets.
	(A gestlet is a particular hand position in a gesticulation.)
  - Gestlet Seq to P(Gesture)
	Converts a small sequence of Gestlets into a probable Gesture.
	OR
	Converts an updating sequence of Gestlets into an updating sequence of Gesture Probabilities.
  - P(Gesture) Seq to Gesture Seq
    Converts a Sequence of Gesture Probabilities into a most likely (Markovian?) sequence of Gestures.
	OR
	Converts an updating sequence of Gesture Probabilities into an updating sequence of most likely Gestures.
  - Current Gesture Seq to Next Gesture Prediction
    Takes in a Gesture Sequence and outputs the probable (next word) or (completion of current word).
- AI Multi-Path
  A trainable generator that is constructed on two generators, the first of which is the simplistic but functional generator and the second of which is the trainable but notes necessary good.
  the system will assume that he second starts off as not very good but as it trained will eventually swap out the old version for better/trained second version. This will occur over many runs of the program as data is collected and the system trained.
- Make Gesture
  Construct a new internal gesture from a given hand gesture.
- Train Gesture
  Improve the accuracy of a given gesture's recognition via manual repetition.

Speech Synth
------------
- Setup
  Initializes the speech engine(s).
- Say
  Takes a phrase or set of letters and produces an utterance to the speakers/headphones.

USB Keyboard Slave
------------------
The pretends to be a USB keyboard for simple interfacing with a host computer.
- Setup
- Type
  Outputs the set of chars as a keyboard would over usb.

Gesture Interface
-----------------
The Gesture Interface is stateful and controls the user's actual experience.
This module sets up and reads inputs from the LEAP->Phys->Gesture stack, and outputs to the screen along with calls to Speech Synth and USB Keyboard Slave.

TODO
====
- Add LEAP motion libs to make file
  ``https://forums.leapmotion.com/t/leap-motion-sdk-with-python-3-5-in-linux-tutorial/5249``
- Add tensorflow or tensorflow-gpu to pip requirements
  ``https://www.tensorflow.org/install/install_linux``

