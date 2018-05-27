.PHONY: run test
all: run

run:

test:
	python3 -m unittest *_test.py

reqs:
	dpkg -V $$(xargs < packages.txt) || sudo apt-get install -y -q $$(xargs < packages.txt)
	pip3 -q install -r requirements.txt


