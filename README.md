CP Comunication System
======================

To anybody who is familare with python, I apologise. This repositoyry will be structured much more like C and C++.

Testing
=======

All python modules have a testing function when called ``./name.py test``.
Each module has either unit tests or integration tests depending on if it includes any other modules.

Modules
=======

Gesgure
-------
- Setup
  Takes a DB to store gesgures in
- Make/Refine Gesgure
  Takes a ``hand`` and a gesgure name
  no return
  incorperates that gesgure into the database
- ReadGesgure
  Takes a ``hand``.
  returns a tuple of ``(position, direction, gesgure)``, where ``gesgure`` is a vector of cirtenty for each known gesgure

AutoCompleate
-------------
- Setup
  Takes a dictionary of words with usage frequency
- predict
  Takes a vector of letter distubutions
  returns a vector of word probabilities
  
SpeachSynth
-----------
- Setup
  Takes a DB of phoneams
  Checks for a program for reading text.
- Say
  Takes a phrase or set of leters
  outputs an utterance to the speakers

LEAP
----
- Setup
  connects to the LEAP

USB Slave
---------

Gesgure Interface
-----------------
The Gesgure Interface is statefull and controls the user's actual experince
- Handel Frame
  Takes a vector of ``(position, direction, gesgure)`` for each hand visable
The outputs of this module are almost exclusivly though the attached screen.
