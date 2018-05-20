.PHONY: run test
all: run

run:

test:
	python3 -m unittest *_test.py

reqs:
	pip3 install -r requirements.txt


