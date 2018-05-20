#!/usr/bin/python3

import sys


def test():
    failed_tests = 0
    tests = 0
    # do the tests here
    if failed_tests == 0:
        print(sys.argv[0] + ": " +
              "Scuccsessfully finished all ("+str(tests)+") tests.")
        return 0
    else:
        print(sys.argv[0] + ": " +
              "Failed ("+str(failed_tests)+") out of ("+str(tests)+").")
        return 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        sys.exit(test())
