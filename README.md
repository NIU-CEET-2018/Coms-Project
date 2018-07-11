Sign Language Communication System
==================================

This repository describes a device for assisting individuals to communicate using sign language with others and computers.
This devices is (initially) aimed towards an individual with Cerebral Palsy who nigher learn standard ASL nor has the dexterity to perform such.

Setup
-----

Running ``make reqs`` will (on Debian) install the required packages (through apt, pip2, and pip3) and will install the Leap Daemon.

Testing
-------

Modules have associated unittest scripts, ``make test`` will run these tests.


Hardware
========

Bought
------

- [X] UDOO Ultra
- [X] IO
  - [X] LEAP Motion Camera
  - [X] FaceDancer
  - [X] 7" WaveShare LCD Screen
- [ ] Power
  - [ ] Battery
  - [ ] Battery Charger

Made
----
- [ ] 3D Printed Case
- [ ] Front Panel Circuit
   - [ ] Power Button
   - [ ] Shutdown on Low Battery
   - [ ] LED Indicator

Software Modules
================

Intelligent Tubes
-----------------
Intelligent Tubes is a library that has been developed for this application. It creates a Unix pipe like object called a `Thinking Sequence`.

LEAP Controller
---------------
This module is divided into two pieces because the Leap Motion Libraries for python have not yet been updated to Python 3. The Python 2 portion resides in `LEAP_Reader.py` and simply passes the LEAP's events out as text. The Python 3 portion captures this text in an event loop.

Physics Filter
--------------
A `Thinking Sequence` object that takes timestamped physics measurements and filters out the suspicious data. The system also tries to separate the data into distinct sequences based on temporal separation.

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
On importing the system initializes the speech engine(s).
When called the module takes a phrase or set of letters and produces an utterance to the standard audio out.

USB Keyboard Slave
------------------
The pretends to be a USB keyboard for simple interfacing with a host computer.

Gesture Interface
-----------------
The Gesture Interface is stateful and controls the user's actual experience.
This module sets up and reads inputs from the LEAP->Phys->Gesture stack, and outputs to the screen along with calls to Speech Synth and USB Keyboard Slave.

