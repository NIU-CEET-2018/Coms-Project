#!/usr/bin/python3

# @package USB_Keyboard_Slave
# This module pretends to be a USB Keyboard to transmit text.
#
# This moduel is ment to run on a raspberry pi with a [raspdancer](http://wiki.yobi.be/wiki/Raspdancer) atached.

import sys


def test():
    failed_tests = 0
    tests = 0
    if failed_tests == 0:
        print(sys.argv[0]+": " +
              "Scuccsessfully finished all ("+str(tests)+") tests.")
        return 0
    else:
        print(sys.argv[0]+": " +
              "Failed ("+str(failed_tests)+") out of ("+str(tests)+").")
        return 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        sys.exit(test())
